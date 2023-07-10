NPX = npx
DEPLOYMENT_TARGET = MY_RSYNC_TARGET   # <---- replace this, e.g. "mu:web/open-gate.eu"

all:

dev-css: site/css/tailwind.css
prod-css: site/css/tailwind.min.css

site/css/tailwind.css: tailwind.config.js site/css/src/tailwind.css
	$(NPX) tailwindcss -i site/css/src/tailwind.css -o site/css/tailwind.css


site/css/tailwind.min.css: tailwind.config.js site/css/src/tailwind.css
	$(NPX) tailwindcss -i site/css/src/tailwind.css -o site/css/tailwind.min.css --minify


sync: prod-css
	rsync -a -v -P --exclude-from .rsync.exclude . $(DEPLOYMENT_TARGET)
	ssh mu 'cd $(DEPLOYMENT_DIR); make use-min-css'


watch-css:
	# Run this target while developing pages in the editor - creates required css on-the-fly
	$(NPX) tailwindcss -i site/css/src/tailwind.css -o site/css/tailwind.css --watch


clean:
	git clean -fdx -e .idea


use-min-css:
	# Run this target on the server via 'make sync' command above.
	find site -name '*.html' -exec sed -i 's/tailwind.css/tailwind.min.css/' {} \;
