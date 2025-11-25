# Helper makefile

HPP = $(wildcard cplusplus/*hpp) $(wildcard cplusplus/dp/*hpp)
CPP = $(wildcard cplusplus/*cpp) $(wildcard cplusplus/dp/*cpp)
PY = $(wildcard python/*) $(wildcard python/base/*) $(wildcard python/dp/*)
DEMOS = $(wildcard demos/*py)
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
	touch cplusplus
	@echo "Done"
	@echo "****************************************************************"

# Build Python package but don't deploy
.PHONY: build
build: build-local
build-local: $(HPP) $(CPP) $(PY) meson.build
	@echo "****************************************************************"
	@echo "Build Python package locally"
	rm -rf build
	@if [ $(shell uname) = "Windows_NT" ]; then \
		meson setup build --vsenv builddir ; \
	elif [ $(shell uname) = "Darwin" ]; then \
		meson setup build; \
	fi
# 	endif
	meson compile -C build
	@echo "Done"
	@echo "****************************************************************"

# Generate Doxygen docs/html/*
.PHONY: doc
doc: docs/html
docs/html: $(HPP) $(CPP) $(DEMOS) $(TESTS) meson.build pyproject.toml README.md
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

# Sync unittests branch with main
.PHONY: unittests
unittests:
	git checkout unittests
	git merge dev
	git push
	git checkout dev

# Clean-up
.PHONY: clean
clean:
	rm -rf build
	rm -rf docs/html