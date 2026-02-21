import streamlit as st
import random
import pickle
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from collections import Counter

# ==============================
# INITIAL SETUP
# ==============================

st.set_page_config(page_title="AI Snake Water Gun", layout="centered")
st.title("AI Snake Water Gun Game 🧠")

choices = ["snake", "water", "gun"]

win_map = {
    "snake": "water",
    "water": "gun",
    "gun": "snake"
}

# ==============================
# DATABASE FUNCTIONS
# ==============================

def init_db():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_move TEXT,
        computer_move TEXT,
        winner TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_game(player, computer, winner):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO game_history (player_move, computer_move, winner)
    VALUES (?, ?, ?)
    """, (player, computer, winner))

    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect("game.db")
    df = pd.read_sql("SELECT * FROM game_history", conn)
    conn.close()
    return df

init_db()

# ==============================
# LOAD ML MODEL
# ==============================

model = None
try:
    model = pickle.load(open("model/model.pkl", "rb"))
except:
    pass

def predict_next_move(prev_move):
    df = pd.DataFrame([prev_move], columns=["prev_move"])
    df = pd.get_dummies(df)
    return model.predict(df)[0]

# ==============================
# RL AGENT (Q-LEARNING)
# ==============================

class RLAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2
        self.actions = choices

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)

        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

        old_value = self.q_table[state][action]
        next_max = max(
            self.q_table.get(next_state, {a: 0 for a in self.actions}).values()
        )

        new_value = old_value + self.alpha * (
            reward + self.gamma * next_max - old_value
        )

        self.q_table[state][action] = new_value


if "agent" not in st.session_state:
    st.session_state.agent = RLAgent()

if "player_score" not in st.session_state:
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.last_move = None

# ==============================
# GAME SECTION
# ==============================

st.header("Play Game")

player_choice = st.selectbox("Choose your move:", choices)

strategy = st.radio(
    "Select AI Strategy:",
    ["Random", "Logistic Regression", "Reinforcement Learning"]
)

if st.button("Play Round"):

    # ==================
    # SELECT COMPUTER MOVE
    # ==================

    if strategy == "Random":
        computer_choice = random.choice(choices)

    elif strategy == "Logistic Regression" and model and st.session_state.last_move:
        predicted = predict_next_move(st.session_state.last_move)

        for key, value in win_map.items():
            if value == predicted:
                computer_choice = key

    elif strategy == "Reinforcement Learning":
        state = st.session_state.last_move
        computer_choice = st.session_state.agent.choose_action(state)

    else:
        computer_choice = random.choice(choices)

    # ==================
    # DETERMINE WINNER
    # ==================

    if player_choice == computer_choice:
        winner = "Tie"
        reward = 0
    elif win_map[player_choice] == computer_choice:
        winner = "Player"
        reward = -1
        st.session_state.player_score += 1
    else:
        winner = "Computer"
        reward = 1
        st.session_state.computer_score += 1

    # RL Update
    if strategy == "Reinforcement Learning":
        st.session_state.agent.update(
            st.session_state.last_move,
            computer_choice,
            reward,
            player_choice
        )

    insert_game(player_choice, computer_choice, winner)

    st.session_state.last_move = player_choice

    st.success(f"Computer chose: {computer_choice}")
    st.write(f"Winner: {winner}")

st.subheader("Score")
st.write(
    f"Player: {st.session_state.player_score} | "
    f"Computer: {st.session_state.computer_score}"
)

# ==============================
# DASHBOARD SECTION
# ==============================

st.header("Statistics Dashboard")

df = get_data()

if not df.empty:

    st.subheader("Move Frequency")
    move_counts = df["player_move"].value_counts()

    fig1, ax1 = plt.subplots()
    move_counts.plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    st.subheader("Win Distribution")
    win_counts = df["winner"].value_counts()

    fig2, ax2 = plt.subplots()
    win_counts.plot(kind="bar", ax=ax2)
    st.pyplot(fig2)

    st.subheader("Recent Games")
    st.dataframe(df.tail(10))

else:
    st.info("No game data available yet.")

# ==============================
# RESET OPTION
# ==============================

if st.button("Reset Scores"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.last_move = None
    st.success("Scores Reset!")