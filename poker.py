import random

from holdem.actions import PERSONALITIES
from holdem.game import play_hand
from holdem.player import Player
from holdem.quests import new_quest, update_quest
from holdem.save import load_state, save_state
from holdem.shop import offer_rebuy, open_shop


def main():
    print("=== 텍사스 홀덤 ===")
    state = load_state()
    if state['chips'] <= 0:
        state['chips'] = 1000
    coins = state['coins']
    quest = state['quest'] or new_quest()

    print(f"불러온 칩: {state['chips']}  |  보유 코인: {coins}")
    print(f"현재 퀘스트: {quest['desc']} ({quest['progress']}/{quest['target']}, 완료 시 {quest['reward']}코인)")

    try:
        num_bots = int(input("상대 봇 수 (1-5, 기본 3): ") or 3)
    except ValueError:
        num_bots = 3
    num_bots = max(1, min(5, num_bots))

    small_blind, big_blind = 10, 20
    human = Player("나", state['chips'], True)
    players = [human]
    players += [Player(f"봇{i+1}", 1000, False, style=random.choice(PERSONALITIES)) for i in range(num_bots)]
    dealer_idx = 0

    while True:
        human.quest, human.coins = quest, coins
        hand_ctx = play_hand(players, dealer_idx, small_blind, big_blind)

        if hand_ctx is not None:
            quest, reward, completed_desc = update_quest(quest, hand_ctx)
            if reward:
                coins += reward
                print(f"\n*** 퀘스트 완료: {completed_desc} (+{reward}코인) *** 보유 코인: {coins}")
                print(f"새 퀘스트: {quest['desc']} ({quest['target']}회 목표, 보상 {quest['reward']}코인)")

        print("\n--- 현재 칩 현황 ---")
        for p in players:
            print(f"{p.name}: {p.chips}")

        for b in players:
            if not b.is_human and b.chips == 0:
                print(f"{b.name} 파산으로 탈락했습니다.")
        alive_bots = [p for p in players if not p.is_human and p.chips > 0]

        if human.chips == 0:
            coins, gained = offer_rebuy(coins)
            if gained:
                human.chips = gained
                print(f"{human.name} 리바이인 완료! 칩 {gained}개로 복귀합니다.")

        players = ([human] if human.chips > 0 else []) + alive_bots
        save_state({'chips': human.chips, 'coins': coins, 'quest': quest})

        if human.chips == 0:
            print("\n파산했습니다. 게임 종료.")
            break
        if len(players) < 2:
            print(f"\n{players[0].name} 최종 우승!")
            break

        dealer_idx = (dealer_idx + 1) % len(players)
        cmd = input("\n다음 핸드 진행? (엔터=계속, s=상점, q=종료): ").strip().lower()
        if cmd == 's':
            coins, gained = open_shop(coins)
            if gained:
                human.chips += gained
                save_state({'chips': human.chips, 'coins': coins, 'quest': quest})
        elif cmd == 'q':
            break


if __name__ == "__main__":
    main()
