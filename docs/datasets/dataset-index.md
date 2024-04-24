# Semanctic Scholar AG Datasets

as of 2024-04-02

NB: All the sizes and numbers for files are approximate, and the citations dataset consists of many more smaller files.

I have built some JSON schemas for the datasets from sample data. Use with caution. 

## abstracts

#### DESCRIPTION
Paper abstract text, where available.  
100M records in 30 1.8GB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "abstracts" dataset provides abstract text for selected papers.  
  
#### SCHEMA  
 - `corpusid`: The paper's primary key
 - `openAccessInfo`:  
   - `externalIds`: IDs of this paper in different catalogs  
   - `license`: terms under which the paper is licensed
   - `url`: location from which the paper can be downloaded
   - `status: "GOLD", "HYBRID", ...
  
[JSON Schema for abstract](abstract.json)

## authors

#### DESCRIPTION  
The core attributes of an author (name, affiliation, paper count, etc.). Authors have an "authorId" field, which can be joined to the "authorId" field of the members of a paper's "authors" field.  
75M records in 30 100MB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "authors" dataset provides summary information about authors.  
  
#### SCHEMA  
See https://api.semanticscholar.org/api-docs/graph#tag/Author-Data  
  
This dataset does not contain information about an author's papers.  
Instead, join with authors.authorId from the "papers" dataset.


## citations

#### DESCRIPTION  
Instances where the bibliography of one paper (the "citingPaper") mentions another paper (the "citedPaper"), where both papers are identified by the "paperId" field. Citations have attributes of their own, (influential classification, intent classification, and citation context).  
2.4B records in 30 8.5GB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "citations" dataset provides details about one paper's citation of another paper.  
  
#### SCHEMA
 - `citationid`: unique key for this citation
 - `citingcorpusid`: corpus id for the citing paper
 - `citedcorpusid`: corpus id for the cited paper (a _reference_)
 - `isinfluential`: true/false if the citation is considered influential. https://www.semanticscholar.org/faq#influential-citations  
 - `contexts`: Text surrounding the citation in the source paper's body.  
 - `intents`: Classification of the intent behind the citations. https://www.semanticscholar.org/faq#citation-intent  

## embeddings-specter_v1

#### DESCRIPTION  
A dense vector embedding representing the contents of the paper.  
120M records in 30 28GB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "embeddings-specter_v1" dataset provides embeddings representing a paper's contents in vector form.  
  
The model is based on the SPECTER model available at https://github.com/allenai/specter. However, the embeddings  
included in this dataset are not compatible with the embeddings produced by the pretrained model from that repo.  
  


## embeddings-specter_v2

#### DESCRIPTION  
A dense vector embedding representing the contents of the paper, generated with SPECTER2  
120M records in 30 28GB files.  
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "embeddings-specter_v2" dataset provides embeddings representing a paper's contents in vector form.  
  
The model is based on the SPECTER 2.0 model available at:  
https://github.com/allenai/SPECTER2_0  
  
These embeddings are compatible with embeddings produced by the pretrained  
model, available from https://huggingface.co/allenai/specter2  
  


## paper-ids

#### DESCRIPTION  
Mapping from sha-based ID to paper corpus ID.  
450M records in 30 500MB file
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "paper-ids" dataset provides mapping between different IDs representing a paper  
  
The primary key of a paper in the S2AG datasets is the corpusId field. However, the public API and web site also accept a sha-based ID, which is also used in some research datasets. This dataset provides a mapping between the different IDs.  
  
#### SCHEMA  
`sha` - A sha-based ID that can be used to access the paper via our API or web site  
`corpusid` - The paper's primary key  
`primary` - There should be only one primary sha for each corpusId. Accessing papers using a non-primary sha will redirect to the primary sha.  
  


## papers

#### DESCRIPTION  
The core attributes of a paper (title, authors, date, etc.).  
200M records in 30 1.5GB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "papers" dataset provides core metadata about papers.  
  
#### SCHEMA  
See https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data  
  
This dataset does not contain information about a paper's references or citations.  
Instead, join with citingPaperId/citedPaperId from the "citations" dataset.  
  


## publication-venues

#### DESCRIPTION  
Details about the venues in which papers are published
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "publication-venues" dataset contains meta-data for a research paper's publication  
journal or venue. The data sources of the venue data comes from The Fatcat Archive, documented  
here: https://archive.org/details/fatcat_snapshots_and_exports?sort=-publicdate, and the now deprecated Microsoft  
Academic Graph (MAG).  
  
#### SCHEMA  
 - id: The id of the venue data. The value also corresponds to the "venueId" field in the papers dataset.  
 - issn: The issn of the publication venue  
 - alternate_issns: The alternative issns for the publication venue  
 - name: The name of the venue  
 - alternate_names: The alternative names for the publication venue  
 - url:  The publication venue's url  
 - alternate_urls: The alternative urls of the publication venue  
 - type: The type (journal / conference) of the publication venue  
  


## s2orc

#### DESCRIPTION  
Full-body paper text parsed from open-access PDFs. Identifies structural elements such as paragraphs, sections, and bibliography entries.  
10M records in 30 4GB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "s2orc" dataset contains parsed full-body text from selected papers.  
  
A subset of this data was previously released (in a different format) as S2ORC https://github.com/allenai/s2orc  
  
The body text is parsed from PDF documents using Grobid, documented at https://grobid.readthedocs.io.  
Its output is converted from XML into a single string with a set of annotation spans.  
  
#### SCHEMA  
 - externalIds: IDs of this paper in different catalogs  
 - content:  
   - source:  
	   - pdfUrls: URLs to the PDF  
	   - oaInfo: license/url/status information from Unpaywall  
   - text: Full body text as a single string  
   - annotations: Annotated spans of the full body text  
  
  


## tldrs

#### DESCRIPTION  
A short natural-language summary of the contents of a paper.  
58M records in 30 200MB files
#### README  
Semantic Scholar Academic Graph Datasets  
  
The "tldrs" dataset provides short natural-language summaries of a paper's content.  
  
The model is based on the SciTLDR model available at https://github.com/allenai/scitldr.  
  

