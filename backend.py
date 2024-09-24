import sqlite3

class ChurchDatabase:
    def __init__(self, main_window, member_id=None):
        self.root = main_window
        self.member_id = member_id
        self.conn = sqlite3.connect("church.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            birth_date TEXT NOT NULL,
            sex TEXT NOT NULL,
            street TEXT,
            number TEXT,
            neighborhood TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            cep TEXT,
            phone TEXT,
            email TEXT,
            marital_status TEXT,
            children_var TEXT,
            children_entry TEXT,
            profession TEXT,
            entry_form TEXT,
            entry_date TEXT
        )
        """)
        self.conn.commit()

    def cpf_exists(self, cpf):
        self.cur.execute("SELECT cpf FROM members WHERE cpf = ?", (cpf,))
        return self.cur.fetchone() is not None

    def save_member(self, full_name, cpf, birth_date, sex, street, number, neighborhood, city, state, country, cep,
                   phone, email, marital_status, children_var, children_entry, profession, entry_form, entry_date):
        if self.cpf_exists(cpf):
            raise ValueError("Este CPF já está registrado.")
        self.cur.execute(""" INSERT INTO members (full_name, cpf, birth_date, sex, street, number, neighborhood,
        city, state, country, cep, phone, email, marital_status, children_var, children_entry, profession, entry_form, entry_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
               (full_name, cpf, birth_date, sex, street, number, neighborhood, city, state, country, cep,
                phone, email, marital_status, children_var, children_entry, profession, entry_form, entry_date))
        self.conn.commit()

    def fetch_all_members(self):
        query = 'SELECT full_name FROM members'
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def fetch_member_info(self, name):
        query = 'SELECT * FROM members WHERE UPPER(full_name) = ?'
        cursor = self.conn.execute(query, (name.upper(),))
        return cursor.fetchone()

    def fetch_member_info_by_id(self, member_id):
        self.cur.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        return self.cur.fetchone()

    def update_member(self, member_id, full_name, cpf, birth_date, sex, street, number, neighborhood, city, state,
                      country, cep,
                      phone, email, marital_status, children_var, children_entry, profession, entry_form, entry_date):
        self.cur.execute(""" UPDATE members SET full_name = ?, cpf = ?, birth_date = ?, sex = ?, street = ?, number = ?, 
        neighborhood = ?, city = ?, state = ?, country = ?, cep = ?, phone = ?, email = ?, marital_status = ?, 
        children_var = ?, children_entry = ?, profession = ?, entry_form = ?, entry_date = ? WHERE id = ?""",
                         (full_name, cpf, birth_date, sex, street, number, neighborhood, city, state, country, cep,
                          phone, email,
                          marital_status, children_var, children_entry, profession, entry_form, entry_date, member_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

#Feito Por Murilo Abreu