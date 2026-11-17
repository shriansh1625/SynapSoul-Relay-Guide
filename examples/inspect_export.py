"""Verify a JSONL export against its manifest and print source citations."""

import argparse
import hashlib
import json
from pathlib import Path


def inspect(manifest_path: Path, export_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files")
    jsonl = manifest
    if files is not None:
        jsonl = next((file for file in files if file["format"] == "jsonl"), None)
    if jsonl is None:
        raise ValueError("The manifest has no JSONL export.")

    seen = set()
    citations = set()
    checksum = hashlib.sha256()
    byte_count = 0
    with export_path.open("rb") as export:
        for line in export:
            checksum.update(line)
            byte_count += len(line)
            record = json.loads(line)
            record_id = record["record_id"]
            if record_id in seen:
                raise ValueError("The file contains a duplicate record ID.")
            seen.add(record_id)
            for source in record["provenance"]:
                citations.add((source["source_id"], source["source_revision"], source["source_url"]))

    if byte_count != jsonl["byte_count"] or checksum.hexdigest() != jsonl["sha256"]:
        raise ValueError("The JSONL size or SHA-256 does not match the manifest.")
    if len(seen) != manifest["record_count"]:
        raise ValueError("The JSONL record count does not match the manifest.")
    print(f"Verified version {manifest['version']} with {len(seen)} records")
    for source_id, revision, url in sorted(citations):
        print(f"{source_id} (revision {revision}): {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    try:
        inspect(args.manifest, args.jsonl)
    except (OSError, KeyError, ValueError, TypeError) as error:
        parser.exit(1, f"Verification failed: {error}\n")
