from itertools import combinations as combin

from .hand_lookup import open_hand_lookup
# from poker import hands_table

hands_table = open_hand_lookup()


def card_chain(*objs):
    """
    Joins lists and individual objects together into a single list
    Used to iterate through individual cards and lists of cards together
    >>> ch = card_chain([1, 2, 3], 4, 5, [6, 7])
    >>> list(ch)
    >>> [1, 2, 3, 4, 5, 6, 7]
    """
    for obj in objs:
        try:
            iter_obj = iter(obj)
            for x in iter_obj:
                yield x
        except TypeError:
            yield obj


def is_suited(hand):
    return len(set([card.suit for card in hand])) == 1


def rank_hand(*cards):
    hand = sorted(list(card_chain(*cards)))
    if len(hand) < 5 or len(hand) > 7:
        raise ValueError("Hand must be between 5-7 cards")

    hand_combins = []
    suited = []
    append_hand = hand_combins.append
    append_suited = suited.append

    for hand_combin in combin(hand, 5):
        append_suited(is_suited(hand_combin))
        append_hand(list(hand_combin))

    # print(hand_combins)
    # print(suited)

    if len(hand_combins) == 1 & len(suited) == 1:
        result = hands_table[(hands_table['objects'].apply(lambda row: list(row) == hand_combins[0])) & (hands_table['Flush'] == suited[0])]
    else:
        result = hands_table[hands_table['objects'].apply(sorted).isin(hand_combins) & hands_table['Flush'].isin(suited)]

    return result.reset_index()[['descr', 'rank', 'sample_hand', 'abbrev', 'Flush']].iloc[0, :].to_dict()
