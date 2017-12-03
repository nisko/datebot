import sqlite3


def format_output(res):
    format_str = ''
    for ob in res:
        format_str += str(ob[0]) + '.' + str(ob[1]) + ' ' + ob[2] + '\n'

    return format_str

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def add_date(day, month, description, chat_id):
    con = create_connection(str(chat_id) + ".db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS date (id INTEGER PRIMARY KEY, day INTEGER, month INTEGER, description TEXT)')
    con.commit()

    cur.execute('INSERT INTO date (day, month, description) VALUES(?,?,?)', (day, month, description))

    con.commit()
    con.close()

    return True

def get_all_date(chat_id):
    con = create_connection(str(chat_id) + ".db")
    cur = con.cursor()
    cur.execute('select day, month, description from date')

    res = cur.fetchall()

    con.close()

    return format_output((res))


def get_date_by_month(month, chat_id):
    con = create_connection(str(chat_id) + ".db")
    cur = con.cursor()

    cur.execute('select day, month, description from date where month = ?', (month,))

    res = cur.fetchall()

    con.close()

    return format_output((res))
