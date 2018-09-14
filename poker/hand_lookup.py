from functools import partial
import os
import re
import requests

from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd

from .cards import Card, Hand


lookup_path = os.path.join(os.path.split(__file__)[0], 'hand_lookup.dat')


def scrape_page():
    req = requests.get("http://suffe.cool/poker/7462.html")
    soup = BeautifulSoup(req.text, 'lxml')
    tables = soup.select('table[cellpadding=8]')
    hands_text = tables[0].pre.text
    for row in hands_text.split('\n')[1:]:
        yield row


def parse_text():
    hands_raw = (row.strip() for row in scrape_page())
    splitted = (re.compile(r'\s{3,}').split(row) for row in hands_raw)
    df = DataFrame(splitted, columns=['rank', 'five_card', 'six_card', 'seven_card', 'eight_card', 'sample_hand', 'abbrev', 'descr'])
    df = df[:-6]
    df['rank'] = pd.to_numeric(df['rank'])
    df.set_index('rank', inplace=True)
    df.iloc[:, :4] = df.iloc[:, :4].apply(lambda row: row.apply(int))

    return df


def string_to_cards(card_string, suits):
    ranks = card_string.split(' ')
    return [Card.string(rank + suit) for rank, suit in zip(ranks, suits)]


fourkind = partial(string_to_cards, suits=['d', 's', 'h', 'c', 'd'])
flush = partial(string_to_cards, suits=['d', 'd', 'd', 'd', 'd', ])
fullhouse = partial(string_to_cards, suits=['d', 's', 'h', 'd', 's'])


def create_hand_lookup():

    hands = parse_text()
    hands.abbrev.unique()
    hands['objects'] = None
    hands.iloc[0, -3] = 'RF'

    hands.loc[hands.abbrev == '4K', 'objects'] = hands.loc[hands.abbrev == '4K', 'sample_hand'].apply(fourkind)

    hands.loc[hands.abbrev == 'FH', 'objects'] = hands.loc[hands.abbrev == 'FH', 'sample_hand'].apply(fullhouse)

    hands.loc[hands.abbrev.isin(['F', 'SF']), 'objects'] = hands.loc[hands.abbrev.isin(['F', 'SF']), 'sample_hand'].apply(flush)

    # hands[hands.objects.isna()].abbrev.unique()

    hands.loc[(~hands.abbrev.isin(['RF'])) & (hands.objects.isna()), 'objects'] = hands.loc[(~hands.abbrev.isin(['RF'])) & (hands.objects.isna()), 'sample_hand'].apply(fourkind)

    hands['rank_percentage'] = 1 - (hands.index / 7462)
    hands.at[1, 'objects'] = [Card.string(i + 'd') for i in ['A', 'K', 'Q', 'J', 'T']]
    hands['objects'] = hands.objects.apply(lambda row: Hand(sorted(row)))
    hands['Flush'] = hands.descr.str.contains('Flush')
    hands.to_pickle(lookup_path)
    return hands


def open_hand_lookup():
    return pd.read_pickle(lookup_path)
