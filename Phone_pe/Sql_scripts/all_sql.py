from load_dataframes import load_all_data
from create_tables import create_tables
from insert_data import insert_all_data

if __name__ == "__main__":
    print("Starting PhonePe DB setup...")

    data = load_all_data()
    create_tables()
    insert_all_data(data)

    print("All tasks completed successfully!")
