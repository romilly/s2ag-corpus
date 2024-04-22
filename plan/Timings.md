# Running the Semantic Scholar database on a Raspberry Pi

## Can you do it with Python and Postgres?

Over the last few days I've been squeezing a quart into a pint pot.

In this post I'll describe what I am trying to do and tell you about the pitfalls and solutions I've found so far.

You'll see a lot of explanation, some Python code, and a link to the GitHub repository in the Resources section at the end.

## Semantic Scholar

I've used the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to help me with my research for years.

The Semantic Scholar corpus is maintained by the Allen Institute for AI.
It's a wonderful resource for researchers, and it's free to use.

he Semantic Scholar REST API allows you to find and explore scientific publication
data about authors, papers, citations, venues, and more. 

You can access the Semantic Scholar corpus via the web, and you download their datatasets for private or commercial use.

They have details of over 200 million scientific papers, including titles, abstracts. citations and references.

I've been using the Semantic Scholar web interface, but I decided that I ought to maintain a local copy of their data.
I figured that would improve my access while reducing the load on their infrastructure.

The database is _large_: in addition to the 214 million papers, there are 2.49 billion citations and references,
so it's challenging to ensure acceptable performance.

I decided to see if I could use a local Postgres database on a Raspberry Pi.

## Why a PI?

The Pi is inexpensive and has a huge supportive community. I've used the Pi since it first came out, and
I have a suitable Pi available.

I have found some dramatic speed-ups in my experiments. I'll describe them in the rest of the article.

## First experiments

I started by downloading the datasets I wanted and exploring how best to load them into Postgres.

For my intended use I only need four of the datasets:
1. The `papers` dataset which contains of 60 zipped files containing 218 million rows of data in json format.
2. The `abstracts` dataset which contains article abstracts and other related information for a subset of the papers.
3. The `tldrs` dataset which contains short AI-generated summaries of a subset of the papers.
3. The `citations` dataset, which contains the ids of the citing and cited paper, along with some additional data.

For each paper, a _reference_ is a mention of an earlier relevant paper by the authors,
and a _citation_ is a reference to that paper by a later paper.

The `papers` table has a numeric key `corpusid` and a jsonb column `paper_json`.

I'll describe the other tables in a later article.

### Getting access to the data

Anyone can use the Semantic Scholar web interface, but you need a free API key to download the datasets.
It's easy to apply for a key: mine arrived within 24 hours. 

Once you have a key you can use the API to retrieve a list of the available
datasets and their descriptions, and then download the datasets themselves.

### Loading the data into Postgres

Each dataset has a lot of data, and I was anxious about how long it would take for the Pi to load the datasets into Postgres.

I created a series of Jupyter notebooks to explore and time the loading process.

For my first experiment I decided to try a simplistic approach which I knew I could improve on.

I unzipped one of the `gz` papers files I'd downloaded and used the `head` command
to create a test file of the first 10,000 rows of json data.

I then wrote a very simple script to populate a `papers` table in a test database on my workstation.

Here's the SQL that created the table:

```sql
create table public.papers
(
    corpusid   integer not null
        constraint papers_pk
            primary key,
    paper_json jsonb   not null
);
```

And here's the Python code that read the file and populated the table:

```python
test_file = base_dir+'/2024-04-02/papers/first10000papers'
with open(test_file) as f:
    with connection.cursor() as cursor:
        for line in f:
            line = line.strip()
            lj = json.loads(line)
            corpus_id = lj['corpusid']
            cursor.execute(INSERT_PAPER_SQL, (corpus_id, line))
            connection.commit()
```

That code took just under 9 seconds - much slower than I would like.

If 10,000 records take 9 seconds to load, how long would 217,545,831 take?

**Over 6 days!**

I found that code on the web, but it's obviously ridiculous. It's doing a commit after every row, and that's sloooow.

I tried again, moving the commit out of the loop.

That took 1.2 seconds - much better.

However, I still had a couple of tricks up my sleeve.

I'd been using the `psycopg2` library to interact with Postgres, and I knew that had faster ways of doing bulk inserts.

Don't use the execute_many method; it has no speed benefit.
Instead, I used the `execute_batch` method from `psycopg2.extras`

```python
test_file = base_dir+'/2024-04-02/papers/first10000papers'
with open(test_file) as f:
    jason_dictionaries = [(line, json.loads(line)) for line in f.readlines()]
    records = [(jd['corpusid'], line) for  line, jd in jason_dictionaries]
    with connection.cursor() as cursor:
        execute_batch(cursor, INSERT_PAPER_SQL, records)
        connection.commit()
```

That took 0.6 seconds. Satisfactory, but I wondered if I could do even better!

`psycopg2` has a method called copy_from which takes a csv file and inserts the contents directory into the database,
and it's very fast. There's just one problem: the datasets are json files, and copy-from needs a csv file.

It's not hard to convert from one format to the other. Alas, it took mode time to write the converted data
to a file than the previous bulk insert.

Could I find a way of doing the conversion without writing to/reading from a file?

I did.

The code is a bit long to print, but you can see it (and all the earlier examples) in the project's [GitHub repository](https://github.com/romilly/s2ag-corpus.git).

It's in the `load-test-corpus-papers-v5.ipynb` notebook.

Running it took 0.4 seconds!

As a final test I used the first of the downloaded files which contains just under 5 million records.
On my workstation it took 2 minutes and 24 seconds to populate the table with `corpusid` as its primary key.

Since there are sixty such files, some rather smaller,
it should take about two and a half hours to populate that table using my workstation.

### Using the data

For my particular use case I'll be reading small batches of records selected by corpusid.
Quick tests show this is almost instantaneous.

## What's coming next?

There's still a lot to do. I've run tests ona Pi 5 using a USB HDD, and the timings are acceptable.
I should be able to speed thm up a lot using an NVME SSD, and I'll explore that later this week.

Loading the tldr and abstract data will take less time than the papers data,
but I am not sure how long the citations data will take to load or access. That's the next bit of coding to test.

Once the database is in production there will still be work to do. I could load the full datasets each week,
but it would be much faster, and more public-spirited, to just download the diffs whihc Semantic Scholar provids.
Of course that will need  additional code.

## Resources.

[Semantic Scholar API](https://www.semanticscholar.org/product/api) - also has links to the discord group.
[Semantic Scholar API docs](https://api.semanticscholar.org/api-docs/graph) 
[My GitHub repository](https://github.com/romilly/s2ag-corpus.git)

## Stay tuned!

I'll be writing about the next stags on substack, and there will be a lot more code coming from my related projects.

Follow me - [@rareblog](https://twitter.com/rareblog) - on X for details, or revisit this page on GitHub.





