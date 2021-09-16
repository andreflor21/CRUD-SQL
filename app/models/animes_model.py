import psycopg2
from psycopg2 import sql
from ..configs import configs
from typing import Union


class Anime():
    def __init__(self, data: Union[tuple, dict]) -> None:

        if type(data) is tuple:
            self.id, self.anime, self.released_date, self.seasons = data
        elif type(data) is dict:
            for k, v in data:
                setattr(self, k, v)

    def create_anime(self):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        columns = [sql.Identifier(key) for key in self.__dict__.keys()]
        values = [sql.Literal(value) for value in self.__dict__.values()]

        query = sql.SQL(
             """
                INSERT INTO
                    animes (id, {columns})
                VALUES
                    (DEFAULT, {values})
                RETURNING *
             """).format(columns=sql.SQL(',').join(columns),
                         values=sql.SQL(',').join(values))

        cur.execute(query)

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        serialized_data = Anime(result).__dict__     

        return serialized_data


    @staticmethod
    def get_all():
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()


        cur.execute('SELECT * FROM animes;')

        result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

        serialized_result = [Anime(anime_data).__dict__ for anime_data in result]

        return serialized_result 
    
    @staticmethod
    def get_one_anime(id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()


        cur.execute('SELECT * FROM animes WHERE id=(%s);', (id, ))

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        serialized_result = Anime(result).__dict__

        return serialized_result

    @staticmethod
    def delete_anime(id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()


        cur.execute('DELETE FROM animes WHERE id=(%s) RETURNING *;', (id, ))

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not result:
            raise IndexError

        serialized_result = Anime(result).__dict__

        return serialized_result
    
    @staticmethod
    def update_anime(id, data):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
             """
                UPDATE
                    animes 
                SET    
                    ({columns}) = row({values})
                WHERE
                    id={id}
                RETURNING *
             """).format(id=sql.Literal(str(id)),
                        columns=sql.SQL(',').join(columns),
                        values=sql.SQL(',').join(values))

        cur.execute(query)

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not result:
            raise IndexError

        serialized_data = Anime(result).__dict__

        return serialized_data        
