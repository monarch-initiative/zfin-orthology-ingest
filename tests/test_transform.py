"""
An example test file for the transform script.

It uses pytest fixtures to define the input data and the KozaRunner.
The test functions then test the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""

import pytest
from biolink_model.datamodel.pydanticmodel_v2 import GeneToGeneHomologyAssociation
from koza.io.writer.writer import KozaWriter
from koza.runner import KozaRunner, KozaTransformHooks
from zfin_orthology_ingest.transform import transform_record

class MockWriter(KozaWriter):
    def __init__(self):
        self.items = []

    def write(self, entities):
        self.items += entities

    def finalize(self):
        pass



@pytest.fixture
def single_pub_entities():
    writer = MockWriter()
    row = {
        "zfin_gene": "ZFIN:ZDB-GENE-080513-4",
        "ortholog_gene": "HGNC:973",
        "evidence": "AA",
        "publications": "ZDB-PUB-030905-1",
    }
    runner = KozaRunner(
        data=iter([row]),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items

@pytest.fixture
def multi_pub_entities():
    writer = MockWriter()
    row = {
        "zfin_gene": "ZFIN:ZDB-GENE-110510-1",
        "ortholog_gene": "HGNC:11795",
        "evidence": "AA",
        "publications": "ZDB-PUB-030905-1|ZDB-PUB-140530-4|ZDB-PUB-181103-13",
    }
    runner = KozaRunner(
        data=iter([row]),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items



# Test the output of the transform


def test_single_pub_entities(single_pub_entities):
    entities = single_pub_entities
    assert len(entities) == 1
    association = entities[0]
    assert association
    assert association.subject == "ZFIN:ZDB-GENE-080513-4"
    assert association.predicate == "biolink:orthologous_to"
    assert association.object == "HGNC:973"
    assert association.has_evidence == ["ECO:0000031"]
    assert association.publications == ["ZFIN:ZDB-PUB-030905-1"]
    assert association.primary_knowledge_source == "infores:zfin"
    assert association.aggregator_knowledge_source == ["infores:monarchinitiative"]

def test_multi_pub_entities(multi_pub_entities):
    entities = multi_pub_entities
    assert len(entities) == 1
    association = entities[0]
    assert association
    assert association.subject == "ZFIN:ZDB-GENE-110510-1"
    assert association.predicate == "biolink:orthologous_to"
    assert association.object == "HGNC:11795"
    assert association.has_evidence == ["ECO:0000031"]
    assert association.publications == ["ZFIN:ZDB-PUB-030905-1", "ZFIN:ZDB-PUB-140530-4", "ZFIN:ZDB-PUB-181103-13"]
    assert association.primary_knowledge_source == "infores:zfin"
    assert association.aggregator_knowledge_source == ["infores:monarchinitiative"]