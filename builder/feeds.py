from datetime import date, datetime

from builder.config import (
    OUT_DIR,
    author,
    default_description,
    default_title,
    domain,
)


def generate_sitemap(pages_meta):
    print('  ├── Generating sitemap... ', end='', flush=True)
    sitemap_path = OUT_DIR / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for vars in pages_meta:
            f.write('  <url>\n')
            f.write(f'    <loc>{vars["url"]}</loc>\n')
            f.write(f'    <lastmod>{vars["modified"]}</lastmod>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')
    print('Done!')


def generate_rss(pages_meta):
    print('  ├── Generating RSS feed... ', end='', flush=True)
    rss_path = OUT_DIR / 'rss.xml'
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n')
        f.write('  <channel>\n')
        f.write(f'    <title>{default_title}</title>\n')
        f.write(f'    <link>{domain}</link>\n')
        f.write(f'    <description>{default_description}</description>\n')
        f.write('    <language>en-us</language>\n')
        f.write('    <docs>https://www.rssboard.org/rss-specification</docs>\n')
        f.write(f'    <atom:link href="{domain}rss.xml" rel="self" type="application/rss+xml" />\n')
        f.write('    <ttl>60</ttl>\n')
        for vars in pages_meta:
            if vars["published"] == '':
                continue
            pub_date = datetime.strptime(vars["published"], "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S EST")
            f.write('    <item>\n')
            f.write(f'      <title>{vars["title_raw"]}</title>\n')
            f.write(f'      <link>{vars["url"]}</link>\n')
            f.write(f'      <description>{vars["description"]}</description>\n')
            f.write(f'      <pubDate>{pub_date}</pubDate>\n')
            f.write(f'      <guid>{vars["url"]}</guid>\n')
            f.write('    </item>\n')
        f.write('  </channel>\n')
        f.write('</rss>\n')
    print('Done!')


def generate_atom(pages_meta):
    print('  ├── Generating Atom feed... ', end='', flush=True)
    atom_path = OUT_DIR / 'atom.xml'
    with open(atom_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<feed xmlns="http://www.w3.org/2005/Atom">\n')
        f.write(f'  <title>{default_title}</title>\n')
        f.write(f'  <link href="{domain}" />\n')
        f.write(f'  <link rel="self" href="{domain}atom.xml" />\n')
        f.write(f'  <id>{domain}</id>\n')
        f.write(f'  <updated>{date.today().strftime("%Y-%m-%d")}T00:00:00Z</updated>\n')
        f.write('  <author>\n')
        f.write(f'    <name>{author}</name>\n')
        f.write('  </author>\n')
        for vars in pages_meta:
            if vars["published"] == '':
                continue
            f.write('    <entry>\n')
            f.write(f'      <title>{vars["title_raw"]}</title>\n')
            f.write(f'      <summary>{vars["description"]}</summary>\n')
            f.write(f'      <link rel="alternate" href="{vars["url"]}" />\n')
            f.write(f'      <updated>{vars["modified"]}T00:00:00Z</updated>\n')
            f.write(f'      <published>{vars["published"]}T00:00:00Z</published>\n')
            f.write(f'      <id>{vars["url"]}</id>\n')
            f.write('    </entry>\n')
        f.write('</feed>\n')
    print('Done!')
