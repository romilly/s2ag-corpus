#!/usr/bin/env python
# coding: utf-8

from s2ag_corpus.database.database_catalogue import DatabaseCatalogue, production_connection
from s2ag_corpus.citation_graphs.dot_writer import write_dot_file
# from s2ag_corpus.citation_graphs.new_dot_writer import write_dot_file


def generate_dot_file(sha: str,
                      dot_file: str,
                      influential=True,
                      show_labels=False):
    connection = production_connection()
    catalogue = DatabaseCatalogue(connection)

    id = catalogue.find_corpus_id_from(sha)
    enriched_links = catalogue.enriched_links(id, influential=influential)
    write_dot_file(enriched_links, dot_file, show_labels=show_labels)


