import sqlite3

db = sqlite3.connect("db.sqlite")
c = db.cursor()
p = print('date_off')
c.execute('UPDATE diia SET date_ = ? WHERE id = ?', (f"{p}", f"{print('id')}"))
db.commit()
c.execute(f"SELECT * FROM diia WHERE id ={p}")