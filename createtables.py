#!/usr/bin/env python3
from mylib.pokeconnect import PokeConnect

commands = [
        """
        CREATE TABLE encounters (
          encounter_id SERIAL PRIMARY KEY,
          pokemon VARCHAR(255) NOT NULL,
          time TIMESTAMPTZ NOT NULL,
          method VARCHAR(255) NOT NULL,
          pokeball VARCHAR(255))
        """,
        """
        CREATE TABLE items (
          item_id SERIAL PRIMARY KEY,
          type VARCHAR(255),
          encounter_id INTEGER NOT NULL,
          FOREIGN KEY(encounter_id)
            REFERENCES encounters (encounter_id)
            ON DELETE CASCADE
        )
        """
]

def main():
    with PokeConnect() as pokeconn:
        with pokeconn.cursor() as cur:
            print('Excuting commands')
            for command in commands:
                print(command)
                cur.execute(command)

if __name__ == '__main__':
    main()
