from db_connect import get_connection

def insert_table_data(df, table_name, insert_query, columns):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        values = tuple(row[col] for col in columns)
        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
    print(f"✅ Data inserted into {table_name}.")

def insert_all_data(data):
    insert_table_data(data["aggre_insurance"], "aggregated_insurance",
        '''INSERT INTO aggregated_insurance VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Insurance_type", "Insurance_count", "Insurance_amount"]
    )

    insert_table_data(data["aggre_transaction"], "aggregated_transaction",
        '''INSERT INTO aggregated_transaction VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"]
    )

    insert_table_data(data["aggre_user"], "aggregated_user",
        '''INSERT INTO aggregated_user VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"]
    )

    insert_table_data(data["map_insurance"], "map_insurance",
        '''INSERT INTO map_insurance VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"]
    )

    insert_table_data(data["map_transaction"], "map_transaction",
        '''INSERT INTO map_transaction VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"]
    )

    insert_table_data(data["map_user"], "map_user",
        '''INSERT INTO map_user VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"]
    )

    insert_table_data(data["top_insurance"], "top_insurance",
        '''INSERT INTO top_insurance VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"]
    )

    insert_table_data(data["top_transaction"], "top_transaction",
        '''INSERT INTO top_transaction VALUES (%s, %s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"]
    )

    insert_table_data(data["top_user"], "top_user",
        '''INSERT INTO top_user VALUES (%s, %s, %s, %s, %s)''',
        ["States", "Years", "Quarter", "Pincodes", "RegisteredUser"]
    )
