#!/usr/bin/env bash
# Rebuild the setup handout from SETUP.md.
#
#   bash docs/build_setup_handout.sh
#
# Produces ASTR5820_Python_Setup.html, and ASTR5820_Python_Setup.pdf as well if
# wkhtmltopdf is installed. The HTML is the primary artifact; printing it from a
# browser (Cmd-P, "Save as PDF") gives a better result than wkhtmltopdf, since
# the stylesheet has a print block that swaps the dark code panels for light ones.
#
# Requires pandoc:
#   macOS:  brew install pandoc
#   optional, for the command-line PDF:  brew install wkhtmltopdf
#
# Run this whenever SETUP.md changes materially, then repost to Canvas -- the
# handout is a snapshot and will otherwise drift out of step with the repository.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="ASTR5820_Python_Setup"

# Insert the repository pointer, which belongs in the standalone handout but not
# in SETUP.md itself (where the reader is already in the repository).
python3 - << 'PY'
src = open('SETUP.md').read()
anchor = "in git, and never copy a constant from one script into another.\n"
addition = anchor + """
The repository is at <https://github.com/phayne/astr5820>. This document is also
in it as `SETUP.md`, where the commands can be copied rather than retyped.
"""
assert anchor in src, "anchor paragraph not found in SETUP.md"
open('/tmp/setup_handout.md', 'w').write(src.replace(anchor, addition, 1))
PY

pandoc /tmp/setup_handout.md -f gfm -t html5 --no-highlight -o /tmp/setup_body.html

# Single self-contained file: the stylesheet is inlined so the handout can be
# posted or emailed on its own.
python3 - << 'PY'
body = open('/tmp/setup_body.html').read()
css = open('docs/setup_style.css').read()
open('ASTR5820_Python_Setup.html', 'w').write(
    f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    f'<title>ASTR 5820: Python Setup</title>\n<style>\n{css}\n</style>\n'
    f'</head>\n<body>\n<main>\n{body}\n</main>\n</body>\n</html>\n'
)
PY
echo "wrote ${OUT}.html"

if command -v wkhtmltopdf > /dev/null 2>&1; then
  # wkhtmltopdf renders screen media, so the print rules in the stylesheet never
  # fire and the code panels would come out dark. Feed it a copy with the print
  # treatment forced on.
  python3 - << 'PY'
html = open('ASTR5820_Python_Setup.html').read()
override = """<style>
pre { background:#f6f5f0 !important; color:#1f1e1d !important;
      border:1px solid #e6e3da !important; }
pre::before { color:#6b6862 !important; }
h1 + p em { background:#f6f5f0 !important; }
a { color:#1f1e1d !important; border-bottom:none !important; }
body { background:#fff !important; padding:0 !important; }
</style>
</head>"""
open('/tmp/setup_print.html', 'w').write(html.replace('</head>', override, 1))
PY
  wkhtmltopdf --enable-local-file-access --page-size Letter \
    --margin-top 16mm --margin-bottom 16mm --margin-left 15mm --margin-right 15mm \
    /tmp/setup_print.html "${OUT}.pdf" 2> /dev/null
  echo "wrote ${OUT}.pdf"
else
  echo "wkhtmltopdf not found -- open ${OUT}.html and print to PDF instead"
fi
