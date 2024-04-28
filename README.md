This Python project imports the [Semantic Scholar Academic Graph Corpus]() into a PostgreSQL database.

It has been developed in a Linux environment, and I do not have the resources to support it under Wiindows or MacOS.

It is a personal project, and it has no official connection with the Allen Institute for AI.

The data that it downloads is subject to the [Semantic Scholar Academic Graph Licence]()

The code is under active development, and the APi may change.
The current version supports downloading and inserting complete datasets.

Future releases will support updating the database from the diffs created by the Semantic Scholar API. 

The datasets supported are:
- `abstracts`
- `authors`
- `citations`
- `paper-ids`
- `papers`
- `publication-venues` and 
- `tldrs`.



## Installation

### Summary:

1. Clone this repository into a directory of your choice.
2. Install the required Python packages.
2. Create a base directory for the files that the software will download fromm Semantic Scholar.
3. Obtain an API key for Semantic Scholar.
3. Create and populate a .env file in the root directory of the downloaded repository.
4. If necessary, install PostgreSQL.
5. Create a Postgres database to hold the production data.
6. If you plan on modifying or extending the code, create a database to hold test data,

#### Clone this repository into a directory of your choice

Within the directory, run

```shell
git clone https://github.com/romilly/s2ag-corpus.git
cd s2ag-corpus
```

**NB:** Much more to come, as fast as I can write it :)

Thanks to the Allen Institute for AI for making the Semantic Scholar data freely available.

You can find out more about the Semantic Scholar platform here:

- **Title**: The Semantic Scholar Open Data Platform
- **Authors**: Rodney Kinney, Chloe Anastasiades, Russell Authur, Iz Beltagy, Jonathan Bragg, Alexandra Buraczynski, Isabel Cachola, Stefan Candra, Yoganand Chandrasekhar, Arman Cohan, Miles Crawford, Doug Downey, Jason Dunkelberger, Oren Etzioni, Rob Evans, Sergey Feldman, Joseph Gorney, David Graham, Fangzhou Hu, Regan Huff, Daniel King, Sebastian Kohlmeier, Bailey Kuehl, Michael Langan, Daniel Lin, Haokun Liu, Kyle Lo, Jaron Lochner, Kelsey MacMillan, Tyler Murray, Chris Newell, Smita Rao, Shaurya Rohatgi, Paul Sayre, Zejiang Shen, Amanpreet Singh, Luca Soldaini, Shivashankar Subramanian, Amber Tanaka, Alex D. Wade, Linda Wagner, Lucy Lu Wang, Chris Wilhelm, Caroline Wu, Jiangjiang Yang, Angele Zamarron, Madeleine Van Zuylen, Daniel S. Weld
- **Publisher**: arXiv
- **Year**: 2023
- **DOI**: [10.48550/ARXIV.2301.10140](https://doi.org/10.48550/arxiv.2301.10140)
- **URL**: [arXiv Link](https://arxiv.org/abs/2301.10140)
