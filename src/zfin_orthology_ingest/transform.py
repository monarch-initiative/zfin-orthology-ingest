import uuid  # For generating UUIDs for associations

from biolink_model.datamodel.pydanticmodel_v2 import AgentTypeEnum, GeneToGeneHomologyAssociation, KnowledgeLevelEnum
from koza.cli_utils import get_koza_app

koza_app = get_koza_app("zfin_orthology")

# Mappings provided by Ceri Van Slyke from ZFIN, ORCID:0000-0002-2244-7917
evidence_map = {
    "AA": "ECO:0000031", # Amino acid sequence comparison to protein BLAST evidence used in manual assertion
    "CE": "ECO:0001163", # Coincident expression to co-localization evidence used in manual assertion
    "CL": "ECO:0000354", # Conserved map location to gene neighbors evidence used in manual assertion
    "FC": "ECO:0006091", # Functional complementation to
    "NT": "ECO:0000032", # Nucleotide sequence comparison to  functional complementation evidence used in manual assertion
    "PT": "ECO:0007750", # Phylogenetic tree to phylogenetic evidence used in manual assertion
    "OT": "ECO:0000352", # Other to evidence used in manual assertion
}

while (row := koza_app.get_row()) is not None:

    publications = [f"ZFIN:{pub}" for pub in row["publications"].split("|")] if row["publications"] else None
    evidence = evidence_map.get(row["evidence"], None)
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
    koza_app.write(association)
