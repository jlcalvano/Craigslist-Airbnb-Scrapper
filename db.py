import sqlite3


def initalize():
    con = sqlite3.connect('database/rooms.db')
    cur = con.cursor()

    cur.execute(
    '''

        CREATE TABLE IF NOT EXISTS rooms_seen (
            room_id INTEGER PRIMARY KEY,
            date_seen TEXT
        )
        
    ''')

    return con, cur



def insert_into(room_id):
    con, cur = initalize()

    sql = f'''
        
        INSERT INTO rooms_seen (room_id,date_seen)
        VALUES({room_id},datetime('now'))

    '''
    cur.execute(sql)
    con.commit()

    return cur.lastrowid


if __name__ == "__main__":
    # execute only if run as a script
    print(insert_into(7359826833,'2021-09-12'))

    con, cur = initalize()

    cur.execute("select * from rooms_seen")
    print(cur.fetchall())
    