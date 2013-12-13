'''
Quick-and-dirty utility for reading UniProt-GOA files.

GOA files describe the relationships between genes and Gene Ontology terms.

ftp://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/idmapping/README
'''
# TODO perhaps this isn't necessarily UniProt-GOA specific
#      and is possible of reading GAF-2.0 format in general.

from collections import defaultdict, namedtuple


GoaRecord = namedtuple('GoaRecord', '''
    DB
    DB_object_ID
    DB_object_symbol
    qualifier
    GO_ID
    DB_reference
    evidence_code
    with_from
    aspect
    DB_object_name
    DB_object_synonym
    DB_object_type
    taxon
    date
    assigned_by
    annotation_extension
    gene_product_form_ID''')


def reader(fh):
    '''
    Read a UniProt-GOA file (GAF v2.0 format).
    
    Given a UniProt-GOA file, generate GoaRecords.
    '''

    for line in fh:
        if not line.startswith('!'):
            sp = line.strip().split('\t')

            # We're expecting 17 columns, but some are optional,
            # so pad the list if we're missing some.
            sp += (17 - len(sp)) * ['']

            yield GoaRecord(*sp)


def load_by_name(fh):
    '''
    Given a UniProt-GOA file,
    return a defaultdict(list) mapping gene names to GOA records.
    '''
    by_name = defaultdict(list)

    for rec in reader(fh):
        by_name[rec.DB_object_symbol].append(rec)

    return by_name
