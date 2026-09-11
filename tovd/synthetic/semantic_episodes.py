from dataclasses import dataclass, replace

import torch
from torch import Tensor
from torch.nn import functional as F


@dataclass
class WorldConfig:
    dim: int = 16
    clusters: int = 12
    classes_per_cluster: int = 10
    train_clusters: int = 8
    spread: float = 0.35
    text_noise: float = 0.02
    observation_noise: float = 0.10
    nonlinear_scale: float = 0.15
    vocabulary_size: int = 4
    queries: int = 8
    foreground_tokens: int = 16
    distractor_tokens: int = 8
    background_tokens: int = 8
    seed: int = 20260912


@dataclass
class Episode:
    X: Tensor
    T: Tensor
    Q: Tensor
    labels: Tensor
    vocabulary_ids: Tensor
    query_ids: Tensor
    image_ids: Tensor  # -1 denotes background; audit only, never model input.

    def to(self, device):
        return Episode(**{name: value.to(device) for name, value in vars(self).items()})

    def permute_vocabulary(self, order: Tensor):
        inverse = torch.argsort(order)
        return replace(self, T=self.T[order], vocabulary_ids=self.vocabulary_ids[order],
                       labels=inverse[self.labels])


class SemanticWorld:
    """Fixed class world; episode RNG is separate from world/model RNG."""

    def __init__(self, config: WorldConfig):
        self.config = config
        g = torch.Generator().manual_seed(config.seed)
        count = config.clusters * config.classes_per_cluster
        self.cluster_ids = torch.arange(config.clusters).repeat_interleave(config.classes_per_cluster)
        centers = F.normalize(torch.randn(config.clusters, config.dim, generator=g), dim=-1)
        residual = F.normalize(torch.randn(count, config.dim, generator=g), dim=-1)
        self.prototypes = F.normalize(centers[self.cluster_ids] + config.spread * residual, dim=-1)
        self.text_rotation = torch.linalg.qr(torch.randn(config.dim, config.dim, generator=g)).Q
        self.visual_rotation = torch.linalg.qr(torch.randn(config.dim, config.dim, generator=g)).Q
        self.text = F.normalize(self.prototypes @ self.text_rotation + config.text_noise *
                                torch.randn(count, config.dim, generator=g), dim=-1)
        self.train_ids = torch.where(self.cluster_ids < config.train_clusters)[0]
        self.test_ids = torch.where(self.cluster_ids >= config.train_clusters)[0]

    def split_ids(self, split):
        return self.train_ids if split == "train" else self.test_ids

    def vocabulary(self, split, hardness, g, anchor=None):
        c = self.config
        available = self.split_ids(split)
        if anchor is None:
            anchor = available[torch.randint(len(available), (), generator=g)]
        anchor = int(anchor)
        cluster = int(self.cluster_ids[anchor])
        if hardness == "hard":
            pool = available[(self.cluster_ids[available] == cluster) & (available != anchor)]
            rest = pool[torch.randperm(len(pool), generator=g)[:c.vocabulary_size-1]]
        else:
            clusters = torch.unique(self.cluster_ids[available])
            clusters = clusters[clusters != cluster]
            selected = clusters[torch.randperm(len(clusters), generator=g)[:c.vocabulary_size-1]]
            rest = torch.stack([members[torch.randint(len(members), (), generator=g)] for members in
                                [available[self.cluster_ids[available] == item] for item in selected]])
        ids = torch.cat([torch.tensor([anchor]), rest])
        return ids[torch.randperm(len(ids), generator=g)]

    def visual_view(self, ids, g):
        z = self.prototypes[ids]
        latent = z + self.config.nonlinear_scale * torch.tanh(2 * z)
        noise = self.config.observation_noise * torch.randn(*z.shape, generator=g)
        return F.normalize(latent @ self.visual_rotation + noise, dim=-1)

    def _scene(self, split, vocabulary, g, single_class=None):
        c = self.config
        foreground = (vocabulary[torch.randperm(len(vocabulary), generator=g)[:2]]
                      if single_class is None else torch.tensor([single_class]))
        query_ids = foreground[torch.randint(len(foreground), (c.queries,), generator=g)]
        foreground_ids = foreground[torch.randint(len(foreground), (c.foreground_tokens,), generator=g)]
        available = self.split_ids(split)
        pool = available[~torch.isin(available, vocabulary)]
        distractor_ids = pool[torch.randint(len(pool), (c.distractor_tokens,), generator=g)]
        image_ids = torch.cat([foreground_ids, distractor_ids, torch.full((c.background_tokens,), -1)])
        X = torch.cat([self.visual_view(foreground_ids, g), self.visual_view(distractor_ids, g),
                       F.normalize(torch.randn(c.background_tokens, c.dim, generator=g), dim=-1)])
        order = torch.randperm(len(X), generator=g)
        labels = (query_ids[:, None] == vocabulary[None, :]).long().argmax(-1)
        return Episode(X[order], self.text[vocabulary], self.visual_view(query_ids, g), labels,
                       vocabulary, query_ids, image_ids[order])

    def episode(self, split, hardness, seed):
        g = torch.Generator().manual_seed(seed)
        return self._scene(split, self.vocabulary(split, hardness, g), g)

    def paired_scene(self, seed):
        """Same X/Q, anchor-preserving easy/hard vocabularies, plus unrelated T."""
        g = torch.Generator().manual_seed(seed)
        anchor = int(self.test_ids[torch.randint(len(self.test_ids), (), generator=g)])
        easy_ids = self.vocabulary("test", "easy", g, anchor)
        hard_ids = self.vocabulary("test", "hard", g, anchor)
        easy = self._scene("test", easy_ids, g, single_class=anchor)
        labels = (easy.query_ids[:, None] == hard_ids[None, :]).long().argmax(-1)
        hard = replace(easy, T=self.text[hard_ids], vocabulary_ids=hard_ids, labels=labels)
        pool = self.test_ids[self.test_ids != anchor]
        unrelated = pool[torch.randperm(len(pool), generator=g)[:self.config.vocabulary_size]]
        # No labels are supplied for this deliberately out-of-vocabulary query.
        return easy, hard, self.text[unrelated], unrelated


def stack_episodes(episodes, device="cpu"):
    return tuple(torch.stack([getattr(ep, name) for ep in episodes]).to(device)
                 for name in ("X", "T", "Q", "labels"))
