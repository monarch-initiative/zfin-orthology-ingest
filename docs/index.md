# zfin-orthology-ingest Report

This transform pulls in Human, Fly and Mouse orthology files from ZFIN and produces a Biolink KGX representation of the orthology relationships, with the zebrafish gene always occupying the subject position. Due to genome duplication, Zebrafish orthology can be especially complex to establish, and this makes the manual curation of orthology relationships provdided by ZFIN especially valuable.

There are two awkard aspects to this transform with respect to Koza's limitations. The `human_orthos.txt` file has one more column than `fly_orthos.txt` and `mouse_orthos.txt`, additionally, these files have a single valued pulication field, but the Biolink model has a multivalued field. These two isses are addressed by a preprocessing SQL step that uses duckdb to normalize the columns and aggregate up to the publication. This step also adds gene prefixes for both the ZFIN gene and the ortholog, because the alternative (at least on the ortholog side) would have been to have bare integer IDs.  

The transform results in the associations listed below

{{ get_edges_report() }}
