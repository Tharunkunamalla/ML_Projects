import pandas as pd
import os

def load_all_data():
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "phonepe_extracted_csv/")

    data = {
        "aggre_transaction": pd.read_csv(base_path + "aggregated_transaction.csv"),
        "aggre_user": pd.read_csv(base_path + "aggregated_user.csv"),
        "aggre_insurance": pd.read_csv(base_path + "aggregated_insurance.csv"),

        "map_transaction": pd.read_csv(base_path + "map_transaction.csv"),
        "map_user": pd.read_csv(base_path + "map_user.csv"),
        "map_insurance": pd.read_csv(base_path + "map_insurance.csv"),

        "top_transaction": pd.read_csv(base_path + "top_transaction.csv"),
        "top_user": pd.read_csv(base_path + "top_user.csv"),
        "top_insurance": pd.read_csv(base_path + "top_insurance.csv"),
    }

    return data
