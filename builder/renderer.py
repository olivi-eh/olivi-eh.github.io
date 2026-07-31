from datetime import datetime
import shutil

import jinja2

from builder.config import (
    NOTES_DIR,
    OUT_DIR,
    STATIC_DIR,
    STATIC_ROOT_DIR,
    TEMPLATES_DIR,
    author,
    default_description,
    default_title,
    domain,
)
from builder.extensions import get_markdown_instance
from builder.feeds import generate_atom, generate_rss, generate_sitemap


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


def process_note(input_path, output_path, pages_meta, md, j2env):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
        md.reset()
        html = md.convert(text)

    template_name = md.Meta.get('template', ['default'])[0]

    vars_dict = {
        'md_html': html,
        'template': template_name,
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
        'pages_meta': pages_meta,
    }

    template = j2env.get_template(f'{template_name}.html')
    html_content = template.render(vars_dict)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    vars_dict.pop('md_html')
    pages_meta.append(vars_dict)


def process_notes(md, j2env):
    print('  ├── Rendering pages... ', end='', flush=True)

    pages_meta = []

    # Process blog notes
    blog_dir = NOTES_DIR / 'blog'
    if blog_dir.exists():
        for filepath_in in blog_dir.rglob('*.md'):
            filename = filepath_in.name
            filepath_out = OUT_DIR / filename.replace('.md', '.html')
            filepath_out.parent.mkdir(parents=True, exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta, md, j2env)

    # Sort blog pages by published date descending
    pages_meta = sorted(pages_meta, key=lambda x: x["published"], reverse=True)

    # Process meta notes
    meta_dir = NOTES_DIR / 'meta'
    if meta_dir.exists():
        for filepath_in in meta_dir.rglob('*.md'):
            filename = filepath_in.name
            filepath_out = OUT_DIR / filename.replace('.md', '.html')
            filepath_out.parent.mkdir(parents=True, exist_ok=True)
            process_note(filepath_in, filepath_out, pages_meta, md, j2env)

    print('Done!')
    return pages_meta


def build():
    # 1. Clean out/ directory
    if OUT_DIR.exists():
        print(f"  ├── Cleaning existing build directory... ", end="", flush=True)
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Done!", flush=True)

    # Initialize Markdown and Jinja environment
    md = get_markdown_instance()
    j2env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))

    # 2. Render all markdown pages and generate lists/feeds
    pages_meta = process_notes(md, j2env)
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
