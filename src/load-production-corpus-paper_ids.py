#!/usr/bin/env python
# coding: utf-8


import os
from dotenv import load_dotenv

from s2ag_corpus.import_dataset import insert_dataset
from s2ag_corpus.database_catalogue import production_connection

# TODO: refactor to move most of the code into insert_dataset
# This and the other loaders should just supply the dataset name and connection, with the release_id coming from .env
# TODO: expand installation instructions to cover choosing a release and updating .env
load_dotenv()
base_dir = os.getenv("BASE_DIR")


connection = production_connection()
release_id = os.getenv('RELEASE_ID')

datasets_dir = f"{base_dir}/{release_id}"
dataset_name = 'paper-ids'

insert_dataset(dataset_name, datasets_dir, connection)

