CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

FIVE = 'five'
FOUR = 'four'
FULL_HOUSE = 'full-house'
THREE = 'three'
TWO_PAIR = '2-pair'
ONE_PAIR = '1-pair'
HIGH_CARD = 'high'

TYPES = {
    FIVE: 0, FOUR: 1, FULL_HOUSE: 2, THREE: 3, TWO_PAIR: 4, ONE_PAIR: 5, HIGH_CARD: 6
}

class Hand:
    def __init__(self, cards: list[int], bet: int) -> None:
        self.cards = cards
        self.bet = bet
        self.type = -1

    def __repr__(self) -> str:
        card_str = ''
        for c in self.cards:
            card_str += CARDS[c]
        card_str += ' '
        card_str += str(self.bet)
        return card_str
    
    def __str__(self) -> str:
        card_str = ''
        for c in self.cards:
            card_str += CARDS[c]
        card_str += ' '
        card_str += str(self.bet)
        return card_str
    
    def get_type(self) -> int:
        if (self.type != -1):
            return self.type
        counts_dict = {}
        for card in self.cards:
            if not card in counts_dict:
                counts_dict[card] = 1
            else:
                counts_dict[card] += 1
        counts = list(counts_dict.values())
        counts.sort(reverse=True) # sort in descending order
        type = -1
        if counts[0] == 5:
            type = TYPES[FIVE]
        elif counts[0] == 4:
            type = TYPES[FOUR]
        elif counts[0] == 3:
            type = TYPES[FULL_HOUSE] if counts[1] == 2 else TYPES[THREE]
        elif counts[0] == 2:
            type = TYPES[TWO_PAIR] if counts[1] == 2 else TYPES[ONE_PAIR]
        elif counts[0] == 1:
            type = TYPES[HIGH_CARD]
        else:
            raise Exception(f"unexpected count {counts[0]}")
        self.type = type
        return type 


    def first_card(self) -> int:
        return self.cards[0]


def get_cards():
    card_dict = {}
    for card_idx in range(len(CARDS)):
        card = CARDS[card_idx]
        card_dict[card] = card_idx
    return card_dict


def read_input(file_name) -> list[Hand]:
    card_dict = get_cards()
    print(card_dict)
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            parts = line.strip().split()
            hand_str = parts[0]
            bet = int(parts[1])
            hand = []
            for card in hand_str:
                hand.append(card_dict[card])
            result.append(Hand(hand, bet))
    return result

def sort_hands(hands: list[Hand]) -> None:
    # sort is stable - sort by the first card first
    # when sorting by type, the hands with the same type preserve the order of the first card
    hands.sort(key=lambda h: h.cards)
    hands.sort(key=lambda h: h.get_type())

def get_winnings(hands: list[Hand]):
    sort_hands(hands)
    sum = 0
    for idx in range(len(hands)):
        hand = hands[idx]
        rank = len(hands) - idx
        winning = hand.bet * rank
        print(hand, 'type:', hand.get_type(), 'rank:', rank, 'win:', winning)
        sum += winning
    return sum



hands = read_input('input.txt')
# hands = read_input('input_small.txt')

res1 = get_winnings(hands)
print(res1)


# for hand in hands:
#     print(hand, 'type:', hand.get_type())