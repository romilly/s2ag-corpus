create table if not exists public.paperids
(
    sha        text    not null
        constraint paperids_pk
            unique,
    corpusid   text    not null
        constraint paperids_pk_2
            unique,
    is_primary boolean not null
);