import os

from s2ag_corpus.datasets import DATASETS
from s2ag_corpus.json_file_inserter import JsonFileInserter


def insert_dataset(dataset_name, datasets_dir, connection):
    """
    Inserts a given dataset into the database.

    The function assumes that the data for the dataset is located in
    a directory named after the dataset, inside the 'datasets_dir' directory.
    Each file can be plain text or gzipped.
    It creates a table suitable for the dataset, reads each file in the dataset's directory,
    inserts the file's content into the database, and finally indexes the table.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to be inserted. The exact name should be present the DATASETS dictionary.
    datasets_dir : str
        Path to the directory where dataset directories are located.
    connection : obj
        Connection object to interact with the database.

    Returns
    -------
    None
    """
    data_dir = f"{datasets_dir}/{dataset_name}"
    dataset = DATASETS[dataset_name]
    inserter = JsonFileInserter(dataset, connection)
    inserter.create_table()
    for source_file in sorted(os.listdir(data_dir)):
        full_path = f"{data_dir}/{source_file}"
        print(full_path)
        inserter.copy_json_to_table(full_path)
    inserter.index_table()