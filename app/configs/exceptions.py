class AnimeNotFound(Exception):
    def __init__(self, id) -> None:

        self.message = {
            "message": f'Anime with id {id} not found.'
        }
        super().__init__(self.message)

class InvalidKeysError(Exception):

    def __init__(self, **kwargs) -> None:
        available_keys = ['anime', 'released_date', 'seasons']

        self.message = {
            "available_keys": available_keys,
            "wrong_keys_sended": [key for key in kwargs if key not in available_keys]
        }
        super().__init__(self.message)