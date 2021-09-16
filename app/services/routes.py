from flask import Blueprint, request
from app.controllers.animes_controller import get_create, filter, update, delete

bp_animes = Blueprint('bp_animes', __name__, url_prefix='/animes')

bp_animes.post('')(get_create)
bp_animes.get('')(get_create)
bp_animes.get('/<int: anime_id>')(filter)
bp_animes.patch('/<int: anime_id>')(update)
bp_animes.delete('/<int: anime_id>')(delete)
