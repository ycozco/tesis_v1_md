"""Fail a Pages build if its entry points, links or chapter images are missing."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        attribute = 'src' if tag in ('img', 'script') else 'href' if tag in ('a', 'link') else None
        if attribute and values.get(attribute):
            self.paths.append(values[attribute])


def verify(directory):
    root = Path(directory).resolve()
    errors = []
    for name in ('index.html', '02-95-tesis.html', 'tesis-completa.html', '.nojekyll'):
        if not (root / name).is_file():
            errors.append(f'Missing entry point: {name}')
    pages = list(root.glob('*.html'))
    for page in pages:
        parser = References()
        parser.feed(page.read_text(encoding='utf-8'))
        for reference in parser.paths:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            # Only validate published pages/assets; source Markdown links are documents.
            if Path(path).suffix.lower() not in ('.html', '.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.css', '.js'):
                continue
            target = (page.parent / path).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f'{page.name}: missing published file {reference}')
    if errors:
        raise SystemExit('\n'.join(sorted(set(errors))))
    print(f'Pages verified: {len(pages)} HTML pages and their local assets.')


if __name__ == '__main__':
    verify(sys.argv[1] if len(sys.argv) > 1 else '_site')
