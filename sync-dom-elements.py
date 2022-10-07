#!/usr/bin/env python3
"""
Sync the given DOM element (e.g. 'nav' or 'footer' from the main index.html page
to all sub-index.html pages.

Call:
    ./sync-dom-elements.py nav footer
"""
import glob
import os
import re
import sys


def main(elements):
    for element in elements:
        if element not in ['nav', 'footer']:
            sys.stderr.write(f'Error: Cannot replace invalid element dom "{element}". Exit.\n')
            sys.exit(1)

    for element in elements:
        pat = re.compile(f'(<{element}.+</{element}>)', flags=re.DOTALL)
        # The "site/index.html" is our reference, so read the dom element from there
        # and sync it with all other html files in the site-directory and below.

        fp = open(os.path.join('site', 'index.html'))
        html = fp.read()
        res = pat.search(html)
        element_content = res.group(1)

        for html_file in glob.glob('site/**/*.html', recursive=True):
            if html_file == 'site/index.html':
                # skip the reference file itself!
                continue
            print(f'Replacing <{element}> in {html_file}')
            fp = open(html_file)
            html = fp.read()
            new_html = pat.sub(element_content, html)
            fp = open(html_file, 'w')
            fp.write(new_html)
            fp.close()


if __name__ == '__main__':
    main(sys.argv[1:])
