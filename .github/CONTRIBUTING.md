# Contributing to this repository

Thank you for your interest in contributing to my personal website and blog! Since this is a personal project, contributions are generally limited to bug fixes for the static site generator, layout improvements, and typo corrections in my posts.

## How to contribute

### 1. Reporting issues
If you find a broken link, a layout bug, or a rendering issue, please open an issue on the GitHub repository detailing:
- The URL where the bug occurred.
- A description of the issue (and screenshot if applicable).
- Steps to reproduce it.

### 2. Submitting typo fixes or improvements
If you've spotted a typo or want to submit a layout bug fix:
1. Fork this repository.
2. Create a new branch (e.g., `git checkout -b fix/typo-on-about-page`).
3. Make your changes.
4. Open a Pull Request detailing the changes made.

---

## Development guide

### Prerequisites
Make sure you have [uv](https://github.com/astral-sh/uv) installed.

### Setup & Local testing
1. Clone your fork and navigate to the directory:
   ```sh
   git clone https://github.com/your-username/olivi-eh.github.io.git
   cd olivi-eh.github.io
   ```
2. Start the local development server:
   ```sh
   ./dev.sh
   ```
3. Open your browser and navigate to [http://localhost:8082](http://localhost:8082). The server will automatically reload and rebuild your pages as you make edits to files under `notes/`, `templates/`, and `static/`.

### Formatting and style
- Keep Markdown files clean and follow the front-matter templates.
- Write clear commit messages.
