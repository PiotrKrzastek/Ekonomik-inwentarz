from app import auth, db
from app.helpers.auth_utils import check_first_login
from app.models.rooms import Rooms
from flask import render_template, Blueprint, session, url_for, request
from itertools import groupby
from operator import itemgetter

# Create a Flask Blueprint for the application routes
home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
@auth.login_required()
@check_first_login
def Home(*, context={"user": {"name": "Anonymous", "preffered_username": "Anonymous"}}):
    """Render the main home page with all rooms"""
    rooms = mDB.db.rooms
    result = rooms.aggregate([
        {"$match": {"floor": {"$ne": None}}},  # pomiń dokumenty bez 'floor'
        {"$group": {
            "_id": "$floor",
            "items": {"$push": "$$ROOT"}
        }}
    ])
    rooms = {g["_id"]: g["items"] for g in result}
    is_htmx = request.headers.get('Hx-Request', False)
    template = "home/home.html"
    response_context = {
        'rooms': rooms,
    }
    if not is_htmx:
        template = '/base.html'
        response_context.update({
        'username':context['user']['name'],
        'currentUser':context['user']['preffered_username'],
        'child_template':"home/home.html"
        })
    return render_template(template, **response_context)