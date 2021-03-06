import database.db_reader as ddr
import psycopg2
import pathlib as pl
from typing import Union, List, Generator
import datetime as dt


def generic_search(search_query: str) -> List:
    """Generic function that executes a search query in the database and returns the results.
    :param search_query: search query to execute
    :return: results of search query
    """
    with psycopg2.connect(user=ddr.USER, database=ddr.DATABASE_NAME) as con:
        with con.cursor() as cursor:
            cursor.execute(search_query)
            return cursor.fetchall()


def load_query(path: Union[str, pl.Path]) -> str:
    with open(path, 'r') as f:
        lines = f.readlines()
    return ''.join(lines)


def date_range(start: str, end: str, start_buffer: int) -> Generator[str, None, None]:
    date_format = '%Y-%m-%d'
    convert = lambda x: dt.datetime.strptime(x, date_format).date()
    start = convert(start) + dt.timedelta(days=start_buffer)
    end = convert(end) + dt.timedelta(days=1)
    for i in range((end - start).days):
        yield start.strftime(date_format)
        start += dt.timedelta(days=1)


if __name__ == '__main__':
    print([i for i in date_range('2019-01-13', '2020-07-23', 14)])
