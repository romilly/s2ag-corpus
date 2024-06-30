create table if not exists paperids
(
    sha        text    not null
        constraint paperids_pk
            unique,
    corpusid   text    not null,
    is_primary boolean not null
);