This Python project imports the [Semantic Scholar Academic Graph Corpus]() into a PostgreSQL database.

WARNING: **I'm getting strange behaviour running the new code in production.**

Do not install or use this release until further notice!

It has been developed in a Linux environment, and I do not have the resources to support it under Windows or MacOS.

It is a personal project, and it has no official connection with the Allen Institute for AI.

The data that it downloads is subject to the Semantic Scholar Academic Graph Licence.

The first iteration is almost complete, but the documentation needs more work.

The code is under active development, and the API may change.

I have just added the code that updates the database from the
diffs created by the Semantic Scholar API.

As a result, the API and setup have changed.


## Changes to running the application

You no longer need to add a release id to .env, and you no longer need to run individual scripts
to load downloaded datasets into the database.

I have described [the first batch of test data](diff-test-data.md) 

Later I will investigate the idea of
providing the application via docker. 


The datasets supported are:
- `abstracts`
- `authors`
- `citations`
- `paper-ids`
- `papers`
- `publication-venues` and 
- `tldrs`

The first dataset release in which a duplicated data anomaly was fixed is the `2024-06-18` release.

The project contains the code that I use to download a dataset release, 
load the data into Postgres, and aply subsequent diffs.

It also contains experimental code to explore
references and citations and present them graphically.

The first example shows a relatively simple citation graph.

![Example 1](notebooks/citations/martyn.svg)

The second shows a much more complex graph.

![Example 2](notebooks/citations/jonathan.svg)

## Installation

### Summary:

1.  Clone this repository into a directory of your choice.
2.  Create and activate a Python virtual environment.
3.  Install the required Python packages.
4.  Create a base directory for the files that the software will download from Semantic Scholar.
5.  Get an API key for Semantic Scholar.
6.  Create and populate a `.env` file in the root directory of the downloaded repository.
7.  If necessary, install PostgreSQL.
8.  Create a Postgres database to hold the production data.
9.  If you plan on modifying or extending the code, create a database to hold test data.
10. Update the .env file to include credentials for the database(s).
11. Run synchronise.py
12. Query the database. 


#### Clone this repository into a directory of your choice.

Within the directory, run

```shell
git clone https://github.com/romilly/s2ag-corpus.git
cd s2ag-corpus
```

#### Create and activate a Python virtual environment.

```shell
python -m venv venv
```

#### Install the required Python packages.

```shell
pip install -r requirements.txt
```

#### Create a base directory for the files that the software will download fromm Semantic Scholar.

You'll need at least 1 TB to allow for the initial downloads and future diffs. 

```shell
mdkir <path-to-your-data-directory>
```

#### Get an API key for Semantic Scholar.

