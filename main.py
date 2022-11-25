import psycopg2


def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS Information(
      id SERIAL PRIMARY KEY,
      first_name VARCHAR(40) UNIQUE,
      last_name VARCHAR(40) UNIQUE,
      email VARCHAR(40) UNIQUE
      );
      ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS klient_phone(
      id SERIAL PRIMARY KEY,
      phone VARCHAR(40),
      information_id INTEGER NOT NULL REFERENCES Information(id)
      );
      ''')


def add_client(first_name, last_name, email, phone):
    cur.execute('''
    INSERT INTO information(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
    ''', (first_name, last_name, email))
    res = cur.fetchone()
    cur.execute('''
    INSERT INTO klient_phone(phone, information_id) VALUES(%s, %s); 
    ''', (phone, res,))


def add_phone(name, phone):
    cur.execute(''' 
    SELECT id FROM Information WHERE last_name=%s;
    ''', (name,))
    res = cur.fetchone()[0]
    cur.execute('''
    INSERT INTO klient_phone(phone, information_id) VALUES(%s, %s);
    ''', (phone, res))


def update_client(name, last_name, new_name, new_last_name, new_email):
    cur.execute('''
    SELECT id FROM Information WHERE first_name=%s AND last_name=%s;
    ''', (name, last_name))
    res = cur.fetchone()[0]
    cur.execute('''
    UPDATE Information SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
    ''', (new_name, new_last_name, new_email, res))


def delete_phone(name, last_name):
    cur.execute('''
    SELECT id FROM Information WHERE first_name=%s AND last_name=%s;
    ''', (name, last_name,))
    res = cur.fetchone()[0]
    cur.execute('''
    DELETE FROM klient_phone WHERE id=%s
    ''', (res,))


def delete_client(name,last_name):
    cur.execute('''
    SELECT id FROM Information WHERE first_name=%s AND last_name=%s;
    ''', (name, last_name))
    res = cur.fetchone()[0]
    cur.execute('''
    DELETE FROM klient_phone WHERE information_id=%s;
    ''', (res,))
    cur.execute('''
    DELETE FROM Information WHERE first_name=%s AND last_name=%s;
    ''', (name, last_name))


def find_client(name, last_name, email, phone_num):
    cur.execute('''
    SELECT first_name, last_name, email, kp.phone FROM Information i
    LEFT JOIN klient_phone kp ON kp.information_id = i.id
    WHERE first_name=%s AND last_name=%s AND email=%s AND kp.phone=%s;
    ''', (name, last_name, email, phone_num))
    res = cur.fetchone()
    print(res)


if __name__ == '__main__':
    with psycopg2.connect(database='SQLpy', user='postgres', password='15wvfus89') as conn:
        with conn.cursor() as cur:
            cur.execute('''
              DROP TABLE klient_phone;
              DROP TABLE Information
              ''')
            create_table()
            add_client('Audrey', 'Smith', 'smith.a@gmail.com', '+420608345177')
            add_client('Alison', 'Dunlop', 'dun.al@hotmail.com', '+420775365145')
            add_client('Melany', 'Cleo', 'cleo.melany@gmail.com', '+420721567544')
            add_client('Thomas', 'Cook', 'cook.th@hotmail.com', '+420602252787')
            add_client('Lesley', 'Ellers', 'miss.ellers@hotmail.com', '+420777187777')
            add_client('Martin', 'Freeman', 'marty.free@gmail.com', '+42060660352')
            add_phone('Smith', '+420602272666')
            add_phone('Smith', '+420777875355')
            add_phone('Smith', '+420606879456')
            add_phone('Cleo', '+420773183478')
            add_phone('Ellers', '+420773264355')
            add_phone('Freeman', '+420774555178')
            update_client('Melany', 'Cleo', 'Melany', 'Seeto', 'seeto.mel@gmail.com')
            update_client('Martin', 'Freeman', 'Martin', 'Freeman', 'martin.freeman@hotmail.com')
            update_client('Alison', 'Dunlop', 'Alison', 'Moore', 'moore.al@gmail.com')
            delete_phone('Audrey', 'Smith')
            delete_phone('Alison', 'Moore')
            delete_phone('Melany', 'Seeto')
            delete_client('Melany', 'Seeto')
            find_client('Audrey', 'Smith', 'smith.a@gmail.com', '+420777875355')

            conn.commit()