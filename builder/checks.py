from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

from builder.log import BuildError


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value and value.startswith('/'):
                self.links.append(value)


def check_internal_links(out_dir):
    broken = []
    checked = 0
    for page in sorted(out_dir.rglob('*.html')):
        collector = LinkCollector()
        collector.feed(page.read_text(encoding='utf-8'))
        checked += len(collector.links)
        for link in collector.links:
            target = out_dir / unquote(urlparse(link).path).lstrip('/')
            if target.is_dir():
                target = target / 'index.html'
            if not target.exists():
                broken.append(f'{page.relative_to(out_dir)}: {link}')

    if broken:
        raise BuildError(f'{len(broken)} broken internal link(s):\n' + '\n'.join(broken))
    return checked
