import sqlite3 as sq

list_current_keys = ['birth_year', 'eye_color', 'gender', 'hair_color', 'height', 'homeworld', 'mass', 'name',
                     'skin_color', 'films', 'species', 'starships', 'vehicles']


def sql_start():
    global base, cur
    base = sq.connect('people_star_wars.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
        base.execute("""CREATE TABLE IF NOT EXISTS people(
                     id INT PRIMARY KEY,
                     birth_year TEXT,
                     eye_color TEXT,
                     gender TEXT,
                     hair_color TEXT,
                     height TEXT,
                     homeworld TEXT,
                     mass TEXT,
                     name TEXT,
                     films TEXT,
                     species TEXT,
                     starships TEXT,
                    vehicles TEXT,
                     skin_color TEXT);
                     """)

        base.commit()


async def load_one_people(people):
    data = (
    people["id"], people["birth_year"], people["eye_color"], people["gender"], people["hair_color"], people["height"],
    people["homeworld"],
    people["mass"], people["name"], people["films"], people["species"], people["starships"], people["vehicles"],
    people["skin_color"])
    cur.execute(f'''INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', data)
    base.commit()
