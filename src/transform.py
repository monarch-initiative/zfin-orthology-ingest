"""Transform ZFIN orthology data into Biolink GeneToGeneHomologyAssociation."""

import uuid

import koza
from biolink_model.datamodel.pydanticmodel_v2 import (
    AgentTypeEnum,
    GeneToGeneHomologyAssociation,
    KnowledgeLevelEnum,
)

# Mappings provided by Ceri Van Slyke from ZFIN, ORCID:0000-0002-2244-7917
EVIDENCE_MAP = {
    "AA": "ECO:0000031",  # Amino acid sequence comparison
    "CE": "ECO:0001163",  # Coincident expression
    "CL": "ECO:0000354",  # Conserved map location
    "FC": "ECO:0006091",  # Functional complementation
    "NT": "ECO:0000032",  # Nucleotide sequence comparison
    "PT": "ECO:0007750",  # Phylogenetic tree
    "OT": "ECO:0000352",  # Other evidence
}


@koza.transform_record()
def transform(koza_transform, row: dict):
    """Transform a row of ZFIN orthology data into a GeneToGeneHomologyAssociation."""
    publications = (
        [f"ZFIN:{pub}" for pub in row["publications"].split("|")]
        if row["publications"]
        else None
    )
    evidence = EVIDENCE_MAP.get(row["evidence"], None)

    association = GeneToGeneHomologyAssociation(
        id=str(uuid.uuid1()),
        subject=row["zfin_gene"],
        predicate="biolink:orthologous_to",
        object=row["ortholog_gene"],
        has_evidence=[evidence],
        publications=publications,
        primary_knowledge_source="infores:zfin",
        aggregator_knowledge_source=["infores:monarchinitiative"],
        knowledge_level=KnowledgeLevelEnum.knowledge_assertion,
        agent_type=AgentTypeEnum.manual_agent,
    )
    return [association]
