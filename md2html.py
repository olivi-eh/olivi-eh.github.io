import markdown
import jinja2
import os
from datetime import date, datetime

default_title = 'Olivier Bourgeois: Cloud and backend software developer'
default_description = 'Cloud and backend software developer based in Canada. Specializes in Golang, Kubernetes, and fostering delightful developer experiences.'
author = 'Olivier Bourgeois'
domain = 'https://olivi-eh.dev/'
md = markdown.Markdown(extensions=['meta', 'extra', 'smarty'])
j2env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

def get_url_from_filepath(filepath):
    path = filepath.replace(os.getcwd(), '').replace('/out/', '').replace('.html', '/')
    if path == 'index/':
        path = ''
    return domain + path

def format_date_str(date_str):
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()
        formatted_date = date_object.strftime("%B %d, %Y")
        return formatted_date
    except ValueError:
        return None

def process_note(input_filename, output_filename, pages_meta):
    with open(input_filename, 'r', encoding='utf-8') as f:
        text = f.read()
        html = md.convert(text)

    vars = {
        'md_html': html,
        'title': f'{md.Meta["title"][0]} - {author}' if 'title' in md.Meta else default_title,
        'title_raw': md.Meta.get('title', [''])[0],
        'description': md.Meta.get('description', [default_description])[0],
        'tags': md.Meta.get('tags', []),
        'modified': md.Meta.get('modified', [''])[0],
        'modified_formatted': format_date_str(md.Meta.get('modified', [''])[0]),
        'published': md.Meta.get('published', [''])[0],
        'published_formatted': format_date_str(md.Meta.get('published', [''])[0]),
        'url': get_url_from_filepath(output_filename),
        'url_absolute': get_url_from_filepath(output_filename).replace(domain, "/"),
        'length': md.Meta.get('length', [''])[0],
        'related': md.Meta.get('related', []),
        'pages_meta': pages_meta
    }

    template_name = md.Meta.get('template', ['default'])[0]
    template = j2env.get_template(f'{template_name}.html')
    html = template.render(vars)
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html)

    vars.pop('md_html')
    pages_meta.append(vars)

def process_notes():
    print('Rendering pages... ', end='', flush=True)

    pages_meta = []
    for dirpath, dirnames, filenames in os.walk('notes/blog/'):
        for filename in filenames:
            filepath_in = os.path.join(dirpath, filename)
            filepath_out = os.path.join(os.getcwd(), 'out', filename.replace('.md', '.html'))
            os.makedirs(os.path.dirname(filepath_out), exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta)
    pages_meta = sorted(pages_meta, key=lambda x: x["published"], reverse=True)

    for dirpath, dirnames, filenames in os.walk('notes/meta/'):
        for filename in filenames:
            filepath_in = os.path.join(dirpath, filename)
            filepath_out = os.path.join(os.getcwd(), 'out', filename.replace('.md', '.html'))
            os.makedirs(os.path.dirname(filepath_out), exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta)

    print('Done!')
    return pages_meta

def generate_sitemap(pages_meta):
    print('Generating sitemap... ', end='', flush=True)
    with open(os.path.join(os.getcwd(), 'out', 'sitemap.xml'), 'w', encoding='utf-8') as f:
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
    print('Generating RRS feed... ', end='', flush=True)
    with open(os.path.join(os.getcwd(), 'out', 'rss.xml'), 'w', encoding='utf-8') as f:
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
            f.write('    <item>\n')
            f.write(f'      <title>{vars["title"]}</title>\n')
            f.write(f'      <link>{vars["url"]}</link>\n')
            f.write(f'      <description>{vars["description"]}</description>\n')
            f.write(f'      <pubDate>{datetime.strptime(vars["published"], "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S EST")}</pubDate>\n')
            f.write(f'      <guid>{vars["url"]}</guid>\n')
            f.write('    </item>\n')
        f.write('  </channel>\n')
        f.write('</rss>\n')
    print('Done!')

def generate_atom(pages_meta):
    print('Generating Atom feed... ', end='', flush=True)
    with open(os.path.join(os.getcwd(), 'out', 'atom.xml'), 'w', encoding='utf-8') as f:
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
            f.write(f'      <title>{vars["title"]}</title>\n')
            f.write(f'      <summary>{vars["description"]}</summary>\n')
            f.write(f'      <link rel="alternate" href="{vars["url"]}" />\n')
            f.write(f'      <updated>{vars["modified"]}T00:00:00Z</updated>\n')
            f.write(f'      <published>{vars["published"]}T00:00:00Z</published>\n')
            f.write(f'      <id>{vars["url"]}</id>\n')
            f.write('    </entry>\n')
        f.write('</feed>\n')
    print('Done!')

if __name__ == '__main__':
    pages_meta = process_notes()
    generate_sitemap(pages_meta)
    generate_rss(pages_meta)
    generate_atom(pages_meta)
