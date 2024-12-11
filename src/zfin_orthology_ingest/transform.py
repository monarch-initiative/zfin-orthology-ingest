import uuid  # For generating UUIDs for associations

from biolink_model.datamodel.pydanticmodel_v2 import AgentTypeEnum, GeneToGeneHomologyAssociation, KnowledgeLevelEnum
from koza.cli_utils import get_koza_app

koza_app = get_koza_app("zfin_orthologs")

# TODO: convert evidence codes to ECO
# AA = Amino acid sequence comparison
# CE = Coincident expression
# CL = Conserved map location
# FC = Functional complementation
# NT = Nucleotide sequence comparison
# PT = Phylogenetic tree
# OT = Other


while (row := koza_app.get_row()) is not None:

    publications = [f"ZFIN:{pub}" for pub in row["publications"].split("|")] if row["publications"] else None

    association = GeneToGeneHomologyAssociation(
        id=str(uuid.uuid1()),
        subject=row["zfin_gene"],
        predicate="biolink:orthologous_to",
        object=row["ortholog_gene"],
        # TODO: convert to ECO CURIE, values are AA, CL, CE, FC, NT, OT, PT 
        has_evidence=[row["evidence"]],
        publications=publications,
        knowledge_level=KnowledgeLevelEnum.knowledge_assertion,
        agent_type=AgentTypeEnum.manual_agent,
    )
    koza_app.write(association)
