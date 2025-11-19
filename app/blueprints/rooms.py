from app import auth
from flask import Blueprint, render_template, request, redirect, url_for, Response

from app.blueprints.utils import build_temporary_alert, build_advanced_form_error_feedback
from app.forms.rooms import EditRoomForm

from app.models.rooms import Rooms
from app.models.users import Users
from app.helpers.auth_utils import check_first_login

rooms_blueprint = Blueprint("rooms", __name__)

@rooms_blueprint.route("/zarzadzaj", methods=['POST', 'GET'])
@auth.login_required()
@check_first_login
def RoomList(*, context={"user": {"name": "Anonymous", "preffered_username": "Anonymous"}}):
    """
    Display and manage rooms:
    - GET: Show paginated list of rooms
    - POST: Update room keepers
    """
    if request.method == "POST":
        form = EditRoomForm(request.form)
        if form.validate():
        # Update room keepers from form
            editedRoom = Rooms.Edit(form.room_id.data, form.teacher_name.data)
            return build_temporary_alert(request, message="Dodano opiekuna do sali", container='#toasts')
        else:
            return build_advanced_form_error_feedback(request, form=form, message="Wystąpił błąd")

            # return redirect(url_for("rooms.RoomList"))


    # Pagination setup
    page = request.args.get('page', 1, type=int)
    perPage = 9
    query = {}
    filterName = request.args.get('filter', '').strip()
    skip = (page - 1) * perPage

    # Apply name filter if provided
    if filterName:
        query['name'] = {'$regex': f'.*{filterName}.*', '$options': 'i'}

    # Get paginated rooms
    allRooms = list(Rooms.Find(query).skip(skip).limit(perPage))

    # Calculate pagination details
    total = Rooms.TotalDocuments(query)
    totalPages = (total + perPage - 1) // perPage

    return render_template("rooms/manage.html",
                           rooms=allRooms,
                           page=page,
                           total_pages=totalPages,
                           username=context['user']['name'])