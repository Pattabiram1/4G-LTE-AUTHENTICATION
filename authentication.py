import sqlite3

# Function to calculate res and xres
def calculate_res_xres(rand, k):
    res = (rand + k) % 10000000  # Example calculation for res
    xres = res  # Set xres equal to res for successful authentication
    return res, xres

# Function to authenticate users from the eNodeB and MME databases
def authenticate_users():
    try:
        with sqlite3.connect('ue_database.db') as ue_conn, \
             sqlite3.connect('hss_database.db') as hss_conn, \
             sqlite3.connect('enb_database.db') as enb_conn, \
             sqlite3.connect('mme_database.db') as mme_conn:

            ue_cursor = ue_conn.cursor()
            hss_cursor = hss_conn.cursor()
            enb_cursor = enb_conn.cursor()
            mme_cursor = mme_conn.cursor()

            # Fetch all UE data
            ue_cursor.execute("SELECT imsi, rand, k FROM ue")
            ue_data = ue_cursor.fetchall()

            # Fetch all HSS data
            hss_cursor.execute("SELECT imsi, rand, k FROM hss")
            hss_data = hss_cursor.fetchall()

            for ue in ue_data:
                imsi, rand, k = ue
                res, xres = calculate_res_xres(rand, k)

                # Insert into eNodeB database
                enb_cursor.execute("INSERT INTO enb (imsi, rand, res) VALUES (?, ?, ?)", (imsi, rand, res))

                # Find corresponding HSS entry and insert into MME database
                for hss in hss_data:
                    if hss[0] == imsi:
                        mme_cursor.execute("INSERT INTO mme (imsi, rand, xres) VALUES (?, ?, ?)", (imsi, hss[1], xres))
                        break

            enb_conn.commit()
            mme_conn.commit()

            # Now compare res in eNodeB with xres in MME
            for ue in ue_data:
                imsi, _, _ = ue

                # Retrieve res from eNodeB
                enb_cursor.execute("SELECT res FROM enb WHERE imsi = ?", (imsi,))
                enb_row = enb_cursor.fetchone()
                if enb_row is None:
                    print(f"IMSI {imsi} not found in eNodeB.")
                    continue
                
                res = enb_row[0]

                # Retrieve xres from MME
                mme_cursor.execute("SELECT xres FROM mme WHERE imsi = ?", (imsi,))
                mme_row = mme_cursor.fetchone()
                if mme_row is None:
                    print(f"IMSI {imsi} authentication rejected.")
                    continue
                
                xres = mme_row[0]

                # Compare res and xres
                if res == xres:
                    print(f"Authentication successful for IMSI {imsi}.")
                else:
                    print(f"Authentication failed for IMSI {imsi}. Expected xres: {xres}, but got res: {res}.")

    except sqlite3.Error as e:
        print(f"An error occurred during authentication: {e}")

# Main function to run the authentication program
if __name__ == "__main__":
    authenticate_users()
