import re
import dotenv

# Regex pattern to parse the database connection string.
CONNECTION_RE = re.compile('postgres://([^:]*):([^@]*)@([^/]*)/([^?]*)?')


def get_connection_string(env_variable_name: str) -> str:
    """
    Returns a connection string in a format suitable for psycopg2.

    :param env_variable_name: The environment variable name that specifies the database connection data'
    :return: a connection string in the format: "dbname='dbname' user='user' host='host' password='password'.

    The environment variable should contain a value like 'postgres://user:password@localhost/dbname', as used by dbmate.
    """
    parsed = parse(dotenv.dotenv_values()[env_variable_name])
    if parsed is not None:
        user, password, host, dbname = parsed
        return f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'"


def parse(env_entry: str):
    """
    Converts a string in the format used by dbmate to a connection string for use by psycopg2.

    :param env_entry:
    :return:  a tuple (user, password, host, dbname) or None.

    If the string does not match the format, it returns None.
    """
    result = None
    match = CONNECTION_RE.search(env_entry)
    if match is not None:
        result = (
            match.group(1),
            match.group(2),
            match.group(3),
            match.group(4)
        )
    return result
