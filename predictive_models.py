import pandas as pd

def elo_simple(master_frame):
    elo_dict = {}
    master_list = master_frame.to_dict(orient="records")
    for fight in master_list:
        print(fight['winner'])