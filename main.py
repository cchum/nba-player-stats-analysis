from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

app = FastAPI()

engine = create_engine(
    "postgresql+psycopg2://christinachum@localhost:5432/nba_stats"
)

@app.get("/")
def home():
    return {"message": "NBA Stats API is live"}

@app.get("/top_players")
def get_top_players():
    query = text("""
        SELECT player, team, points_per_game, efg_percent
        FROM player_stats
        ORDER BY points_per_game DESC
        LIMIT 5;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
 
    df["points_per_game"] = pd.to_numeric(df["points_per_game"], errors="coerce")
    df["efg_percent"] = pd.to_numeric(df["efg_percent"], errors="coerce")
    df = df.fillna(0)


    return df.to_dict(orient="records")
