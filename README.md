![GitHub branch check runs](https://img.shields.io/github/check-runs/bourgeoisor/bourgeoisor.github.io/main)
![GitHub License](https://img.shields.io/github/license/bourgeoisor/bourgeoisor.github.io)

# Personal website

This repository contains my personal website, which is hosted on [olivi-eh.dev](https://olivi-eh.dev/). It is powered by a custom static site generator script that renders Markdown documents using Jinja2 templates.

## Features

* **Markdown pages:** Write posts and pages in plain Markdown inside the `notes/` directory.
* **Pretty URLs:** Automatically formats outputs so that pages are served clean (e.g., `/about/` instead of `/about.html`).
* **Automated feeds:** Dynamically generates RSS (`rss.xml`), Atom (`atom.xml`), and Sitemap (`sitemap.xml`) files on every build.
* **Development mode:** Built-in development server with automatic file watching and rebuilds.

## Directory structure

* **`notes/`** — Source markdown files for the posts and pages.
* **`static/`** — Static assets like CSS, images, and fonts.
* **`templates/`** — Jinja2 HTML templates used to render the markdown pages.
* **`static-root/`** — Configuration files meant to live at the root of the site (e.g., `CNAME`, `robots.txt`, `404.html`).
* **`out/`** — The compiled web assets ready for deployment (git ignored).

## Development and building

This project utilizes the `uv` Python package manager to manage dependencies and execute tasks.

### Prerequisites

Make sure you have [uv](https://github.com/astral-sh/uv) installed.

### 1. Run the development server (with watcher)

To serve the website locally and watch for changes in `notes/`, `templates/`, and `static/` directories:

```sh
./dev.sh
```

This will automatically build the site, run a local development server at [http://localhost:8082](http://localhost:8082), and trigger automatic rebuilds as you edit the files.

### 2. Build the production site

If you just want to run a one-time build to compile the static files:

```sh
uv run build.py
```

This clean build will output all static assets directly into the `out/` directory.

## Deployment

Deployments are automated via GitHub Actions ([gh-pages-deploy.yaml](file:///.github/workflows/gh-pages-deploy.yaml)). Any push to the `main` branch compiles the site with Python 3.14 and pushes the output from the `out/` directory to the `gh-pages` branch.
