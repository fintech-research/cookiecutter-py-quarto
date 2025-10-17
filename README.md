# cookiecutter-py-quarto

---

[![Python version](https://img.shields.io/badge/python-3.13-blue?labelColor=grey&color=blue)](https://github.com/fintech-research/cookiecutter-py-quarto/blob/main/pyproject.toml)
[![License](https://img.shields.io/github/license/fintech-research/cookiecutter-py-quarto)](https://img.shields.io/github/license/fintech-research/cookiecutter-py-quarto)
[![style](https://img.shields.io/badge/style-ruff-ff69b4?labelColor=grey&color=ff69b4)](https://github.com/astral-sh/ruff)

**WARNING**: This template is under active development and is not quite ready for use yet. Use it at your own risk.

This is a modern Cookiecutter template that can be used to initiate a research project that uses Python and Quarto.

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter gh:fintech-research/cookiecutter-py-quarto
```

or if you don't have [`uv`](https://docs.astral.sh/uv/) installed yet (you should really consider installing it):

```bash
pip install cookiecutter
cookiecutter cookiecutter gh:fintech-research/cookiecutter-py-quarto
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## Overview

Cookiecutter template for research projects that use Python and Quarto. This template is _very_ opinionated, and is meant to be a good starting point for empirical research projects in Python with companion papers and presentations written in Quarto. It tailored for our research group's workflow; feel free to use it as is, or fork it and adapt it to your own needs.

Python project with all the necessary tools for development, testing, and deployment. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- python-dotenv for environment variable management
- [just](https://github.com/casey/just) task runner
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/astral-sh/ruff) and [ty](https://docs.astral.sh/ty/)
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [pytest-cov](https://github.com/pytest-dev/pytest-cov)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Containerization with [Docker](https://www.docker.com/) or [Podman](https://podman.io/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Hydra](https://hydra.cc/) for managing complex configurations and building processing pipelines
- [Claude Code](https://claude.ai/) and GitHub Copilot integration for AI-assisted coding
- Quarto, LaTex + template for paper and slides
- Template README.md with setup instructions that are not managed by cookiecutter
- Initial project structure with src, tests, notebooks, data (raw, clean, results), outputs, docs, notes, paper, slides
- Script for project setup (runs `uv add` and `uv sync` for base dependencies, sets up pre-commit, etc)
- Brewfile for macOS users to install all necessary dependencies with `brew bundle`

## Comparison with `cookiecutter-uv`

`cookiecutter-py-quarto` is based on the [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) template, and is meant to be a good starting point for data science and machine learning projects that use Python and Quarto. If you are looking for a more general Python project template for libraries that you aim to publish on PyPI, you should use [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).

Features that are specific to `cookiecutter-py-quarto`:

- Quarto and TeX/LaTeX for document preparation
- Hydra-based processing pipeline
- Claude Code integration for AI-assisted coding
- python-dotenv for environment variable management
- Boilerplate code for research data management
- [just](https://github.com/casey/just) for task automation (instead of Makefile)
- Additional tools in the devcontainer: lazygit, gh, jq, duckdb

Features in `cookiecutter-uv` that are not in `cookiecutter-py-quarto`:

- Supports both [src and flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/). _cookiecutter-py-quarto_ only supports the src layout.
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub. _cookiecutter-py-quarto_ does not include any specific configuration for publishing to PyPI.
- Test coverage reporting to [codecov](https://codecov.io/). _cookiecutter-py-quarto_ does not include any specific configuration for code coverage reporting, it only includes [pytest-cov](https://github.com/pytest-dev/pytest-cov).
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Code quality with [deptry](https://github.com/fpgmaas/deptry/) (important rules are covered by ruff and ty).

---

## Acknowledgements

This project is based on [Florian Maas\'s](https://github.com/fpgmaas)\'s
[cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv)
repository, which in turn is partially based on [Audrey Feldroy's](https://github.com/audreyfeldroy) great [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage).

## Directory Structure

```
.
├── .claude/
├── .devcontainer/
├── .env-example
├── .github/
├── .gitignore
├── .python-version
├── conf
│   └── config.yaml
├── docs/
├── justfile
├── LICENSE
├── mkdocs.yml
├── notebooks/
├── notes/
├── paper/
├── pyproject.toml
├── outputs/ *
├── README.md
├── slides/
├── src
│   └── {{ cookiecutter.project_slug }}
│       ├── __init__.py
│       ├── __main__.py
│       ├── data/
│       ├── figures/
│       ├── pipeline.py
│       ├── tables/
│       └── utils/
├── tests
│   └── __init__.py
└── uv.lock
```

- The `outputs/` directory is created when running the pipeline for the first time.

### Data

The data directory (defined in the `DATA_DIR` environment variable, default `data/`) is structured as follows:

```
.
├── data
│   ├── clean/
│   ├── preprocessing-cache/
│   ├── raw
│   │   ├── download-cache/
│   │   ├── open/
│   │   └── restricted/
│   └── results/
```

### Results

The results directory (defined in the `RESULTS_DIR` environment variable, default `results/`) is structured as follows:

```
.
├── results/
│   ├── figures/
│   ├── tables/
│   └── text/
```

### Resources

There is also a resources directory (defined in the `RESOURCES_DIR` environment variable, default `resources/`) that can be used to store shared resources, such as fonts. We do not have a specific structure for this directory, as it will depend on the project.
