create table if not exists public.papers
(
    corpusid   text  not null
        constraint papers_pk
            primary key,
    sha        text not null
        constraint papers_pk_2
            unique,
    paper_json jsonb not null
);