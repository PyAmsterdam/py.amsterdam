.DEFAULT_GOAL:=help
PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
NOW_CONFIG_FILE=$(BASEDIR)/now/now.json
CONFFILE=$(BASEDIR)/pelicanconf.py
CONF_PROD=$(BASEDIR)/conf_prod.py
CONF_PREVIEW=$(BASEDIR)/conf_preview.py
CONF_GH_PAGES=$(BASEDIR)/conf_gh_pages.py


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

.check-env-vars:
	@test $${NOW_TOKEN?Please set environment variable NOW_TOKEN}
	@test $${NOW_ORG_ID?Please set environment variable NOW_ORG_ID}
	@test $${NOW_PROJECT_ID?Please set environment variable NOW_PROJECT_ID}

.PHONY: help
help:	## This help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

html: ## Build html for localhost
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean: clean-nas
	@[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

serve-global:
ifdef SERVER
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b $(SERVER)
else
	$(PELICAN) -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b 0.0.0.0
endif

devserver:
ifdef PORT
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

livereload:
	invoke livereload

.PHONY: html help clean regenerate serve serve-global devserver publish

clean-nas:  ## Clean files duplicated by Synology DS
	@find . -type f -name "*_DiskStation_*" -exec rm {} \;

prod: clean
	@echo making prod
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONF_PROD) $(PELICANOPTS)
	#yarn now $(OUTPUTDIR) --prod --token=$(NOW_TOKEN) --local-config=$(NOW_CONFIG_FILE)

preview: .check-env-vars clean
	@echo making preview
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONF_PREVIEW) $(PELICANOPTS)
	# yarn now $(OUTPUTDIR) --token=$(NOW_TOKEN) --local-config=$(NOW_CONFIG_FILE)

github: .check-env-vars clean
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONF_GH_PAGES) $(PELICANOPTS)
	ghp-import -b gh-pages -m "In dev preview" $(OUTPUTDIR) -p