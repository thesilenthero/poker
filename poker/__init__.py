import os


from poker.hand_lookup import create_hand_lookup

if not os.path.isfile(os.path.join(os.path.split(__file__)[0], 'hand_lookup.dat')):
    create_hand_lookup()

from poker.cards import Card, Deck, Hand
from poker.evaluator import rank_hand


def summarize_hand(h1, h2, board):

    flop = rank_hand(h1, board[:3]), rank_hand(h2, board[:3])
    turn = rank_hand(h1, board[:4]), rank_hand(h2, board[:4])
    river = rank_hand(h1, board[:5]), rank_hand(h2, board[:5])

    h1_score = rank_hand(h1, board[:5])
    h2_score = rank_hand(h2, board[:5])

    if h1_score['rank'] < h2_score['rank']:
        winner = f"Player 1 wins: {h1_score['descr']}"
    elif h2_score['rank'] < h1_score['rank']:
        winner = f"Player 2 wins: {h2_score['descr']}"
    else:
        winner = f"Tie: {h2_score['descr']}"

    print(f"""PLAYERS:
Player 1: {h1}
Player 2: {h2}

======== FLOP ========
Board: {board[:3]}
Player 1: {flop[0]['descr']}, percentage rank: {round(1 - (flop[0]['rank'] / 7462), 3)}
Player 2: {flop[1]['descr']}, percentage rank: {round(1 - (flop[1]['rank'] / 7462), 3)}

======== TURN ========
Board: {board[:4]}
Player 1: {turn[0]['descr']}, percentage rank: {round(1 - (turn[0]['rank'] / 7462), 3)}
Player 2: {turn[1]['descr']}, percentage rank: {round(1 - (turn[1]['rank'] / 7462), 3)}

======== RIVER ========
Board: {board[:5]}
Player 1: {river[0]['descr']}, percentage rank: {round(1 - (river[0]['rank'] / 7462), 3)}
Player 2: {river[1]['descr']}, percentage rank: {round(1 - (river[1]['rank'] / 7462), 3)}

======== SUMMARY ========
""" + winner)
