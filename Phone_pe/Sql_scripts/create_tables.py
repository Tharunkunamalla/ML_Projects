from db_connect import get_connection

def create_tables():
    queries = {
        "aggregated_insurance": '''CREATE TABLE IF NOT EXISTS aggregated_insurance (
            States VARCHAR(50), Years INT, Quarter INT,
            Insurance_type VARCHAR(50), Insurance_count BIGINT, Insurance_amount BIGINT)''',

        "aggregated_transaction": '''CREATE TABLE IF NOT EXISTS aggregated_transaction (
            States VARCHAR(50), Years INT, Quarter INT,
            Transaction_type VARCHAR(50), Transaction_count BIGINT, Transaction_amount BIGINT)''',

        "aggregated_user": '''CREATE TABLE IF NOT EXISTS aggregated_user (
            States VARCHAR(50), Years INT, Quarter INT,
            Brands VARCHAR(50), Transaction_count BIGINT, Percentage FLOAT)''',

        "map_insurance": '''CREATE TABLE IF NOT EXISTS map_insurance (
            States VARCHAR(50), Years INT, Quarter INT,
            District VARCHAR(50), Transaction_count BIGINT, Transaction_amount FLOAT)''',

        "map_transaction": '''CREATE TABLE IF NOT EXISTS map_transaction (
            States VARCHAR(50), Years INT, Quarter INT,
            District VARCHAR(50), Transaction_count BIGINT, Transaction_amount FLOAT)''',

        "map_user": '''CREATE TABLE IF NOT EXISTS map_user (
            States VARCHAR(50), Years INT, Quarter INT,
            Districts VARCHAR(50), RegisteredUser BIGINT, AppOpens BIGINT)''',

        "top_insurance": '''CREATE TABLE IF NOT EXISTS top_insurance (
            States VARCHAR(50), Years INT, Quarter INT,
            Pincodes INT, Transaction_count BIGINT, Transaction_amount BIGINT)''',

        "top_transaction": '''CREATE TABLE IF NOT EXISTS top_transaction (
            States VARCHAR(50), Years INT, Quarter INT,
            Pincodes INT, Transaction_count BIGINT, Transaction_amount BIGINT)''',

        "top_user": '''CREATE TABLE IF NOT EXISTS top_user (
            States VARCHAR(50), Years INT, Quarter INT,
            Pincodes INT, RegisteredUser BIGINT)'''
    }

    conn = get_connection()
    cursor = conn.cursor()

    for name, query in queries.items():
        cursor.execute(query)

    conn.commit()
    conn.close()
    print("✅ All tables created.")
