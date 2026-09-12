"""Select IDs once from all COCO2017 val IDs, before detector outcomes."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    coco = json.loads(args.annotations.read_text())
    ids = sorted(row["id"] for row in coco["images"])
    assert len(ids) == len(set(ids)) == 5000
    selected = sorted(random.Random(20260912).sample(ids, 1000))
    selected_set = set(selected)
    smoke = [i for i in ids if i not in selected_set][:3]
    # Coverage is descriptive after selection; it never changes the IDs.
    coverage = Counter(a["category_id"] for a in coco["annotations"] if a["image_id"] in selected_set)
    output = {"seed": 20260912, "procedure": "Python random.Random(seed).sample(sorted(all5000IDs),1000), then sort",
              "primary_ids": selected, "smoke_ids": smoke,
              "annotation_sha256": hashlib.sha256(args.annotations.read_bytes()).hexdigest(),
              "coverage_instances": dict(sorted(coverage.items())),
              "covered_classes": len(coverage), "instances_including_crowd": sum(coverage.values())}
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"primary_count": len(selected), "smoke_ids": smoke,
                      "covered_classes": len(coverage), "instances": sum(coverage.values())}))


if __name__ == "__main__":
    main()
