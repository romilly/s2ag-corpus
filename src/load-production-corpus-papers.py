#!/usr/bin/env python
# coding: utf-8


import os
from dotenv import load_dotenv

from s2ag_corpus.import_dataset import insert_dataset
from s2ag_corpus.database_catalogue import production_connection


load_dotenv()
base_dir = os.getenv("BASE_DIR")


connection = production_connection()
release_id = os.getenv('RELEASE_ID')

datasets_dir = f"{base_dir}/{release_id}"
dataset_name = 'papers'

insert_dataset(dataset_name, datasets_dir, connection)

