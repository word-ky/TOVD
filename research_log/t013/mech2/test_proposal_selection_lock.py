"""Synthetic-only selector/gather tests on explicitly selected tensor device."""
import os
import unittest
import torch
from proposal_selection_lock import select_references


class ProposalLockTests(unittest.TestCase):
    def setUp(self):
        self.device = os.environ.get('MECH2_TEST_DEVICE', 'cpu')
        self.logits = torch.arange(48, dtype=torch.float32, device=self.device).reshape(2, 8, 3)
        self.coords = torch.arange(64, dtype=torch.float32, device=self.device).reshape(2, 8, 4).requires_grad_()
        self.i0 = torch.tensor([[1, 5, 2], [4, 0, 6]], dtype=torch.int64, device=self.device)

    def test_native_identity(self):
        for logits in (self.logits, torch.ones_like(self.logits)):
            with self.subTest(ties=bool(torch.all(logits == 1))):
                indices, refs = select_references(logits, self.coords, 3)
                direct = torch.topk(logits.max(-1)[0], 3, dim=1)[1]
                self.assertTrue(torch.equal(indices, direct))
                self.assertTrue(torch.equal(refs, torch.gather(self.coords, 1, direct.unsqueeze(-1).repeat(1,1,4))))
                self.assertFalse(refs.requires_grad)

    def test_override_uses_only_vx_coordinates(self):
        before = self.coords.clone()
        indices, refs = select_references(self.logits, self.coords, 3, self.i0)
        self.assertTrue(torch.equal(indices, self.i0))
        self.assertTrue(torch.equal(refs, torch.gather(self.coords, 1, self.i0.unsqueeze(-1).repeat(1,1,4))))
        _, shifted = select_references(self.logits, self.coords + 1000, 3, self.i0)
        self.assertTrue(torch.equal(shifted, refs + 1000))
        self.assertTrue(torch.equal(before, self.coords))
        self.assertFalse(refs.requires_grad)
        # No V0 coordinate, score or feature parameter exists in the helper.

    def test_override_order_preserved(self):
        _, refs = select_references(self.logits, self.coords, 3, self.i0)
        permutation = torch.tensor([2,0,1], device=self.device)
        indices, permuted = select_references(self.logits, self.coords, 3, self.i0[:,permutation])
        self.assertTrue(torch.equal(indices, self.i0[:,permutation]))
        self.assertTrue(torch.equal(permuted, refs[:,permutation]))

    def test_null_intervention_identity(self):
        indices, refs = select_references(self.logits, self.coords, 3)
        locked_indices, locked_refs = select_references(self.logits, self.coords, 3, indices)
        self.assertTrue(torch.equal(indices, locked_indices))
        self.assertTrue(torch.equal(refs, locked_refs))

    def test_invalid_override_rejected(self):
        bad = [self.i0.float(), self.i0.int(), self.i0[0], self.i0[:1], self.i0[:,:2],
               torch.tensor([[-1,1,2],[0,1,2]],device=self.device),
               torch.tensor([[8,1,2],[0,1,2]],device=self.device),
               torch.tensor([[1,1,2],[0,1,2]],device=self.device)]
        for n, indices in enumerate(bad):
            with self.subTest(case=n), self.assertRaises(ValueError):
                select_references(self.logits, self.coords, 3, indices)

    def test_invalid_requested_count_rejected(self):
        for count in (0, 9, 3.0, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                select_references(self.logits, self.coords, count)


if __name__ == '__main__':
    unittest.main()
