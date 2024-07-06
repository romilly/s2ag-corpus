# Automating database population and updates

I plan to automate the population of the database with the latest datasets and then determine
which diffs to download and apply. 

All files are downloaded into directories somewhere below `BASE_DIR` - the base directory
which is specified in the `.env` file.

When the first datasets are downloaded, a directory called `datasets` is created under `BASE_DIR`,
and a directory named by the release_id is created under that.

Example: if the initial release-id is dated 2024-06-18, the directory tree below the base directory
after the download will look like this:

```text
.
├── datasets
    └── 2024-06-18
        ├── abstracts
        │   ├── abstracts000.gz
        │   ├── ...
        │   └── abstracts059.gz
        ├── authors
        │   ├── authors000.gz
        │   ├── ...
        │   └── authors029.gz
        ├── citations
        │   ├── citations000.gz
        │   ├── ...
        │   └── citations217.gz
        ├── paper-ids
        │   ├── paper-ids000.gz
        │   ├── ...
        │   └── paper-ids029.gz
        ├── papers
        │   ├── papers000.gz
        │   ├── ...
        │   └── papers059.gz
        ├── publication-venues
        │   └── publication-venues000.gz
        └── tldrs
            ├── tldrs000.gz
            ├── ...
            └── tldrs029.gz
```

<div style="page-break-after: always;"></div>

After downloading the diff files that span 2024-06-18 to 2024-06-25, the tree would look like this:

```text
.
├── datasets
│   └── 2024-06-18
│       ├── abstracts
│       │   ├── abstracts000.gz
│       │   ├── ...
│       │   └── abstracts059.gz
│       ├── authors
│       │   ├── authors000.gz
│       │   ├── ...
│       │   └── authors029.gz
│       ├── citations
│       │   ├── citations000.gz
│       │   ├── ...
│       │   └── citations217.gz
│       ├── paper-ids
│       │   ├── paper-ids000.gz
│       │   ├── ...
│       │   └── paper-ids029.gz
│       ├── papers
│       │   ├── papers000.gz
│       │   ├── ...
│       │   └── papers059.gz
│       ├── publication-venues
│       │   └── publication-venues000.gz
│       └── tldrs
│           ├── tldrs000.gz
│           ├── ...
│           └── tldrs029.gz
└── diffs
    └── 2024-06-25
        ├── abstracts
        │   ├── delete_files-000.gz
        │   ├── ...
        │   ├── delete_files-003.gz
        │   ├── update_files-000.gz
        │   ├── ...
        │   └── update_files-024.gz
        ├── authors
        │   ├── ...
        ├── citations
        │   ├── ...
        ├── paper-ids
        │   ├── ...
        ├── papers
        │   ├── ...
        ├── publication-venues
        └── tldrs
```


The Synchronizer  class will work like this:

Its constructor will find the base directory by loading the BASE_DIR environment variable
which is defined in the `.env` file and save it in a field. It will also store some helper objects in fields.

It will perform appropriate downloads and database updates based on the contents of the base directory.

This wil be triggered by invoking s `synchronise` method.

If there is no `datasets` directory under the base directory it will 
1. create a datasets direcotry,
2. download the datasets, and
3. load the datasets into the database.

If there is a `datasets` directory, it will check for the existence of a diffs directory under the base directory.

It will find the id of the latest available release using a find_latest_release_id method.

If there is no `datasets` directory, it will
1. download the diffs that span the release_id of the original dataset download and the latest release_id, and
2. apply each set of diffs.

If there is a `datasets` directory, it will contain one or more subdirectories 
named after the release_id of the diffs within.

The Synchronizer will find the last release_id and
1. dowwload the diffs that span the last downloaded release_id and the latest release_id, and 
2. apply each set of diffs.


