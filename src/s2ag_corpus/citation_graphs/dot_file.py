#!/usr/bin/env python
# coding: utf-8

from s2ag_corpus.database_catalogue import DatabaseCatalogue, production_connection
from s2ag_corpus.dot_writer import write_dot_file



def generate_dot_file(sha: str, dot_file: str):
    connection = production_connection()
    catalogue = DatabaseCatalogue(connection)

    id = catalogue.find_corpus_id_from(sha)
    catalogue.find_paper_details(id)
    enriched_links = catalogue.enriched_links(id)
    write_dot_file(enriched_links, dot_file)


