#!/usr/bin/env python3
"""Kiem tra lien ket noi bo trong cac file Markdown cua repo.

Bo qua lien ket ngoai (http/https/mailto), neo trong trang (#...), va moi
lien ket nam trong khoi code da rao bang ```.
"""
import os
import re
import sys

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def links_outside_code(text):
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK.finditer(line):
            yield lineno, match.group(1)


def main():
    broken = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            for lineno, link in links_outside_code(text):
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = link.split("#")[0]
                if not target:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(root, target))):
                    broken.append(f"{path}:{lineno} -> {link}")

    if broken:
        print(f"{len(broken)} lien ket gay:")
        for item in broken:
            print("  " + item)
        return 1
    print("Tat ca lien ket noi bo deu hop le.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
