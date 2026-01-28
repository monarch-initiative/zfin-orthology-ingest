# zfin-orthology-ingest

Transform of ZFIN's curated orthology data into Biolink compliant KGX format.

## Requirements

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

## Installation

```bash
uv sync
```

## Usage

Run the full pipeline (download, preprocess, transform):

```bash
just run
```

Or run individual steps:

```bash
just download    # Download ortholog files from ZFIN
just preprocess  # Merge files into unified TSV using DuckDB
just transform   # Run Koza transform
```

### Testing

```bash
just test
```

## Data Sources

This ingest downloads three ortholog files from ZFIN:
- `fly_orthos.txt` - Zebrafish to Drosophila orthologs
- `human_orthos.txt` - Zebrafish to Human orthologs
- `mouse_orthos.txt` - Zebrafish to Mouse orthologs

These are preprocessed with DuckDB to merge into a single unified format before transformation.

## Output

The transform produces GeneToGeneHomologyAssociation edges linking zebrafish genes to their orthologs in fly, human, and mouse.
