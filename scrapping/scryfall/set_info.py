import psycopg2
from psycopg2 import sql
import scrapping.utility as su
import scrapping.scryfall.utility as ssu
import database.db_reader as dbr

"""Module for pulling set info from the Scryfall API"""

# Constants
SCRYFALL_SET_URL = 'https://api.scryfall.com/sets'


def get_sets_from_db(db_cursor):
    return ssu.get_distinct_column_from_table(db_cursor, ('cards', 'printings'), 'set')


def get_set_data(logger):
    logger.info('Retrieving all set info from Scryfall')
    json_data = ssu.json_from_url(SCRYFALL_SET_URL)
    data = json_data['data']

    printing_info = {}
    for printing in data:
        set_name = printing['code']
        printing_info[set_name] = printing
    return printing_info


def insert_set_data(db_cursor, code, full_name, release_date, size, logger):
    logger.info(f'Inserting set info for set {code}')
    insert_query = ssu.get_n_item_insert_query(4).format(
        sql.Identifier('cards', 'set_info'), sql.Identifier('set'), sql.Identifier('full_name'),
        sql.Identifier('release'), sql.Identifier('size'))
    db_cursor.execute(insert_query, (code, full_name, release_date, size))


def get_stored_set_data(database, user, logger):
    with psycopg2.connect(database=database, user=user) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            # get all sets stored in database
            recorded_sets = get_sets_from_db(cursor, )

            # get all set data as mapping of set code to set info
            set_data = get_set_data(logger)

            # # for each set get data from Scryfall, then parse and store it appropriately
            for printing in recorded_sets:
                if printing not in set_data:  # should never happen, sanity check
                    raise ValueError(f'Unsupported printing with code {printing}')
                else:
                    info = set_data[printing]
                    full_name = info['name']
                    release_data = info['released_at']  # already in isodate form, year-month-day
                    size = info['card_count']
                    insert_set_data(cursor, printing, full_name, release_data, size, logger)


if __name__ == '__main__':
    logger = su.init_logging('scryfall_set_scrapper.log')
    get_stored_set_data(dbr.DATABASE_NAME, dbr.USER, logger)
