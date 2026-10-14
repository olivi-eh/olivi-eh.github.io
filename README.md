![GitHub branch check runs](https://img.shields.io/github/check-runs/olivi-eh/olivi-eh.github.io/main)
![GitHub License](https://img.shields.io/github/license/olivi-eh/olivi-eh.github.io)

# Personal website

Source for my personal website and blog, hosted at [olivi-eh.dev](https://olivi-eh.dev/). It's built by a small custom static site generator that renders Markdown notes through Jinja2 templates.

- **Markdown content:** pages and posts are plain Markdown files with front matter.
- **Pretty URLs:** every page is served from its own directory (`/about/` rather than `/about.html`).
- **Feeds:** RSS, Atom, and a sitemap are generated on every build.
- **Link checking:** the build fails if any page links to an internal page or asset that doesn't exist.
- **Dev server:** local preview with automatic rebuilds on save.

## Quick start

The only requirement is [uv](https://github.com/astral-sh/uv), which installs the right Python version (see `.python-version`) and dependencies on first run.

```sh
git clone https://github.com/olivi-eh/olivi-eh.github.io.git
cd olivi-eh.github.io
./dev.sh
```

The site is served at [http://localhost:8082](http://localhost:8082) and rebuilds whenever a file in `notes/`, `templates/`, `static/`, or `static-root/` changes.

To produce a one-time production build in `out/`:

```sh
uv run build.py
```

## Project layout

```
notes/
  blog/          Blog posts, served at /<filename>/ and listed in the feeds
  meta/          Standalone pages (index, about, now, 404, ...)
  wip/           Drafts and the post template; never built
templates/       Jinja2 templates (default, blog, blog-index, index)
static/          CSS, fonts, and images, served at /static/
static-root/     Files copied to the site root (CNAME, robots.txt)
builder/         The site generator
build.py         Entry point for builds and the dev server
optimize_images.py
out/             Build output (git ignored)
```

## Writing content

Each note starts with front matter, followed by a `---` line and the Markdown body:

```
title: My post title
description: One-line summary used in feeds and meta tags.
tags: first-tag
tags: second-tag
published: 2026-01-31
modified: 2026-01-31
template: blog
length: 5
---
```

| Key | Notes |
| --- | --- |
| `title` | Page title. Omit it to use the site's default title. |
| `description` | Used for meta tags and feeds. Defaults to the site description. |
| `tags` | Repeat the key once per tag. |
| `published` | `YYYY-MM-DD`. Posts without it are left out of the blog list and feeds. |
| `modified` | `YYYY-MM-DD`. Shown in the footer and used in the sitemap. |
| `template` | `default` (the default), `blog`, `blog-index`, or `index`. |
| `length` | Reading time in minutes. |
| `related` | Optional, repeatable. |

The build warns about any other key, which usually means a typo.

> [!IMPORTANT]
> Every file in `notes/blog/` is published on the next deploy, whatever its `published` date. Keep drafts in `notes/wip/` until they're ready. `notes/wip/!template.md` is a starting point for new posts.

### Markdown extras

On top of standard Markdown (with tables, fenced code, attribute lists, and admonitions):

- **Footnotes:** reference with `[^1]` or `[^*]`, and define at the start of a line with `[^1]: text`. Definitions render in place as small text rather than at the end of the page.
- **Shortcodes:** `{caption: text}` for an image caption and `{small: text}` for small text.
- **External links:** links to other sites and to PDFs open in a new tab automatically.
- **Images:** local images get `loading="lazy"` and their width and height added automatically.

### Adding images

Put images in `static/images/<post-name>/`, reference them as `/static/images/<post-name>/<file>`, then convert them before committing:

```sh
uv run optimize_images.py static/images/<post-name>/
```

This resizes each JPEG or PNG to at most 1600 px wide, converts it to WebP, strips all metadata (including GPS location), and updates references in `notes/`.

## Deployment

Every push to `main` runs [gh-pages-deploy.yaml](.github/workflows/gh-pages-deploy.yaml), which builds the site and deploys `out/` to GitHub Pages. In the repository settings, the Pages source must be set to **GitHub Actions**.
