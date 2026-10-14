from datetime import date, datetime, time
from email.utils import format_datetime
from xml.etree import ElementTree as ET

from builder.config import (
    author,
    default_description,
    default_title,
    domain,
    language,
    timezone,
)

ATOM_NS = 'http://www.w3.org/2005/Atom'
ET.register_namespace('atom', ATOM_NS)


def to_datetime(d: date) -> datetime:
    return datetime.combine(d, time(), tzinfo=timezone)


def write_xml(root, path):
    ET.indent(root)
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)


def generate_sitemap(pages, out_dir):
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for page in pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = page['url']
        if page['modified']:
            ET.SubElement(url, 'lastmod').text = page['modified'].isoformat()
    write_xml(urlset, out_dir / 'sitemap.xml')


def generate_rss(posts, out_dir):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = default_title
    ET.SubElement(channel, 'link').text = domain
    ET.SubElement(channel, 'description').text = default_description
    ET.SubElement(channel, 'language').text = language
    ET.SubElement(channel, 'docs').text = 'https://www.rssboard.org/rss-specification'
    ET.SubElement(
        channel, f'{{{ATOM_NS}}}link',
        href=f'{domain}rss.xml', rel='self', type='application/rss+xml',
    )
    ET.SubElement(channel, 'ttl').text = '60'
    for post in posts:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['title_raw']
        ET.SubElement(item, 'link').text = post['url']
        ET.SubElement(item, 'description').text = post['description']
        ET.SubElement(item, 'pubDate').text = format_datetime(to_datetime(post['published']))
        ET.SubElement(item, 'guid').text = post['url']
    write_xml(rss, out_dir / 'rss.xml')


def generate_atom(posts, out_dir):
    def el(parent, tag, text=None, **attrib):
        e = ET.SubElement(parent, tag, attrib)
        e.text = text
        return e

    feed = ET.Element('feed', xmlns=ATOM_NS)
    el(feed, 'title', default_title)
    el(feed, 'link', href=domain)
    el(feed, 'link', rel='self', href=f'{domain}atom.xml')
    el(feed, 'id', domain)
    last_updated = max((post['modified'] or post['published'] for post in posts), default=date.today())
    el(feed, 'updated', to_datetime(last_updated).isoformat())
    el(el(feed, 'author'), 'name', author)
    for post in posts:
        entry = el(feed, 'entry')
        el(entry, 'title', post['title_raw'])
        el(entry, 'summary', post['description'])
        el(entry, 'link', rel='alternate', href=post['url'])
        el(entry, 'updated', to_datetime(post['modified'] or post['published']).isoformat())
        el(entry, 'published', to_datetime(post['published']).isoformat())
        el(entry, 'id', post['url'])
    write_xml(feed, out_dir / 'atom.xml')
