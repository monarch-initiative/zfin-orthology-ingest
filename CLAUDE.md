# zfin-orthology-ingest

Koza ingest for ZFIN orthology data - transforms zebrafish ortholog relationships into Biolink KGX format.

## Project Structure

- `download.yaml` - Downloads ortholog files (fly, human, mouse) from ZFIN
- `src/transform.yaml` - Koza transform configuration
- `src/transform.py` - Transform logic for GeneToGeneHomologyAssociation
- `scripts/preprocess.py` - Preprocessing wrapper
- `scripts/preprocess.sql` - DuckDB SQL to merge ortholog files

## Key Commands

- `just run` - Full pipeline (download -> preprocess -> transform)
- `just download` - Download ortholog data from ZFIN
- `just preprocess` - Merge ortholog files into single TSV
- `just transform` - Run Koza transform
- `just test` - Run pytest

## Preprocessing

This ingest has a preprocessing step using DuckDB to merge three separate ortholog files (fly, human, mouse) into a unified TSV format with consistent columns:
- zfin_gene, ortholog_gene, evidence, publications

Run preprocessing with: `just preprocess` or `uv run python scripts/preprocess.py`
