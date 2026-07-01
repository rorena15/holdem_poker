import random

QUEST_TEMPLATES = [
    {'id': 'win_hand', 'desc': '이번 핸드에서 팟 가져가기', 'target': 1, 'reward': 20},
    {'id': 'win_3_hands', 'desc': '팟을 3번 가져가기', 'target': 3, 'reward': 50},
    {'id': 'showdown_win', 'desc': '쇼다운에서 승리하기', 'target': 1, 'reward': 30},
    {'id': 'two_pair_plus', 'desc': '투페어 이상 족보로 승리하기', 'target': 1, 'reward': 40},
    {'id': 'survive_5', 'desc': '5핸드 동안 파산하지 않고 생존하기', 'target': 5, 'reward': 25},
    {'id': 'no_fold_3', 'desc': '3핸드 연속 폴드 없이 쇼다운까지 가기', 'target': 3, 'reward': 45},
]

REBUY_COST = 50
REBUY_CHIPS = 500


def new_quest():
    t = random.choice(QUEST_TEMPLATES)
    return {'id': t['id'], 'desc': t['desc'], 'target': t['target'], 'reward': t['reward'], 'progress': 0}


def update_quest(quest, ctx):
    if quest is None:
        quest = new_quest()

    qid = quest['id']
    advanced = False
    if qid in ('win_hand', 'win_3_hands') and ctx['human_won']:
        advanced = True
    elif qid == 'showdown_win' and ctx['human_won'] and ctx['reached_showdown']:
        advanced = True
    elif qid == 'two_pair_plus' and ctx['human_won'] and ctx['human_hand_category'] is not None and ctx['human_hand_category'] >= 2:
        advanced = True
    elif qid == 'survive_5' and not ctx['human_busted']:
        advanced = True
    elif qid == 'no_fold_3':
        if ctx['human_folded']:
            quest['progress'] = 0
        elif ctx['reached_showdown']:
            advanced = True

    if advanced:
        quest['progress'] += 1

    if quest['progress'] >= quest['target']:
        return new_quest(), quest['reward'], quest['desc']
    return quest, 0, None
