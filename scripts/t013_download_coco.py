"""Eight HTTP ranges for the observed slow official COCO connection."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile


def download(url, target):
    request = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        content_range = response.headers["Content-Range"]
        total = int(content_range.split("/")[-1])
        etag = response.headers.get("ETag")
    parts = target.parent / (target.name + ".parts")
    parts.mkdir(exist_ok=True)
    chunk_size = 4 * 1024 * 1024
    ranges = [(i, start, min(total, start + chunk_size))
              for i, start in enumerate(range(0, total, chunk_size))]

    def fetch(spec):
        index, start, stop = spec
        part = parts / f"{index:04d}"
        have = part.stat().st_size if part.exists() else 0
        if have < stop - start:
            request = urllib.request.Request(url, headers={"Range": f"bytes={start + have}-{stop - 1}"})
            with urllib.request.urlopen(request, timeout=120) as response:
                assert response.status == 206
                assert response.headers["Content-Range"] == f"bytes {start + have}-{stop - 1}/{total}"
                with part.open("ab") as output:
                    shutil.copyfileobj(response, output, length=1024 * 1024)
        assert part.stat().st_size == stop - start
        return index

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch, spec) for spec in ranges]
        for completed, future in enumerate(as_completed(futures), 1):
            index = future.result()
            print(f"{target.name}: part {index} complete; {completed}/{len(ranges)}", flush=True)
    with target.open("wb") as output:
        for index, _, _ in ranges:
            with (parts / f"{index:04d}").open("rb") as source:
                shutil.copyfileobj(source, output)
    assert target.stat().st_size == total
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
    with target.open("rb") as source:
        sha = hashlib.file_digest(source, "sha256").hexdigest()
    return {"url": url, "path": str(target), "size": total, "etag": etag,
            "sha256": sha, "zip_crc_all_entries_passed": True, "connections": 8}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    receipts = []
    for name, url, output_name in [
        ("annotations", "http://images.cocodataset.org/annotations/annotations_trainval2017.zip", "annotations_trainval2017.parallel.zip"),
        ("images", "http://images.cocodataset.org/zips/val2017.zip", "val2017.parallel.zip"),
    ]:
        archive_path = args.destination / output_name
        receipt = download(url, archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            if name == "annotations":
                archive.extract("annotations/instances_val2017.json", args.destination)
            else:
                archive.extractall(args.destination)
        receipts.append(receipt)
        args.receipt.write_text(json.dumps(receipts, indent=2) + "\n")
        print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
