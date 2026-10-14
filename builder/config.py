from pathlib import Path
from zoneinfo import ZoneInfo

# Paths relative to repository root
ROOT_DIR = Path(__file__).parent.parent.resolve()
OUT_DIR = ROOT_DIR / 'out'
STATIC_DIR = ROOT_DIR / 'static'
STATIC_ROOT_DIR = ROOT_DIR / 'static-root'
NOTES_DIR = ROOT_DIR / 'notes'
TEMPLATES_DIR = ROOT_DIR / 'templates'

# Site Metadata Configuration
site_name = 'Olivier Bourgeois: Cloud and backend software developer'
default_title = site_name
default_description = 'Cloud and backend software developer based in Canada. Specializes in Golang, Kubernetes, and fostering delightful developer experiences.'
author = 'Olivier Bourgeois'
domain = 'https://olivi-eh.dev/'
language = 'en-ca'

# Timezone used to turn front matter dates into feed timestamps
timezone = ZoneInfo('America/Toronto')
