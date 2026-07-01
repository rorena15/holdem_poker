class Player:
    def __init__(self, name, chips, is_human):
        self.name = name
        self.chips = chips
        self.is_human = is_human
        self.hole = []
        self.bet = 0
        self.total_bet = 0
        self.folded = False
        self.all_in = False


def post_blind(p, amount):
    pay = min(amount, p.chips)
    p.chips -= pay
    p.bet += pay
    p.total_bet += pay
    if p.chips == 0:
        p.all_in = True
    return pay
