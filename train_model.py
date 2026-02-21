import sqlite3
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

conn = sqlite3.connect("../database/game.db")
df = pd.read_sql("SELECT player_move FROM game_history", conn)

# Create sequential data
df["prev_move"] = df["player_move"].shift(1)
df = df.dropna()

X = pd.get_dummies(df["prev_move"])
y = df["player_move"]

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved.")