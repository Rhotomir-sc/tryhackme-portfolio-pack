"""Check inline relative Markdown links and balanced fences; no network access.

Checks paths only, not heading anchors, reference-style links, or external URLs.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import unquote, urlsplit


def check(root, known_paths=None):
    errors = []
    if known_paths is None:
        known_paths = {p.relative_to(root).as_posix() for p in root.rglob('*')
                       if '.git' not in p.relative_to(root).parts}
    else:
        known_paths = set(known_paths)
    for path in list(known_paths):
        known_paths.update(str(p) for p in PurePosixPath(path).parents if str(p) != '.')
    for file in sorted(root.rglob('*.md')):
        if '.git' in file.relative_to(root).parts:
            continue
        relative = file.relative_to(root).as_posix()
        fence = None
        for number, line in enumerate(file.read_text(encoding='utf-8').splitlines(), 1):
            match = re.match(r'^\s*(`{3,}|~{3,})', line)
            if match:
                token = match.group(1)
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence):
                    fence = None
                continue
            if fence:
                continue
            for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', line):
                target = target.strip()
                if target.startswith('<') and '>' in target:
                    target = target[1:target.index('>')]
                else:
                    target = re.split(r'\s+[\"\']', target, maxsplit=1)[0]
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target_path = unquote(parsed.path)
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative), target_path))
                if target_path.startswith('/') or resolved == '..' or resolved.startswith('../') or resolved not in known_paths:
                    errors.append(f'{relative}:{number}: missing/outside local target {target}')
        if fence:
            errors.append(f'{relative}: unclosed code fence')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paths-json', type=Path, help='Optional path manifest for a partial local checkout')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = json.loads(args.paths_json.read_text(encoding='utf-8')) if args.paths_json else None
    errors = check(root, paths)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print('Local Markdown paths and code fences passed')
