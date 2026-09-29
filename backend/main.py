from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import uuid

from pydantic import BaseModel

from f1_data_gen import generate

class Guess(BaseModel): # pydantic model for data coming towards the server
    user_id: str
    round_id: str
    guess: list[str]

app = FastAPI()

# allows the fastAPI backend to accept requests from the browser (blocked by default)
app.add_middleware(CORSMiddleware,
                   allow_origins = ["*"],
                   allow_methods = ["*"],
                   allow_headers = ["*"],)


rounds = {} # responsible for storing the session's answers
player_level = {} # responsible for authorative player's level
# won = False # As this gets assigned later not referenced we do not need it here. No need to use as a global
winning_level = 10 # The level needed to win the game

@app.get("/start") # use GET for when the client fetches data
def start():
    user_id = str(uuid.uuid4())
    level = 1
    player_level[user_id] = level
    return {"user_id": user_id}

@app.get("/round")
def get_round(user_id: str): # taking in argument (in URL)
    race_name, year, drivers, results = generate(player_level.get(user_id))
    round_id = str(uuid.uuid4()) # generate a roundID
    rounds[round_id] = results
    return {"race_name": race_name, 
            "year": year,
            "drivers": drivers,
            "results_id": round_id,
            "player_level": player_level[user_id]} # returning data back to be displayed/stored

@app.post("/guess") # use POST when updating server side
def post_guess(data: Guess): # building a BODY to enter in data -> List is big, structed so cannot pass through as too complex

    if data.round_id not in rounds: # stores round_id as a key in rounds. The value is results which is checked later! smart implementation
        raise HTTPException(status_code=404, detail="round not found")
    results = rounds[data.round_id]
    rounds.pop(data.round_id) # remove the entry in rounds

    if data.guess == results:
        level = player_level.get(data.user_id) 
        player_level[data.user_id] = level + 1 # increase the level on server side

        won = player_level[data.user_id] > winning_level # if our user passes the winning level

        return {"pass": True,
                "won": won}
    else:
        player_level.pop(data.user_id) # remove the players level as their game is over
        return {"pass": False,
                "won": False} 
    
                