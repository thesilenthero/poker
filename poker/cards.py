import os

from random import shuffle

path, _ = os.path.split(__file__)


class Card(object):
    """
    >>> Card(1, 4)
    2d
    >>> Card.string('Qh')
    Qh
    >>> C1, C2 = Card(9, 4), Card.string('3h')
    >>> C1 > C2
    True
    """

    _ranks = ['null', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q',
              'K', 'A']
    _suits = ['null', 'C', 'D', 'H', 'S']
    _suits_long = ['null', 'Clubs', 'Diamonds', 'Hearts', 'Spades']
    _ranks_long = ['null', '2', '3', '4', '5', '6', '7', '8', '9', 'Ten',
                   'Jack', 'Queen', 'King', 'Ace']

    # rank = WriteOnlyAttribute()
    # suit = WriteOnlyAttribute()

    def __init__(self, rank, suit):

        if rank not in range(1, 14):
            raise ValueError("Not a rank: {}. Select a rank from 1 to 13".format(rank))
        if suit not in range(1, 5):
            raise ValueError("Not a suit: {}. Select a suit from 1 to 4".format(suit))

        self._rank = rank
        self._suit = suit
        self.rank_str = self._ranks[rank]
        self.suit_str = self._suits[suit]
        self.values = self.rank, self.suit

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    @classmethod
    def string(cls, card_string):
        rank, suit = [x for x in card_string.upper()]
        return cls(cls._ranks.index(rank), cls._suits.index(suit))

    def _to_int(self, int_or_card):
        """Convert rank to integer"""
        if isinstance(int_or_card, Card):
            return int_or_card.rank
        return int_or_card

    def __lt__(self, other):
        return self.rank < self._to_int(other)

    def __le__(self, other):
        return self.rank <= self._to_int(other)

    def __gt__(self, other):
        return self.rank > self._to_int(other)

    def __ge__(self, other):
        return self.rank >= self._to_int(other)

    def __ne__(self, other):
        return self.rank != other.rank and self.suit != other.suit

    def __eq__(self, other):
        return self.rank == other.rank

    def __repr__(self):
        return ''.join([self.rank_str, self.suit_str.lower()])


class Hand(object):

    def __init__(self, cards):
        self.cards = cards

    @property
    def suits(self):
        return [card.suit for card in self.cards]

    @property
    def ranks(self):
        return [card.rank for card in self.cards]

    @property
    def values(self):
        return [(card.rank, card.suit) for card in self.cards]

    def index(self, card):
        try:
            index = self.values.index((card.rank, card.suit))
            return index
        except ValueError:
            raise ValueError(f"{card} is not in the deck.")

    def __contains__(self, card):
        try:
            self.index(card)
            return True
        except ValueError:
            return False

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __repr__(self):
        return f"Hand({self.cards})"


class Deck(Hand):

    def __init__(self):
        super().__init__([Card(x, y) for x in range(1, 14) for y in range(1, 5)])
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def deal(self, cards=1):

        if len(self) == 0:
            return None

        if isinstance(cards, str):
            card = Card.string(cards)
            card_index = self.index(card)
            return self.cards.pop(card_index)

        else:
            if cards == 1:
                to_deal = self.cards[0]
            else:
                to_deal = self.cards[0: cards]
            self.cards = self.cards[cards:]
            return to_deal

    def __repr__(self):
        return f"Deck({self.cards})"


if __name__ == '__main__':
    pass
