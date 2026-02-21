import random
from collections import Counter

class SnakeWaterGunGame:
    def __init__(self, player_name, rounds, difficulty="easy"):
        self.player_name = player_name
        self.rounds = rounds
        self.difficulty = difficulty
        self.choices = ["snake", "water", "gun"]
        self.win_map = {
            "snake": "water",
            "water": "gun",
            "gun": "snake"
        }
        self.player_score = 0
        self.computer_score = 0
        self.history = []

    def get_computer_choice(self):
        if self.difficulty == "easy":
            return random.choice(self.choices)

        elif self.difficulty == "medium":
            if len(self.history) < 2:
                return random.choice(self.choices)
            return self.counter_player_move()

        elif self.difficulty == "hard":
            if len(self.history) == 0:
                return random.choice(self.choices)
            return self.counter_player_move()

    def counter_player_move(self):
        player_moves = [h[0] for h in self.history]
        most_common = Counter(player_moves).most_common(1)[0][0]

        # Counter logic
        for key, value in self.win_map.items():
            if value == most_common:
                return key

    def check_win(self, player, computer):
        if player == computer:
            return "Tie"
        elif self.win_map[player] == computer:
            return "Player"
        else:
            return "Computer"

    def play_round(self, player_choice):
        computer_choice = self.get_computer_choice()
        winner = self.check_win(player_choice, computer_choice)

        if winner == "Player":
            self.player_score += 1
        elif winner == "Computer":
            self.computer_score += 1

        self.history.append((player_choice, computer_choice, winner))
        return computer_choice, winner

    def play_game(self):
        for i in range(self.rounds):
            player_choice = input("Choose snake, water, or gun: ").lower()
            while player_choice not in self.choices:
                player_choice = input("Invalid! Choose snake, water, or gun: ").lower()

            computer_choice, winner = self.play_round(player_choice)

            print(f"Computer chose: {computer_choice}")
            print(f"Winner: {winner}")
            print(f"Score: {self.player_score} - {self.computer_score}")
            print("-" * 30)

        print("\nFinal Result:")
        print(f"{self.player_name}: {self.player_score}")
        print(f"Computer: {self.computer_score}")


if __name__ == "__main__":
    name = input("Enter your name: ")
    rounds = int(input("Enter rounds: "))
    difficulty = input("Choose difficulty (easy/medium/hard): ").lower()

    game = SnakeWaterGunGame(name, rounds, difficulty)
    game.play_game()