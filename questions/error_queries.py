from questions.utility import generic_search

"""Collection of queries showing errors / malformed data in the database"""

# Decks FROM mtgtop8 that have sideboards above 15
missized_sideboard = ('SELECT e.url, SUM(c.quantity) q '
                      'FROM events.event_entry e JOIN events.entry_card c ON c.entry_id = e.entry_id '
                      'WHERE c.is_mainboard = \'f\' '
                      'GROUP BY e.entry_id HAVING SUM(c.quantity) > 15 ORDER BY q DESC')

# Decks FROM mtgtop8 that have cards with a quantity greater than 4
too_many_cards = ('SELECT e.url u, c.quantity q '
                  'FROM events.event_entry e JOIN events.entry_card c ON c.entry_id = e.entry_id '
                  'HAVING q > 4 ORDER BY u, q DESC')

# Decks from mtgtop8 that have deck sizes greater than 60 (not always an issue)
url_to_deck_size = ('SELECT e.url, SUM(c.quantity) q '
                    'FROM events.event_entry e JOIN events.entry_card c ON c.entry_id = e.entry_id '
                    'GROUP BY e.entry_id HAVING SUM(c.quantity) > 60 ORDER BY q DESC')

# Decks FROM mtgtop8 that have have a mislabelled card, labelled as "Unknown Card"
error_decks = ('WITH ids AS ('
               'SELECT DISTINCT(e.entry_id) id '
               'FROM events.entry_card e '
               'WHERE e.card = \'Unknown Card\') '
               'SELECT DISTINCT(e.url) '
               'FROM events.event_entry e, ids '
               'WHERE e.entry_id = ids.id')

if __name__ == '__main__':
    for i in generic_search(error_decks):
        print(i)
