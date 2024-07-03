import os

from s2ag_corpus.datasets.dataset_definitions import DATASETS
from s2ag_corpus.datasets.json_file_inserter import JsonFileInserter
from s2ag_corpus.helpers.monitor import Monitor


def insert_dataset(dataset_name, datasets_dir, connection, monitor: Monitor):
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
        Name of the dataset to be inserted. The exact name should be present in the DATASETS dictionary.
    datasets_dir : str
        Path to the directory where dataset directories are located.
    connection : obj
        Connection object to interact with the database.

    Returns
    -------
    None
    :param monitor:
        an object that can be used for logging
    :return: None
    """
    data_dir = f"{datasets_dir}/{dataset_name}"
    dataset = DATASETS[dataset_name]
    inserter = JsonFileInserter(dataset, connection, monitor)
    inserter.create_table()
    for source_file in sorted(os.listdir(data_dir)):
        full_path = f"{data_dir}/{source_file}"
        monitor.debug(f"inserting {full_path}")
        inserter.copy_json_to_table(full_path)
    inserter.index_table()
