# Helper makefile

HPP = $(wildcard src/*hpp) $(wildcard src/dp/*hpp)
CPP = $(wildcard src/*cpp) $(wildcard src/dp/*cpp)
PY = $(wildcard python/*) $(wildcard python/dp/*)
TESTS = $(wildcard test/*py)

# Build everything (Python package, docs) and deploy pkg
.PHONY: all
all: src doc

# Build and deploy Python package
src: $(HPP) $(CPP) $(PY) pyproject.toml meson.build
	@echo "****************************************************************"
	@echo "Build and deploy Python package"
	rm -rf build
	pip install .
	touch src
	@echo "Done"
	@echo "****************************************************************"

# Build Python package but don't deploy
.PHONY: local
local: build
build: $(HPP) $(CPP) $(PY) meson.build
	@echo "****************************************************************"
	@echo "Build Python package locally"
	rm -rf build
	meson setup build
	meson compile -C build
	@echo "Done"
	@echo "****************************************************************"

# Generate Doxygen docs/html/*
.PHONY: doc
doc: docs/html
docs/html: $(HPP) $(CPP) $(TESTS) meson.build pyproject.toml README.md
	@echo "****************************************************************"
	@echo "Build Doxygen documentation"
	doxygen Doxyfile
	touch docs
	touch docs/html
	@echo "Done"
	@echo "****************************************************************"

# Sync dev branch with main
.PHONY: dev
dev:
	git checkout main
	git pull
	git checkout dev
	git merge main
	git push

# Clean-up
.PHONY: clean
clean:
	rm -rf build
	rm -rf docs/html