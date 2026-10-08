#!/usr/bin/env python3
"""Regenerates content_manifest.txt from the videos/ folder.

Each line is "relative/path.mp4|sha256hex" (forward slashes). The app
(Program.cs CheckForContentUpdatesAsync) downloads a file if it's missing
locally OR its local SHA-256 doesn't match the hash here - so editing an
existing video and re-running this script is enough to push that edit to
every customer on their next content check.

Run from the repo root after adding/editing files under videos/:
    python generate_manifest.py
Then bump content_version.txt and commit both.
"""
import hashlib
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(ROOT, "videos")
MANIFEST = os.path.join(ROOT, "content_manifest.txt")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    entries = []
    for dirpath, _dirnames, filenames in os.walk(VIDEOS_DIR):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, VIDEOS_DIR).replace(os.sep, "/")
            entries.append((rel, sha256_of(full)))
    entries.sort(key=lambda e: e[0].lower())

    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        for rel, digest in entries:
            f.write(f"{rel}|{digest}\n")

    print(f"Wrote {len(entries)} entries to {MANIFEST}")


if __name__ == "__main__":
    main()