See [Do I need an API key](https://www.semanticscholar.org/product/api#api-key) on the  Semantic Scholar website.

You *will* need a key to download the datasets you'll need.

#### Create and populate a `.env` file in the root directory of the downloaded repository.

The code in this repository assumes that you have created a `.env` file in the root directory of the project.
This will contain various credentials.

You'll need the private Semantic Scholar API key that you got in the previous step. 

The initial contents of the `.env` file should look like this:

```text
BASE_DIR = path-to-your-data-directory
S2_API_KEY = api-key-from-semantic-scholar
```

#### If necessary, install PostgreSQL.

You should be able to find installation instructions for your flavour of Linux on the internet.
Make sure that you install `postgres` and `postgresql-contrib`.

#### Create a Postgres database to hold the production data.

You'll need to create a database to hold the data.

Again, you'll need a lot of room on the volume that contains the database.

That may mean that you need to create the database with a tablespace on a volume that's not the default.
Consult the Postgres documentation for how to do this.

I'm running the application on a Raspberry Pi 5 computer, using a dedicated 4 TB nvme drive for downloaded data
and the database tablespace. That works well.

#### If you plan on modifying or extending the code, create a database to hold test data.

This needs much less space: 250 GB should be ample.

Running automated tests needs its own README, and will get one _real soon now_(tm).

#### Update the .env file to include credentials for the database(s).

You'll need to add one or two rows to the `.env` file that you created earlier.

The first row contains login credentials for the production database.
The second row should contain credentials for the test database if you are using one.

Here are example entries:

```text
BASE_DIR = path-to-your-data-directory
S2_API_KEY = api-key-from-semantic-scholar
PROD_DB = "postgres://romilly:semantic@pi5-postgres/ss_corpus"
TEST_DB = "postgres://romilly:semantic@pi5-postgres/corpus_test"
```
In the entries for the production database, `romilly` is the Postgres username who owns the database.
You should replace that by the name of the Postgres user who owns the database that you set up earlier.
`semantic` is the password for the database. gain, replace that with the password for the database that you created.
`pi5-postgres` is the hostname where your Postgres server is installed.
If you are running the software on the same computer, you can replace that by `localhost`
`ss-corpus` is the name of the database. Replace it by the name of the database that you create earlier.

The entry for the optional test database follows a similar format.

#### Synchronize the database with the Semnatic Scholar repository.

Change directory to the `src` directory for the project and run `synchronise.py`.

You'll need to run it using python.
For some Linux distributions you may need to replace `python` by `python3` in the entries below.

```shell
cd src
python synchronise.py
```

This will take some time to run, depending on the speed of your computer and your internet connection.

On the first run, it's going to download about a terabyte of data and then do a series of
very large inserts into the database. There are over 220 Million papers, and over 2.6 Billion citations.

On the [hardware that I use](Hardware.md) for production, the process takes over a day to complete.

You can follow progress by tailing the log dile in the `logs` directory.

#### Query the database

If you know a paper's sha or corpus_id, it takes milliseconds to query the database for the paper,
its references and citations.

Querying a title or abstract would be very slow. 
It would also be very slow to search for all the papers by a given author.

I may add code to do those queries via the web API.

You'll find some example code in the notebooks and tests.

The notebook that I find most useful is the `citations.ipynb` notebook.

To use it, you'll need to know the `sha` for the paper you're interested in.

You can find that using the Semantic Scholar web interface.

![](img/citations-eg.png)

In that example, the sha is at the end of the URL: ìt's `a2266a06e752df98615787746599dc81440c0ae1`.

Enter the `sha` in the line that starts `sha = 'paper of interest'`,
and then specify the name you want to use for the generated dot file and svg.
Don't add the dot or svg extension as these are added by the notebook.
The files will be created in the citations subdirectory of the notebooks directory.

Now run the notebook.

You can open the generated svg file in a browser. Hover over a node to see the details of the paper,
or click on the node to open Semantic Scholar on the page for that paper.

## Thanks

Thanks to the Allen Institute for AI for making the Semantic Scholar data freely available.

You can find out more about the Semantic Scholar platform here:

- **Title**: The Semantic Scholar Open Data Platform
- **Authors**: Rodney Kinney, Chloe Anastasiades, Russell Authur, Iz Beltagy, Jonathan Bragg, Alexandra Buraczynski, Isabel Cachola, Stefan Candra, Yoganand Chandrasekhar, Arman Cohan, Miles Crawford, Doug Downey, Jason Dunkelberger, Oren Etzioni, Rob Evans, Sergey Feldman, Joseph Gorney, David Graham, Fangzhou Hu, Regan Huff, Daniel King, Sebastian Kohlmeier, Bailey Kuehl, Michael Langan, Daniel Lin, Haokun Liu, Kyle Lo, Jaron Lochner, Kelsey MacMillan, Tyler Murray, Chris Newell, Smita Rao, Shaurya Rohatgi, Paul Sayre, Zejiang Shen, Amanpreet Singh, Luca Soldaini, Shivashankar Subramanian, Amber Tanaka, Alex D. Wade, Linda Wagner, Lucy Lu Wang, Chris Wilhelm, Caroline Wu, Jiangjiang Yang, Angele Zamarron, Madeleine Van Zuylen, Daniel S. Weld
- **Publisher**: arXiv
- **Year**: 2023
- **DOI**: [10.48550/ARXIV.2301.10140](https://doi.org/10.48550/arxiv.2301.10140)
- **URL**: [arXiv Link](https://arxiv.org/abs/2301.10140)
