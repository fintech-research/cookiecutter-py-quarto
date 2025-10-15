set shell := ["zsh", "-lc"]
set default := "help"

# bake without inputs and overwrite if exists.
bake:
    uv run cookiecutter --no-input . --overwrite-if-exists

# bake without inputs and overwrite if exists (src layout)
bake-src:
    uv run cookiecutter --no-input . --overwrite-if-exists layout="src"

# bake with inputs and overwrite if exists.
bake-with-inputs:
    uv run cookiecutter . --overwrite-if-exists

# For quick publishing to cookiecutter-py-quarto-example to test GH Actions
bake-and-test-deploy:
    rm -rf cookiecutter-py-quarto-example || true
    uv run cookiecutter --no-input . --overwrite-if-exists \
        author="Vincent Grégoire" \
        email="vincent.gregoire@gmail.com" \
        github_author_handle=vgreg \
        project_name=cookiecutter-py-quarto-example \
        project_slug=cookiecutter_py_quarto_example
    cd cookiecutter-py-quarto-example; uv sync && \
        git init -b main && \
        git add . && \
        uv run pre-commit install && \
        uv run pre-commit run -a || true && \
        git add . && \
        uv run pre-commit run -a || true && \
        git add . && \
        git commit -m "init commit" && \
        git remote add origin git@github.com:fintech-research/cookiecutter-py-quarto-example.git && \
        git push -f origin main

# Install the virtual environment
install:
    echo "🚀 Creating virtual environment"
    uv sync

# Run code quality tools.
check:
    echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    uv lock --locked
    echo "🚀 Linting code: Running pre-commit"
    uv run pre-commit run -a
    echo "🚀 Static type checking: Running ty"
    uv run ty
    echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Test the code with pytest.
test:
    echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml tests

# Clean build artifacts
clean-build:
    echo "🚀 Removing build artifacts"
    uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

# Build wheel file (depends on clean-build)
build: clean-build
    echo "🚀 Creating wheel file"
    uvx --from build pyproject-build --installer uv

# Publish a release to PyPI.
publish:
    echo "🚀 Publishing: Dry run."
    uvx --from build pyproject-build --installer uv
    echo "🚀 Publishing."
    uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

build-and-publish: build publish

# Test if documentation can be built without warnings or errors
docs-test:
    uv run mkdocs build -s

# Build and serve the documentation
docs:
    uv run mkdocs serve

# Show available recipes and their short descriptions
help:
    just --summary
