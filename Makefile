# Helper makefile

HPP = $(wildcard cplusplus/*hpp) $(wildcard cplusplus/dp/*hpp)
CPP = $(wildcard cplusplus/*cpp) $(wildcard cplusplus/dp/*cpp)
PY = $(wildcard python/*) $(wildcard python/base/*) $(wildcard python/dp/*)
TESTS = $(wildcard tests/*py)

# Build everything (Python package, docs) and deploy pkg
.PHONY: all
all: install doc

# Build and deploy Python package
install: $(HPP) $(CPP) $(PY) pyproject.toml meson.build
	@echo "****************************************************************"
	@echo "Build and deploy Python package"
	rm -rf build
	uv pip install .
	touch src
	@echo "Done"
	@echo "****************************************************************"

# Build Python package but don't deploy
.PHONY: build
build: build-local
build-local: $(HPP) $(CPP) $(PY) meson.build
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