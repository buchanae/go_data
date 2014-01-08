from collections import defaultdict
import logging

import rdflib


log = logging.getLogger(__name__)


class GODatabase(object):
    def __init__(self, goa_path, owl_path):
        self._goa_path = goa_path

        # Load GO ontology definition
        log.info('Loading ontology definition')
        self.graph = rdflib.Graph()
        self.graph.parse(owl_path)

        self.description_by_GO_ID = self._index_descriptions_by_GO_ID()
        self.description_by_gene_ID = self._index_descriptions_by_gene_ID()

    def _index_descriptions_by_GO_ID(self):
        """
        Returns a dictionary mapping GO term IDs to descriptions.
        """
        d = {}
        namespace_uris = dict(self.graph.namespaces())
        oboInOwl_ns = rdflib.Namespace(namespace_uris['oboInOwl'])

        query = None, rdflib.RDF.type, rdflib.OWL.Class
        for s, p, o in self.graph.triples(query):

            IDs_query = s, oboInOwl_ns.id, None
            IDs = list(g.triples(IDs_query))

            if IDs:
                ID = IDs[0][2].value
                description_query = s, rdflib.RDFS.label, None
                res = list(g.triples(description_query))
                d[ID] = res[0][2].value
        return d

    def _index_descriptions_by_gene_ID(self):
        """
        Returns a dictionary mapping gene IDs to GO term descriptions.
        """
        d = defaultdict(list)
        # Load GO human annotation
        goa = list(goa.reader(self._goa_path))

        for record in goa:
            gene_ID = record.DB_object_symbol
            GO_ID = record.GO_ID

            try:
                description = self.description_by_GO_ID[GO_ID]
                d[gene_ID].append(description)
            except KeyError:
                log.warning('Missing description for {}'.format(GO_ID))
        return d
