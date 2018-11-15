#!/usr/bin/env python3

from mylib.pokeconnect import PokeConnect
import csv

class Encounter(object):
    def __init__(self, pokemon, time, method, pokeball, items):
        self.pokemon = pokemon
        self.time = time
        self.method = method
        self.pokeball = pokeball
        self.items = items

    @staticmethod
    def parse(ls):
        pokemon = ls[0]
        time = ls[1]
        method = ls[2]
        pokeball = ls[3] if method == 'Phone' else None
        items = ls[4:]
        return Encounter(pokemon, time, method, pokeball, items)

    def __repr__(self):
        return '{0} encountered on {1} using {2}. Pokeball was {3} with items {4}'.format(self.pokemon, self.time, self.method, self.pokeball, self.items)

def read_pokedex(fname):
    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            yield Encounter.parse(row)

encounter_insert_sql = """
  INSERT INTO encounters(pokemon, time, method, pokeball)
  VALUES (%s,%s,%s,%s) RETURNING encounter_id;
"""

item_insert_sql = """
  INSERT INTO items(type, encounter_id)
  VALUES (%s,%s) RETURNING item_id;
"""

def insert_encounter(cur, encounter):
    print('Inserting "{0}"'.format(encounter))
    cur.execute(encounter_insert_sql, (encounter.pokemon, encounter.time, encounter.method, encounter.pokeball))
    encounter_id = cur.fetchone()[0]
    for item in encounter.items:
        cur.execute(item_insert_sql, (item, encounter_id))

def main():
    print('Populating tables from pokedex.csv')
    encounters = read_pokedex('pokedex.csv')

    with PokeConnect() as pokeconn:
        with pokeconn.cursor() as cur:
            for encounter in encounters:
                insert_encounter(cur, encounter)

if __name__ == '__main__':
    main()
