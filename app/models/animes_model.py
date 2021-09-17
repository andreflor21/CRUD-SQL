from flask.json import jsonify
from app.configs.exceptions import AnimeNotFound, InvalidKeysError
import psycopg2
from psycopg2 import sql
from app.configs.configs import configs
from typing import Union


class Anime():
    available_keys = ['anime', 'released_date', 'seasons']
    def __init__(self, data: Union[tuple, dict]) -> None:

        if type(data) is tuple:
            self.id, anime,released_date, self.seasons = data
            self.anime = anime.title()
            self.released_date = released_date.isoformat()

        elif type(data) is dict:
            for k, v in data.items():
                if k in self.available_keys:
                    setattr(self, k, v)
                else:
                    raise InvalidKeysError(**data)

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
    def get_one_anime(anime_id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()


        cur.execute('SELECT * FROM animes WHERE id=(%s);', (anime_id, ))

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()
        
        if not result:
            raise AnimeNotFound(anime_id)

        serialized_result = Anime(result).__dict__

        return serialized_result

    @staticmethod
    def delete_anime(anime_id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()


        cur.execute('DELETE FROM animes WHERE id=(%s) RETURNING *;', (anime_id, ))

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not result:
            raise AnimeNotFound(anime_id)

        serialized_result = Anime(result).__dict__

        return serialized_result
    
    @staticmethod
    def update_anime(anime_id, data):
        available_keys = ['anime', 'released_date', 'seasons']
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        for k, v in data.items():
            if k in available_keys:

                columns = [sql.Identifier(k) for k in data.keys()]
                values = [sql.Literal(v) for v in data.values()]

            else:
                raise InvalidKeysError(**data)

        query = sql.SQL(
             """
                UPDATE
                    animes 
                SET    
                    ({columns}) = row({values})
                WHERE
                    id={anime_id}
                RETURNING *
             """).format(id=sql.Literal(str(anime_id)),
                        columns=sql.SQL(',').join(columns),
                        values=sql.SQL(',').join(values))

        cur.execute(query)

        result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not result:
            raise AnimeNotFound(anime_id)

        serialized_data = Anime(result).__dict__

        return serialized_data        
