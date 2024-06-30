# Test data for the diff code

The first test of the diff code operates on the `paperids` table, as this is simple in structure.

Each `sha` describes what sort of row it is in order to show the intent of the test. 
The `sha` and `corpusid` values are not consistent with real data from Semantic Scholar,
but that does not affect the validity of the test.

One `corpusid` is updated, and two `is_primary` values are flipped.

Note that the json created by Semantic Scholar uses `primary` rather than `is_primary`.
The table definition uses `is_primary` because `primary` is
a keyword in SQL.


## Specification

| sha         | corpusid | updated | is_primary | updated |
| ----------- | -------- |---------|------------|---------|
| update01    | 1234567  | 1234560 | false      | true    |
| insert01    | 2345678  | 2345678 | true       | true    |
| delete01    | 764320   | -       | false      | -       |
| unchanged01 | 24680    | 24680   | false      | false   |
| insert02    | 35791    | 35791   | false      | false   |
| update02    | 27463    | 27463   | true       | false   |
| unchanged02 | 86429    | 86429   | true       | true    |
| delete02    | 3749230  | -       | true       | -       |

For *inserts*, this table shows what values should be inserted.

For *updates*, this table shows the initial `is_primary` state;
the updated `is_primary` value should be the **opposite** of
the initial value.

One `corpusid` value is changed.

## Initial values in the test database

| sha         | corpusid | is_primary |
|-------------|----------|------------|
| update01    | 1234567  | false      |
| delete01    | 764320   | false      |
| unchanged01 | 24680    | false      |
| update02    | 27463    | true       |
| unchanged02 | 86429    | true       |
| delete02    | 3749230  | true       |

## Upserts in json format

```json
{"sha": "update01", "corpusid": 1234560, "primary": "true"}
{"sha": "insert01", "corpusid": 2345678, "primary": "true"}
{"sha": "insert02", "corpusid": 35791, "primary": "false"}
{"sha": "update02", "corpusid": 27463, "primary": "false"}
```

## Deletions in json format

```json
{"sha": "delete01"}
{"sha": "delete02"}
```

## Expected final values in the test database

|      sha      | corpusid | is_primary |
| ------------- |----------| ---------- |
|  update01     | 1234560  | true       |
|  unchanged01  | 24680    | false      |
|  insert01     | 2345678  | true       |
|  insert02     | 35791    | false      |
|  update02     | 27463    | false      |
|  unchanged02  | 86429    | true       |
