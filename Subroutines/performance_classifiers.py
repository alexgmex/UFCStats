import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore
from scipy.stats import gaussian_kde


def generate_data_dict(master_frame):
    master_dict = master_frame.copy()
    master_dict = master_dict.drop(['name','date','event_link','method','winner','weightclass','fight_link','fighter1_name','fighter1_link','fighter1_score','fighter2_name','fighter2_link','fighter2_score'],axis=1)
    master_dict = master_dict.to_dict(orient="list")

    data_dict = {}
    for key in master_dict:
        key_real = key[9:]
        if key_real not in data_dict:
            data_dict[key_real] = master_dict[key]
        else:
            data_dict[key_real] += master_dict[key]

    return data_dict


def assign_stat_scores(data_dict):
    pass


def generate_pdf_plots(data_dict):
    kde_dict = {}
    for key in data_dict:
        kde_dict[key] = gaussian_kde(data_dict[key], bw_method='scott')

    for key in data_dict:
        x_values = np.linspace(min(data_dict[key]), max(data_dict[key]),100)
        pdf_values = kde_dict[key](x_values)
        mean = np.mean(data_dict[key])
        
        plt.plot(x_values, pdf_values, label='PDF')
        plt.hist(data_dict[key], density=True, bins=10, alpha=0.5, color='gray', label='Histogram')
        plt.xlabel('Value')
        plt.ylabel('Density')
        plt.legend()
        plt.title(f"{key} PDF")
        plt.show()
        plt.close()
        print(f"Mean: {mean}")
        print(f"Confirm: {kde_dict[key](mean)}")