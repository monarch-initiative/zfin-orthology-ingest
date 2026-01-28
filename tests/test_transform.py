"""
Test file for the ZFIN orthology transform.

Uses Koza 2.x KozaRunner for testing transforms.
"""

import importlib.util
from pathlib import Path

import pytest
from koza.runner import KozaRunner, PassthroughWriter, load_transform

TRANSFORM_SCRIPT = Path(__file__).parent.parent / "src" / "transform.py"


def load_module_from_path(path: Path):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location("transform", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_transform(rows: list[dict]) -> list:
    """Run transform on test rows and return entities."""
    module = load_module_from_path(TRANSFORM_SCRIPT)
    hooks = load_transform(module)
    writer = PassthroughWriter()
    runner = KozaRunner(
        data=iter(rows),
        writer=writer,
        hooks=hooks,
        base_directory=TRANSFORM_SCRIPT.parent,
    )
    runner.run()
    return writer.data


class TestSinglePublication:
    """Tests for single publication rows."""

    @pytest.fixture
    def entities(self):
        row = {
            "zfin_gene": "ZFIN:ZDB-GENE-080513-4",
            "ortholog_gene": "HGNC:973",
            "evidence": "AA",
            "publications": "ZDB-PUB-030905-1",
        }
        return run_transform([row])

    def test_entity_count(self, entities):
        assert len(entities) == 1

    def test_association_fields(self, entities):
        association = entities[0]
        assert association.subject == "ZFIN:ZDB-GENE-080513-4"
        assert association.predicate == "biolink:orthologous_to"
        assert association.object == "HGNC:973"
        assert association.has_evidence == ["ECO:0000031"]
        assert association.publications == ["ZFIN:ZDB-PUB-030905-1"]
        assert association.primary_knowledge_source == "infores:zfin"
        assert association.aggregator_knowledge_source == ["infores:monarchinitiative"]


class TestMultiplePublications:
    """Tests for multiple publication rows."""

    @pytest.fixture
    def entities(self):
        row = {
            "zfin_gene": "ZFIN:ZDB-GENE-110510-1",
            "ortholog_gene": "HGNC:11795",
            "evidence": "AA",
            "publications": "ZDB-PUB-030905-1|ZDB-PUB-140530-4|ZDB-PUB-181103-13",
        }
        return run_transform([row])

    def test_entity_count(self, entities):
        assert len(entities) == 1

    def test_multiple_publications(self, entities):
        association = entities[0]
        assert association.publications == [
            "ZFIN:ZDB-PUB-030905-1",
            "ZFIN:ZDB-PUB-140530-4",
            "ZFIN:ZDB-PUB-181103-13",
        ]


class TestEvidenceCodes:
    """Tests for different evidence codes."""

    @pytest.mark.parametrize(
        "evidence_code,expected_eco",
        [
            ("AA", "ECO:0000031"),
            ("CE", "ECO:0001163"),
            ("CL", "ECO:0000354"),
            ("FC", "ECO:0006091"),
            ("NT", "ECO:0000032"),
            ("PT", "ECO:0007750"),
            ("OT", "ECO:0000352"),
        ],
    )
    def test_evidence_mapping(self, evidence_code, expected_eco):
        row = {
            "zfin_gene": "ZFIN:ZDB-GENE-000001-1",
            "ortholog_gene": "HGNC:1",
            "evidence": evidence_code,
            "publications": "ZDB-PUB-000001-1",
        }
        entities = run_transform([row])
        assert entities[0].has_evidence == [expected_eco]
