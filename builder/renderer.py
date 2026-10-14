from datetime import date
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
    site_name,
)
from builder.checks import check_internal_links
from builder.extensions import get_markdown_instance
from builder.feeds import generate_atom, generate_rss, generate_sitemap
from builder.log import BuildError, BuildLog, bold, dim

KNOWN_META_KEYS = {'title', 'description', 'tags', 'published', 'modified', 'template', 'length', 'related'}

# Pages served from a fixed file instead of a pretty /slug/ URL
SPECIAL_PATHS = {'index': '', '404': '404.html'}


def parse_date(value):
    return date.fromisoformat(value) if value else None


def format_date(d):
    return f'{d:%B} {d.day}, {d.year}' if d else None


def read_note(input_path, md, log):
    md.reset()
    html = md.convert(input_path.read_text(encoding='utf-8'))

    unknown_keys = md.Meta.keys() - KNOWN_META_KEYS
    if unknown_keys:
        log.warn(f'Unknown front matter in {input_path.name}: {", ".join(sorted(unknown_keys))}')

    meta = {key: values[0] for key, values in md.Meta.items()}
    slug = input_path.stem
    path = SPECIAL_PATHS.get(slug, f'{slug}/')
    published = parse_date(meta.get('published'))
    modified = parse_date(meta.get('modified'))

    return {
        'md_html': html,
        'slug': slug,
        'path': path,
        'template': meta.get('template', 'default'),
        'title': f'{meta["title"]} - {author}' if 'title' in meta else default_title,
        'title_raw': meta.get('title', ''),
        'description': meta.get('description', default_description),
        'tags': md.Meta.get('tags', []),
        'modified': modified,
        'modified_formatted': format_date(modified),
        'published': published,
        'published_formatted': format_date(published),
        'url': domain + path,
        'url_absolute': '/' + path,
        'length': meta.get('length', ''),
        'related': md.Meta.get('related', []),
    }


def render_notes(md, j2env, out_dir, log):
    blog_pages = [read_note(p, md, log) for p in sorted((NOTES_DIR / 'blog').rglob('*.md'))]
    meta_pages = [read_note(p, md, log) for p in sorted((NOTES_DIR / 'meta').rglob('*.md'))]
    posts = sorted(blog_pages, key=lambda p: p['published'] or date.min, reverse=True)
    pages = posts + meta_pages

    seen = set()
    for page in pages:
        if page['slug'] in seen:
            raise BuildError(f'Duplicate page slug: {page["slug"]}')
        seen.add(page['slug'])

    for page in pages:
        output_path = out_dir / page['path']
        if page['path'] == '' or page['path'].endswith('/'):
            output_path = output_path / 'index.html'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = j2env.get_template(f'{page["template"]}.html')
        output_path.write_text(template.render(page, page=page, posts=posts), encoding='utf-8')

    return pages, posts


def build(dev=False, verbose=True):
    log = BuildLog(verbose)
    if verbose:
        site = domain.removeprefix('https://').rstrip('/')
        print(f'{bold(site)} {dim("dev build" if dev else "production build")}', flush=True)

    # Build into a staging directory, then swap it in so out/ is never half-built
    staging_dir = OUT_DIR.with_name(OUT_DIR.name + '.tmp')
    old_dir = OUT_DIR.with_name(OUT_DIR.name + '.old')
    for d in (staging_dir, old_dir):
        if d.exists():
            shutil.rmtree(d)
    staging_dir.mkdir(parents=True)

    md = get_markdown_instance()
    j2env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    j2env.globals.update(site_name=site_name, domain=domain)

    try:
        with log.step('Pages') as step:
            pages, posts = render_notes(md, j2env, staging_dir, log)
            published_posts = [p for p in posts if p['published']]
            step.detail = f'{len(pages)} pages, {len(published_posts)} posts'

        with log.step('Feeds') as step:
            generate_sitemap([p for p in pages if p['slug'] != '404'], staging_dir)
            generate_rss(published_posts, staging_dir)
            generate_atom(published_posts, staging_dir)
            step.detail = 'sitemap, RSS, Atom'

        with log.step('Static assets') as step:
            if dev:
                # Link static/ instead of copying it, so rebuilds stay fast
                (staging_dir / 'static').symlink_to(STATIC_DIR, target_is_directory=True)
                step.detail = 'linked'
            else:
                shutil.copytree(STATIC_DIR, staging_dir / 'static')
                files = [f for f in STATIC_DIR.rglob('*') if f.is_file()]
                step.detail = f'{len(files)} files, {sum(f.stat().st_size for f in files) / 1e6:.1f} MB'
            root_files = [f for f in STATIC_ROOT_DIR.iterdir() if f.is_file()]
            for filepath in root_files:
                shutil.copy2(filepath, staging_dir / filepath.name)
            step.detail += f' + {len(root_files)} root files'

        with log.step('Links') as step:
            step.detail = f'{check_internal_links(staging_dir)} internal links OK'
    except Exception:
        shutil.rmtree(staging_dir)
        raise

    if OUT_DIR.exists():
        OUT_DIR.rename(old_dir)
    staging_dir.rename(OUT_DIR)
    if old_dir.exists():
        # rmtree removes the static/ symlink itself without following it
        shutil.rmtree(old_dir)

    log.done(f'Built {len(pages)} pages' + ('' if dev else f' {dim("→")} {OUT_DIR.relative_to(OUT_DIR.parent)}/'))
