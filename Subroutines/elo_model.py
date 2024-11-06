def elo_predictor(elo_dict, fighter1_name, fighter2_name, log=True):

    f1_elo = elo_dict[fighter1_name]
    f2_elo = elo_dict[fighter2_name]

    f1_exp = 1/(1+pow(10,((f2_elo-f1_elo)/400)))
    f2_exp = 1 - f1_exp

    if log:
        print(f"In a fight between {fighter1_name} and {fighter2_name}:\n{fighter1_name}: {round(100*f1_exp,2)}% chance of winning\n{fighter2_name}: {round(100*f2_exp,2)}% chance of winning\n")
    return f1_exp, f2_exp, f1_elo, f2_elo


def elo_simple(master_frame):
    elo_dict = {}
    K_val = 40
    master_list = master_frame.to_dict(orient="records")
    for fight in master_list:
        if fight['fighter1_name'] not in elo_dict:
            elo_dict[fight['fighter1_name']] = 1000

        if fight['fighter2_name'] not in elo_dict:
            elo_dict[fight['fighter2_name']] = 1000

        f1_exp, f2_exp, f1_elo, f2_elo = elo_predictor(elo_dict, fight['fighter1_name'], fight['fighter2_name'], False)

        if fight['method'] == "nc":
            continue
        elif fight['method'] == "draw":
            f1_score = 0.5
            f2_score = 0.5
        else:
            if(fight['fighter1_name'] == fight['winner']):
                f1_score = 1
                f2_score = 0
            elif(fight['fighter2_name'] == fight['winner']):
                f1_score = 0
                f2_score = 1
            else:
                print("Some sort of mistake in elo engine")
        
        f1_elo = round(f1_elo + K_val*(f1_score-f1_exp),2)
        f2_elo = round(f2_elo + K_val*(f2_score-f2_exp),2)

        elo_dict[fight['fighter1_name']] = f1_elo
        elo_dict[fight['fighter2_name']] = f2_elo

    return elo_dict


def goat_list(elo_dict, top_ranks):
    sorted_list = sorted(elo_dict.items(), key=lambda item: item[1], reverse=True)
    print("GOATs by Elo Ranking:")
    for i in range(top_ranks):
        print(str(i+1) + ". " + sorted_list[i][0] + ", " + str(sorted_list[i][1]))
    print()