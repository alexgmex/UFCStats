import pandas as pd

def construct_dataframe(events, saved_filename):
    master_list = []
    for i in range(len(events)):
        for j in range(len(events[i].fights)):
            event_dict = events[i].__dict__.copy()
            fight_dict = events[i].fights[j].__dict__.copy()
            fighter1_dict = {f'fighter1_{key}': value for key, value in events[i].fights[j].fighter1_stats.__dict__.items()}
            fighter2_dict = {f'fighter2_{key}': value for key, value in events[i].fights[j].fighter2_stats.__dict__.items()}

            event_dict.pop('fights')
            fight_dict.pop('fighter1_stats')
            fight_dict.pop('fighter2_stats')

            master_list.append(event_dict | fight_dict | fighter1_dict | fighter2_dict)

    file_frame = pd.read_csv(saved_filename)
    master_frame = pd.DataFrame(master_list)
    master_frame = pd.concat([master_frame, file_frame], ignore_index=True)

    master_frame.to_csv('master.csv', index=False)
    return master_frame