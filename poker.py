from holdem.game import play_hand
from holdem.player import Player


def main():
    print("=== 텍사스 홀덤 ===")
    try:
        num_bots = int(input("상대 봇 수 (1-5, 기본 3): ") or 3)
    except ValueError:
        num_bots = 3
    num_bots = max(1, min(5, num_bots))

    small_blind, big_blind = 10, 20
    players = [Player("나", 1000, True)]
    players += [Player(f"봇{i+1}", 1000, False) for i in range(num_bots)]
    dealer_idx = 0

    while True:
        play_hand(players, dealer_idx, small_blind, big_blind)

        print("\n--- 현재 칩 현황 ---")
        for p in players:
            print(f"{p.name}: {p.chips}")

        players = [p for p in players if p.chips > 0]
        if not any(p.is_human for p in players):
            print("\n파산했습니다. 게임 종료.")
            break
        if len(players) < 2:
            print(f"\n{players[0].name} 최종 우승!")
            break

        dealer_idx = (dealer_idx + 1) % len(players)
        if input("\n다음 핸드 진행? (엔터=계속, q=종료): ").strip().lower() == 'q':
            break


if __name__ == "__main__":
    main()
