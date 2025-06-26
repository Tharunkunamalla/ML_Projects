import os
import json
import pandas as pd

# ✅ Set your pulse base path here:
base_path = "C:/Users/THARUN KUNAMALLA/CODE LANG/ML_Projects/Phone_pe/pulse/data"

# ✅ Function to standardize state names
def clean_states(df, col="States"):
    df[col] = df[col].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
    df[col] = df[col].str.replace("-", " ")
    df[col] = df[col].str.title()
    df[col] = df[col].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return df

# ✅ Output folder
output_folder = "phonepe_extracted_csv"
os.makedirs(output_folder, exist_ok=True)

# ------------------ AGGREGATED TRANSACTION ------------------ #
path1 = os.path.join(base_path, "aggregated/transaction/country/india/state")
columns1 = {"States":[], "Years":[], "Quarter":[], "Transaction_type":[], "Transaction_count":[],"Transaction_amount":[] }

for state in os.listdir(path1):
    cur_states = os.path.join(path1, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["transactionData"]:
                    columns1["Transaction_type"].append(i["name"])
                    columns1["Transaction_count"].append(i["paymentInstruments"][0]["count"])
                    columns1["Transaction_amount"].append(i["paymentInstruments"][0]["amount"])
                    columns1["States"].append(state)
                    columns1["Years"].append(year)
                    columns1["Quarter"].append(int(file.strip(".json")))

df1 = pd.DataFrame(columns1)
df1 = clean_states(df1)
df1.to_csv(f"{output_folder}/aggregated_transaction.csv", index=False)

# ------------------ AGGREGATED USER ------------------ #
path2 = os.path.join(base_path, "aggregated/user/country/india/state")
columns2 = {"States":[], "Years":[], "Quarter":[], "Brands":[],"Transaction_count":[], "Percentage":[] }

for state in os.listdir(path2):
    cur_states = os.path.join(path2, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                try:
                    for i in data["data"]["usersByDevice"]:
                        columns2["Brands"].append(i["brand"])
                        columns2["Transaction_count"].append(i["count"])
                        columns2["Percentage"].append(i["percentage"])
                        columns2["States"].append(state)
                        columns2["Years"].append(year)
                        columns2["Quarter"].append(int(file.strip(".json")))
                except:
                    pass

df2 = pd.DataFrame(columns2)
df2 = clean_states(df2)
df2.to_csv(f"{output_folder}/aggregated_user.csv", index=False)

# ------------------ AGGREGATED INSURANCE ------------------ #
path3 = os.path.join(base_path, "aggregated/insurance/country/india/state")
columns3 = {"States":[], "Years":[], "Quarter":[], "Insurance_type":[], "Insurance_count":[],"Insurance_amount":[] }

for state in os.listdir(path3):
    cur_states = os.path.join(path3, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["transactionData"]:
                    columns3["Insurance_type"].append(i["name"])
                    columns3["Insurance_count"].append(i["paymentInstruments"][0]["count"])
                    columns3["Insurance_amount"].append(i["paymentInstruments"][0]["amount"])
                    columns3["States"].append(state)
                    columns3["Years"].append(year)
                    columns3["Quarter"].append(int(file.strip(".json")))

df3 = pd.DataFrame(columns3)
df3 = clean_states(df3)
df3.to_csv(f"{output_folder}/aggregated_insurance.csv", index=False)

# ------------------ MAP TRANSACTION ------------------ #
path4 = os.path.join(base_path, "map/transaction/hover/country/india/state")
columns4 = {"States":[], "Years":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}

for state in os.listdir(path4):
    cur_states = os.path.join(path4, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["hoverDataList"]:
                    columns4["District"].append(i["name"])
                    columns4["Transaction_count"].append(i["metric"][0]["count"])
                    columns4["Transaction_amount"].append(i["metric"][0]["amount"])
                    columns4["States"].append(state)
                    columns4["Years"].append(year)
                    columns4["Quarter"].append(int(file.strip(".json")))

df4 = pd.DataFrame(columns4)
df4 = clean_states(df4)
df4.to_csv(f"{output_folder}/map_transaction.csv", index=False)

# ------------------ MAP USER ------------------ #
path5 = os.path.join(base_path, "map/user/hover/country/india/state")
columns5 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[] }

for state in os.listdir(path5):
    cur_states = os.path.join(path5, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for k, v in data["data"]["hoverData"].items():
                    columns5["Districts"].append(k)
                    columns5["RegisteredUser"].append(v["registeredUsers"])
                    columns5["AppOpens"].append(v["appOpens"])
                    columns5["States"].append(state)
                    columns5["Years"].append(year)
                    columns5["Quarter"].append(int(file.strip(".json")))

df5 = pd.DataFrame(columns5)
df5 = clean_states(df5)
df5.to_csv(f"{output_folder}/map_user.csv", index=False)

# ------------------ MAP INSURANCE ------------------ #
path6 = os.path.join(base_path, "map/insurance/hover/country/india/state")
columns6 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "Transaction_count":[],"Transaction_amount":[] }

for state in os.listdir(path6):
    cur_states = os.path.join(path6, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["hoverDataList"]:
                    columns6["Districts"].append(i["name"])
                    columns6["Transaction_count"].append(i["metric"][0]["count"])
                    columns6["Transaction_amount"].append(i["metric"][0]["amount"])
                    columns6["States"].append(state)
                    columns6["Years"].append(year)
                    columns6["Quarter"].append(int(file.strip(".json")))

df6 = pd.DataFrame(columns6)
df6 = clean_states(df6)
df6.to_csv(f"{output_folder}/map_insurance.csv", index=False)

# ------------------ TOP TRANSACTION ------------------ #
path7 = os.path.join(base_path, "top/transaction/country/india/state")
columns7 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[],"Transaction_amount":[]}

for state in os.listdir(path7):
    cur_states = os.path.join(path7, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["pincodes"]:
                    columns7["Pincodes"].append(i["entityName"])
                    columns7["Transaction_count"].append(i["metric"]["count"])
                    columns7["Transaction_amount"].append(i["metric"]["amount"])
                    columns7["States"].append(state)
                    columns7["Years"].append(year)
                    columns7["Quarter"].append(int(file.strip(".json")))

df7 = pd.DataFrame(columns7)
df7 = clean_states(df7)
df7.to_csv(f"{output_folder}/top_transaction.csv", index=False)

# ------------------ TOP USER ------------------ #
path8 = os.path.join(base_path, "top/user/country/india/state")
columns8 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUser":[]}

for state in os.listdir(path8):
    cur_states = os.path.join(path8, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["pincodes"]:
                    columns8["Pincodes"].append(i["name"])
                    columns8["RegisteredUser"].append(i["registeredUsers"])
                    columns8["States"].append(state)
                    columns8["Years"].append(year)
                    columns8["Quarter"].append(int(file.strip(".json")))

df8 = pd.DataFrame(columns8)
df8 = clean_states(df8)
df8.to_csv(f"{output_folder}/top_user.csv", index=False)

# ------------------ TOP INSURANCE ------------------ #
path9 = os.path.join(base_path, "top/insurance/country/india/state")
columns9 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in os.listdir(path9):
    cur_states = os.path.join(path9, state)
    for year in os.listdir(cur_states):
        cur_years = os.path.join(cur_states, year)
        for file in os.listdir(cur_years):
            with open(os.path.join(cur_years, file), "r") as f:
                data = json.load(f)
                for i in data["data"]["pincodes"]:
                    columns9["Pincodes"].append(i["entityName"])
                    columns9["Transaction_count"].append(i["metric"]["count"])
                    columns9["Transaction_amount"].append(i["metric"]["amount"])
                    columns9["States"].append(state)
                    columns9["Years"].append(year)
                    columns9["Quarter"].append(int(file.strip(".json")))

df9 = pd.DataFrame(columns9)
df9 = clean_states(df9)
df9.to_csv(f"{output_folder}/top_insurance.csv", index=False)

print("✅ All CSVs have been saved in folder:", output_folder)
