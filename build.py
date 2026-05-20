import markdown
import jinja2
import shutil
import sys
import time
import http.server
import threading
from datetime import date, datetime
from pathlib import Path

# Paths relative to the script location
ROOT_DIR = Path(__file__).parent.resolve()
OUT_DIR = ROOT_DIR / 'out'
STATIC_DIR = ROOT_DIR / 'static'
STATIC_ROOT_DIR = ROOT_DIR / 'static-root'
NOTES_DIR = ROOT_DIR / 'notes'
TEMPLATES_DIR = ROOT_DIR / 'templates'

default_title = 'Olivier Bourgeois: Cloud and backend software developer'
default_description = 'Cloud and backend software developer based in Canada. Specializes in Golang, Kubernetes, and fostering delightful developer experiences.'
author = 'Olivier Bourgeois'
domain = 'https://olivi-eh.dev/'

md = markdown.Markdown(extensions=['meta', 'extra', 'smarty', 'admonition'])
j2env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))

def get_url_from_filepath(filepath):
    relative = filepath.relative_to(OUT_DIR)
    path_str = relative.as_posix().replace('.html', '/')
    if path_str == 'index/':
        path_str = ''
    return domain + path_str

def format_date_str(date_str):
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_object.strftime("%B %d, %Y")
    except ValueError:
        return None

def process_note(input_path, output_path, pages_meta):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
        md.reset()
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
        'url': get_url_from_filepath(output_path),
        'url_absolute': get_url_from_filepath(output_path).replace(domain, "/"),
        'length': md.Meta.get('length', [''])[0],
        'related': md.Meta.get('related', []),
        'pages_meta': pages_meta
    }

    template_name = md.Meta.get('template', ['default'])[0]
    template = j2env.get_template(f'{template_name}.html')
    html_content = template.render(vars)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    vars.pop('md_html')
    pages_meta.append(vars)

def process_notes():
    print('  ├── Rendering pages... ', end='', flush=True)

    pages_meta = []
    
    # Process blog notes
    blog_dir = NOTES_DIR / 'blog'
    if blog_dir.exists():
        for filepath_in in blog_dir.rglob('*.md'):
            filename = filepath_in.name
            filepath_out = OUT_DIR / filename.replace('.md', '.html')
            filepath_out.parent.mkdir(parents=True, exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta)
            
    # Sort blog pages by published date descending
    pages_meta = sorted(pages_meta, key=lambda x: x["published"], reverse=True)

    # Process meta notes
    meta_dir = NOTES_DIR / 'meta'
    if meta_dir.exists():
        for filepath_in in meta_dir.rglob('*.md'):
            filename = filepath_in.name
            filepath_out = OUT_DIR / filename.replace('.md', '.html')
            filepath_out.parent.mkdir(parents=True, exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta)

    print('Done!')
    return pages_meta

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
            f.write('    <item>\n')
            f.write(f'      <title>{vars["title_raw"]}</title>\n')
            f.write(f'      <link>{vars["url"]}</link>\n')
            f.write(f'      <description>{vars["description"]}</description>\n')
            f.write(f'      <pubDate>{datetime.strptime(vars["published"], "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S EST")}</pubDate>\n')
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

def build():
    # 1. Clean out/ directory
    if OUT_DIR.exists():
        print(f"  ├── Cleaning existing build directory... ", end="", flush=True)
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Done!", flush=True)

    # 2. Render all markdown pages and generate lists/feeds
    pages_meta = process_notes()
    generate_sitemap(pages_meta)
    generate_rss(pages_meta)
    generate_atom(pages_meta)

    # 3. Post-process HTML pages for clean/pretty URLs
    print("  ├── Post-processing HTML pages for clean URLs... ", end="", flush=True)
    for filepath in list(OUT_DIR.glob('*.html')):
        if filepath.name == 'index.html':
            continue
        
        folder_name = filepath.stem
        dest_dir = OUT_DIR / folder_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_file = dest_dir / 'index.html'
        filepath.rename(dest_file)
    print("Done!", flush=True)

    # 4. Copy static assets to out/static/
    if STATIC_DIR.exists():
        print("  ├── Copying static assets... ", end="", flush=True)
        shutil.copytree(STATIC_DIR, OUT_DIR / 'static', dirs_exist_ok=True)
        print("Done!", flush=True)

    # 5. Copy root level config/static files to out/
    print("  └── Copying root configuration files... ", end="", flush=True)
    if STATIC_ROOT_DIR.exists():
        for filepath in STATIC_ROOT_DIR.iterdir():
            if filepath.is_file():
                shutil.copy2(filepath, OUT_DIR / filepath.name)
    print("Done!", flush=True)

    print("🎉 Build completed successfully!", flush=True)

def get_max_mtime():
    paths_to_watch = [NOTES_DIR, TEMPLATES_DIR, STATIC_DIR, STATIC_ROOT_DIR]
    max_mtime = 0.0
    for path in paths_to_watch:
        if not path.exists():
            continue
        for p in path.rglob('*'):
            try:
                mtime = p.stat().st_mtime
                if mtime > max_mtime:
                    max_mtime = mtime
            except OSError:
                pass
                
    return max_mtime

def serve_directory(directory, port=8082):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, format, *args):
            # Suppress normal server logs to keep rebuild console clean
            pass

    server = http.server.ThreadingHTTPServer(('', port), Handler)
    server.socket.setsockopt(http.server.socket.SOL_SOCKET, http.server.socket.SO_REUSEADDR, 1)
    
    print(f"🚀 Local development server running at: http://localhost:{port}/", flush=True)
    try:
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}", flush=True)

def watch_and_serve():
    # Initial build before serving
    print("🛠️ Building...", flush=True)
    build()

    # Start the HTTP server in a daemon thread
    server_thread = threading.Thread(target=serve_directory, args=(OUT_DIR, 8082), daemon=True)
    server_thread.start()

    print("👀 Watching for changes in notes/, templates/, and static/...", flush=True)
    last_mtime = get_max_mtime()
    try:
        while True:
            time.sleep(1.0)
            current_mtime = get_max_mtime()
            if current_mtime > last_mtime:
                print("\n🛠️ Change detected! Rebuilding...", flush=True)
                try:
                    build()
                except Exception as e:
                    print(f"❌ Rebuild failed: {e}", flush=True)
                last_mtime = current_mtime
    except KeyboardInterrupt:
        print("\nStopping watch and server. Bye!", flush=True)

def main():
    if '--serve' in sys.argv or '--watch' in sys.argv:
        watch_and_serve()
    else:
        print("🛠️ Building...", flush=True)
        build()

if __name__ == '__main__':
    main()
