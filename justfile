# zfin-orthology-ingest justfile

# Default recipe
default:
    @just --list

# Install dependencies
install:
    uv sync

# Download source data
download: install
    uv run downloader download.yaml

# Run preprocessing (merge ortholog files with duckdb)
preprocess:
    uv run python scripts/preprocess.py

# Run transform
transform:
    koza transform --source src/transform.yaml --output-format tsv

# Full pipeline: download, preprocess, transform
run: download preprocess transform

# Run tests
test:
    uv run pytest tests/

# Clean output and data directories
clean:
    rm -rf output/ data/
