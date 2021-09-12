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

def does_id_exist(room_id):
    con, cur = initalize()

    cur.execute(f"select * from rooms_seen where room_id = {room_id}")
    
    if cur.fetchone():
        return True
    else:
        return False


if __name__ == "__main__":
    # execute only if run as a script
    print(insert_into(7359826833))

    con, cur = initalize()

    cur.execute(f"select * from rooms_seen where room_id = {7359826831}")
    
    print(cur.fetchone())
    