"""
This python module will be used to evaluate hands in the poker game.
Essentially, each hand will be scored from 1-10 depending on No Limit Texas Hold'Em Rules.
This scoring system will help guide the Monte-Carlo Simulator in determining hand win probability.
The hand win probability will be used to determine expected profit for player with each decision.
Expected profit will be used to determine decision as well as opponents decision (to update pot)


"""

def calculate_winprob(your_cards, community_cards, players, num_opponents = 5, iterations = 10000):
    import eval7
    import random
    num_opponents = count_players(players)
    my_cards = [eval7.Card(c) for c in your_cards]
    board = [eval7.Card(c) for c in community_cards]
    deck = eval7.Deck()
    for card in my_cards + board:
        deck.cards.remove(card)
    cards_remaining = 5 - len(community_cards)
    wins = 0
    ties = 0
    losses = 0
    equity = 0
    # Win prob = wins/total, Tie Prob = ties/total, Loss Prob = losses/total
    for x in range(0, iterations):
        opposing_hands = []
        random.shuffle(deck.cards)
        card_num = 0
        for y in range(0, num_opponents):
            #deal cards to opponents
            opposing_hands.append(deck.cards[card_num:card_num+2])
            card_num += 2
        new_board = deck.cards[card_num:card_num+cards_remaining]
        temp_board = board + new_board
        my_score = evaluate_hand(my_cards, temp_board)
        opponent_scores = []
        for hand in opposing_hands:
            opponent_scores.append(evaluate_hand(hand, temp_board))
        all_scores = [my_score] + opponent_scores
        best_score = max(all_scores)
        if my_score == best_score:
            winners = all_scores.count(best_score)
            equity += 1 / winners
    return equity/iterations

        



def evaluate_hand(your_cards, community_cards):

    """
    This will be a function called to evaluate a hand.
    It will check if a hand is of the 
    """

    import eval7
    cards = your_cards + community_cards
    return eval7.evaluate(cards)

def count_players(players):
    counter = 0
    for x in range(0, len(players)):
        if players[x]['state'] == 'active':
            counter += 1


def make_decisions(estimated_equity, pot, amount_owed, stack, players):
    n_players = count_players(players)
    ev = {}

    # Fold
    if amount_owed > 0:
        ev["fold"] = 0
        ev["check"] = estimated_equity * pot



    # Call
    if amount_owed > 0:
        call_amount = min(amount_owed, stack)
        ev["call"] = (
            estimated_equity * (pot + call_amount)
            - call_amount
        )

    return ev





if __name__ == "__main__":

    test_hands = [
        ["As", "Ah"],  # Pocket aces
        ["Ks", "Qs"],  # Suited king-queen
        ["7h", "2c"],  # Weak starting hand
        ["Js", "Jd"],  # Pocket jacks
        ["As", "Ks"]   # Suited ace-king
    ]

    for hand in test_hands:
        equity = calculate_winprob(
            your_cards=hand,
            community_cards=[],
            num_opponents=5,
            iterations=15000
        )

        print(f"Hand: {hand} | Equity: {equity:.2%}")

