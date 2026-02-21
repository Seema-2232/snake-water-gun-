import tkinter as tk
import random
from collections import Counter

class SnakeWaterGunGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Water Gun Game")

        self.choices = ["snake", "water", "gun"]
        self.win_map = {
            "snake": "water",
            "water": "gun",
            "gun": "snake"
        }

        self.player_score = 0
        self.computer_score = 0
        self.history = []

        self.label = tk.Label(root, text="Choose your move", font=("Arial", 16))
        self.label.pack(pady=10)

        for choice in self.choices:
            tk.Button(root, text=choice.capitalize(),
                      command=lambda c=choice: self.play_round(c),
                      width=15).pack(pady=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0 - 0")
        self.score_label.pack()

    def get_computer_choice(self):
        return random.choice(self.choices)

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

        self.result_label.config(
            text=f"Computer chose {computer_choice}. Winner: {winner}"
        )

        self.score_label.config(
            text=f"Score: {self.player_score} - {self.computer_score}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeWaterGunGUI(root)
    root.mainloop()