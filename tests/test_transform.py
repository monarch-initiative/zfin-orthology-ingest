"""
An example test file for the transform script.

It uses pytest fixtures to define the input data and the mock koza transform.
The test_example function then tests the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""

import pytest
from koza.utils.testing_utils import mock_koza

# Define the ingest name and transform script path
INGEST_NAME = "zfin_orthology"
TRANSFORM_SCRIPT = "./src/zfin_orthology_ingest/transform.py"


@pytest.fixture
def single_pub_entities(mock_koza):
    row = {
        "zfin_gene": "ZFIN:ZDB-GENE-080513-4",
        "ortholog_gene": "HGNC:973",
        "evidence": "AA",
        "publications": "ZDB-PUB-030905-1",
    }

    return mock_koza(INGEST_NAME, row, TRANSFORM_SCRIPT)

@pytest.fixture
def multi_pub_entities(mock_koza):
    row = {
        "zfin_gene": "ZFIN:ZDB-GENE-110510-1",
        "ortholog_gene": "HGNC:11795",
        "evidence": "AA",
        "publications": "ZDB-PUB-030905-1|ZDB-PUB-140530-4|ZDB-PUB-181103-13",
    }

    return mock_koza(INGEST_NAME, row, TRANSFORM_SCRIPT)



# Test the output of the transform


def test_single_pub_entities(single_pub_entities):
    entities = single_pub_entities
    assert len(entities) == 1
    association = entities[0]
    assert association
    assert association.subject == "ZFIN:ZDB-GENE-080513-4"
    assert association.predicate == "biolink:orthologous_to"
    assert association.object == "HGNC:973"
    assert association.has_evidence == ["Amino acid sequence comparison"]
    assert association.publications == ["ZFIN:ZDB-PUB-030905-1"]

def test_multi_pub_entities(multi_pub_entities):
    entities = multi_pub_entities
    assert len(entities) == 1
    association = entities[0]
    assert association
    assert association.subject == "ZFIN:ZDB-GENE-110510-1"
    assert association.predicate == "biolink:orthologous_to"
    assert association.object == "HGNC:11795"
    assert association.has_evidence == ["Amino acid sequence comparison"]
    assert association.publications == ["ZFIN:ZDB-PUB-030905-1", "ZFIN:ZDB-PUB-140530-4", "ZFIN:ZDB-PUB-181103-13"]