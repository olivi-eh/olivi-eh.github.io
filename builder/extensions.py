import re
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor

from builder.config import domain


def get_internal_prefixes(site_domain: str = domain) -> tuple[str, ...]:
    parsed = urlparse(site_domain)
    host = parsed.hostname or ''
    base_host = host[4:] if host.startswith('www.') else host

    if not base_host:
        return ()

    prefixes = []
    for scheme in ('http', 'https'):
        prefixes.append(f'{scheme}://{base_host}')
        prefixes.append(f'{scheme}://www.{base_host}')
    return tuple(prefixes)


class AutoExternalLinksTreeprocessor(Treeprocessor):
    def __init__(self, md=None, site_domain: str = domain):
        super().__init__(md)
        self.internal_prefixes = get_internal_prefixes(site_domain)

    def run(self, root):
        for element in root.iter('a'):
            href = element.get('href', '')
            is_external = (
                href.startswith(('http://', 'https://'))
                and not href.startswith(self.internal_prefixes)
            )
            is_pdf = href.endswith('.pdf')
            if is_external or is_pdf:
                element.set('target', '_blank')


class AutoExternalLinksExtension(Extension):
    def __init__(self, site_domain: str = domain, **kwargs):
        super().__init__(**kwargs)
        self.site_domain = site_domain

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            AutoExternalLinksTreeprocessor(md, site_domain=self.site_domain),
            'auto_external_links',
            15,
        )


class SectionFootnotesTreeprocessor(Treeprocessor):
    def run(self, root):
        parent_map = {c: p for p in root.iter() for c in p}
        for p in list(root.iter('p')):
            if not p.text:
                continue
            lines = p.text.split('\n')
            if any(
                re.match(r'^(?:\[\^(\*|\d+)\]:?|\^(\*|\d+)\^?|<sup>(\*|\d+)</sup>:?)\s*', line)
                for line in lines
            ):
                parent = parent_map.get(p, root)
                idx = list(parent).index(p)
                parent.remove(p)
                for i, line in enumerate(lines):
                    m = re.match(
                        r'^(?:\[\^(\*|\d+)\]:?|\^(\*|\d+)\^?|<sup>(\*|\d+)</sup>:?)\s*(.*)',
                        line,
                    )
                    if m:
                        symbol = m.group(1) or m.group(2) or m.group(3)
                        rest = m.group(4)
                        new_p = ET.Element('p')
                        new_p.attrib['class'] = 'text-small'
                        sup = ET.Element('sup')
                        sup.text = symbol
                        sup.tail = rest
                        new_p.append(sup)
                        parent.insert(idx + i, new_p)
                    else:
                        new_p = ET.Element('p')
                        new_p.text = line
                        parent.insert(idx + i, new_p)

        for elem in root.iter():
            if elem.tag not in ('script', 'style'):
                if elem.tag == 'p' and elem.attrib.get('class') == 'text-small':
                    continue
                if elem.text:
                    elem.text = re.sub(r'\[\^(\*|\d+)\]', r'<sup>\1</sup>', elem.text)
                if elem.tail:
                    elem.tail = re.sub(r'\[\^(\*|\d+)\]', r'<sup>\1</sup>', elem.tail)


class SectionFootnotesExtension(Extension):
    def extendMarkdown(self, md):
        for reg in (
            md.preprocessors,
            md.inlinePatterns,
            md.parser.blockprocessors,
            md.treeprocessors,
        ):
            for key in list(reg._data.keys()):
                if 'footnote' in key.lower():
                    reg.deregister(key)
        md.treeprocessors.register(
            SectionFootnotesTreeprocessor(md), 'section_footnotes', 25
        )


class ShortcodesInlineProcessor(InlineProcessor):
    CLASS_MAP = {'small': 'text-small', 'caption': 'img-caption'}

    def handleMatch(self, m, data):
        tag_type = m.group(1)
        text = m.group(2)
        class_name = self.CLASS_MAP.get(tag_type, tag_type)
        span = ET.Element('span')
        span.attrib['class'] = class_name
        span.text = text
        return span, m.start(0), m.end(0)


class ShortcodesExtension(Extension):
    def extendMarkdown(self, md):
        pattern = r'\{(small|caption):\s*(.*?)\}'
        md.inlinePatterns.register(
            ShortcodesInlineProcessor(pattern, md), 'shortcodes', 175
        )


def get_markdown_instance(site_domain: str = domain) -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            'meta',
            'extra',
            'smarty',
            'admonition',
            AutoExternalLinksExtension(site_domain=site_domain),
            SectionFootnotesExtension(),
            ShortcodesExtension(),
        ]
    )
