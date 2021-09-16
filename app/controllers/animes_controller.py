from flask import request
from app.models.animes_model import Anime
from psycopg2.errors import UniqueViolation
from app.configs.exceptions import AnimeNotFound, InvalidKeysError

def get_create():
    if request.method == "GET":
       animes_list = Anime.get_all()

       return {"data": animes_list}, 200
    
    elif request.method == "POST":
        data = request.json

        try: 
            anime = Anime(data)
            new_anime = anime.create_anime()

            return new_anime, 201

        except UniqueViolation as err:

            return {"message": f'Anime {data["anime"].title()} already exists'}, 409

        except InvalidKeysError as err:

            return err.message, 422

def filter(anime_id: int):
    try:
        anime = Anime.get_one_anime(anime_id)

        return anime, 200
    
    except AnimeNotFound as err:

        return err.message, 404


def update(anime_id: int):
    try:
        data = request.json
        updated_anime = Anime.update_anime(anime_id, data)
        
        return updated_anime, 200
    
    except InvalidKeysError as err:
        
        return err.message, 422

    except AnimeNotFound as err:
        
        return err.message, 404


def delete(anime_id: int):
    try: 
        deleted_anime = Anime.delete_anime(anime_id)

        return "", 204

    except AnimeNotFound as err:

        return err.message, 404
