from __future__ import absolute_import

from collections import defaultdict

import rdflib

from go_data import goa


def load_gene_terms(goa_path, go_owl_path):
    """
    Load GO information related to a certain gene annotation.

    A GO annotation file describes the GO terms related to each gene
    in a specific organism. For example, if you download
    "gene_association.goa_human" from UniProt, it will tell you that the gene
    "LCE6A" is associated with "GO:0031424".

    However, the annotation file only gives you a reference to a GO ID,
    so you need the entire GO ontology definition to get more detail
    about the associated GO term. A GO OWL file describes a GO ontology. 

    Given a path to a GO annotation file, and a path to a GO ontology file,
    this function loads the records from the annotation file, and the 
    GO term description from the ontology file.

    Note, currently this only loads the term description from the ontology.
    GO ontologies are complex, and this function is only loading a very
    minimum amount of data.
    """
    genes_terms = defaultdict(list)

    goa_records_by_gene = goa.load_by_name(goa_path)
    descriptions = load_term_descriptions(go_owl_path)

    for gene_ID, goa_record in goa_records_by_gene.items():
        description = descriptions[record.GO_ID]
        genes_terms[gene_ID].append((goa_record, description))
        
    return genes_terms


def load_term_descriptions(go_owl_path):
    """
    Given a path to a GO ontology file in OWL format, return a dictionary
    mapping GO term IDs to descriptions.
    """
    d = {}

    g = rdflib.Graph()
    result = g.parse(go_owl_path)

    namespace_uris = dict(g.namespaces())

    oboInOwl_ns = rdflib.Namespace(namespace_uris['oboInOwl'])

    for s, p, o in g.triples((None, rdflib.RDF.type, rdflib.OWL.Class)):
        IDs = list(g.triples((s, oboInOwl_ns.id, None)))
        if IDs:
            ID = IDs[0][2].value
            desc = list(g.triples((s, rdflib.RDFS.label, None)))[0][2].value
            d[ID] = desc
    return d
