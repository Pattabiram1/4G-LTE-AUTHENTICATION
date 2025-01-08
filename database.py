import sqlite3
import random

# SQL Queries as constants
CREATE_UE_TABLE = '''
    CREATE TABLE IF NOT EXISTS ue (
        imsi TEXT PRIMARY KEY,
        rand INTEGER,
        k INTEGER
    )
'''

CREATE_HSS_TABLE = '''
    CREATE TABLE IF NOT EXISTS hss (
        imsi TEXT PRIMARY KEY,
        rand INTEGER,
        k INTEGER
    )
'''

CREATE_ENB_TABLE = '''
    CREATE TABLE IF NOT EXISTS enb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imsi TEXT,
        rand INTEGER,
        res INTEGER,
        FOREIGN KEY (imsi) REFERENCES ue (imsi)
    )
'''

CREATE_MME_TABLE = '''
    CREATE TABLE IF NOT EXISTS mme (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imsi TEXT,
        rand INTEGER,
        xres INTEGER,
        FOREIGN KEY (imsi) REFERENCES hss (imsi)
    )
'''

INSERT_UE_DATA = '''
    INSERT OR IGNORE INTO ue (imsi, rand, k) VALUES (?, ?, ?)
'''

INSERT_HSS_DATA = '''
    INSERT OR IGNORE INTO hss (imsi, rand, k) VALUES (?, ?, ?)
'''

# Function to create databases and tables
def create_databases():
    try:
        # Create UE database
        with sqlite3.connect('ue_database.db') as ue_conn:
            ue_cursor = ue_conn.cursor()
            ue_cursor.execute(CREATE_UE_TABLE)
            ue_data = [
                ("123456789012345", random.randint(10000000, 99999999), random.randint(10000000, 99999999)),
                ("987654321098765", random.randint(10000000, 99999999), random.randint(10000000, 99999999)),
                ("112233445566778", random.randint(10000000, 99999999), random.randint(10000000, 99999999)),
                ("223344556677889", random.randint(10000000, 99999999), random.randint(10000000, 99999999)),  # Different IMSI
            ]
            ue_cursor.executemany(INSERT_UE_DATA, ue_data)
            ue_conn.commit()

        # Create HSS database
        with sqlite3.connect('hss_database.db') as hss_conn:
            hss_cursor = hss_conn.cursor()
            hss_cursor.execute(CREATE_HSS_TABLE)
            hss_data = [
                ("123456789012345", 12345678, 11111111),  # Same rand, k
                ("987654321098765", 12345678, 22222222),  # Same rand, different k
                ("112233445566778", 87654321, 33333333),  # Different rand, k
                ("223344556677889", 87654321, 44444444),  # Different rand, k
            ]
            hss_cursor.executemany(INSERT_HSS_DATA, hss_data)
            hss_conn.commit()

        # Create empty eNodeB database
        with sqlite3.connect('enb_database.db') as enb_conn:
            enb_cursor = enb_conn.cursor()
            enb_cursor.execute(CREATE_ENB_TABLE)
            enb_conn.commit()

        # Create empty MME database
        with sqlite3.connect('mme_database.db') as mme_conn:
            mme_cursor = mme_conn.cursor()
            mme_cursor.execute(CREATE_MME_TABLE)
            mme_conn.commit()

        print("Databases and tables created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred while creating databases: {e}")

# Main function to run the database creation program
if __name__ == "__main__":
    create_databases()
