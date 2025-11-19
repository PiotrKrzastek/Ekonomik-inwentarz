from http.client import responses

from flask import render_template, Blueprint, request, redirect, url_for, flash, Response
from werkzeug.routing import ValidationError

from app.models.users import Users
from app.models.settings import Settings
from app.helpers.auth_utils import check_first_login
from app import auth
from app.forms.users import CreateUserForm, UpdateUserForm, DeleteUserForm, UpdateGlobalFilterForm
from app.blueprints.utils import build_basic_alert, build_temporary_alert, build_advanced_form_error_feedback, has_privilege

users_blueprint = Blueprint("users", __name__)

# TODO: name: Imie, nazwisko, preferred_username: email

@users_blueprint.route("", methods=['GET'])
@auth.login_required()
@check_first_login
def main_view(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    allUsers = Users.Find()
    currentFilter = Settings.GetFilterState()
    is_htmx = request.headers.get('Hx-Request', False)
    template = "users/manage.html"
    response_context = {
        'filter_status' :currentFilter,
        'has_priviledge':has_privilege(context),
        'users': allUsers,
    }
    if not is_htmx:
        template = '/base.html'
        response_context.update({
        'username':context['user']['name'],
        'currentUser':context['user']['preferred_username'],
        'child_template':'/users/manage.html'
        })
    return render_template(template, **response_context)


@users_blueprint.route("dodaj", methods=['POST'])
@auth.login_required()
@check_first_login
def create_user(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    is_privileged = has_privilege(context)
    users = Users.Find()
    if not has_privilege(context):
        if 'Hx-Request' in request.headers.keys():
            return build_basic_alert(request, tag='error', message='Nie masz uprawnień do wykonania tej akcji')
        else:
            return Response(status=403)
    form = CreateUserForm(request.form)
    if form.validate():
        name = form.name.data
        permission = form.permission.data
        try:
            Users.Create(name, permission, None)
            return render_template('users/partials/table_content.html', has_priviledge=is_privileged, users=users)
        except ValidationError as e:
            return Response(status=500, response='Wystąpił błąd')
    else:
        return build_advanced_form_error_feedback(request, form=form, message='Wystąpił błąd')

@users_blueprint.route("edytuj", methods=['POST'])
@auth.login_required()
@check_first_login
def update_user(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    if not has_privilege(context):
        if 'Hx-Request' in request.headers.keys():
            return build_basic_alert(request, tag='error', message='Nie masz uprawnień do wykonania tej akcji')
        else:
            return Response(status=403)
    form = UpdateUserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        permission = form.permission.data
        try:
            user_object = Users.FindBy_ID(user_id)
            Users.EditPrviledges(user_object["name"], permission)
            return build_temporary_alert(request, message='Edycja uprawnień użytkownika udana.', container='#toasts')
        except ValidationError as e:
            return Response(status=500, response="Wystąpił błąd")
    else:
        return build_advanced_form_error_feedback(request, form=form, message='Wystąpił błąd')

@users_blueprint.route("usun", methods=['POST'])
@auth.login_required()
@check_first_login
def delete_user(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    if not has_privilege(context):
        if 'Hx-Request' in request.headers.keys():
            return build_basic_alert(request, tag='error', message='Nie masz uprawnień do wykonania tej akcji')
        else:
            return Response(status=403)
    form = DeleteUserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        try:
            Users.DeleteBy_ID(user_id)
            return Response(status=200)
        except ValidationError as e:
            return Response(status=500, response='Wystąpił błąd')
    else:
        return build_advanced_form_error_feedback(request, form=form, message='Wystąpił błąd')


@users_blueprint.route("filtracja", methods=['GET', 'POST'])
@auth.login_required()
@check_first_login
def manage_global_filter_status(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    if not has_privilege(context):
        if 'Hx-Request' in request.headers.keys():
            return build_basic_alert(request, tag='error', message='Nie masz uprawnień do wykonania tej akcji')
        else:
            return Response(status=403)
    if request.method == 'GET':
        filter_status = Settings.GetFilterState()
        return Response(status=200)
    if request.method == "POST":
        form = UpdateGlobalFilterForm(request.form)
        if form.validate():
            is_active = form.is_active.data
            try:
                Settings.UpdateFilter(state=is_active)
                return build_temporary_alert(request, message=f'Zmieniono status filtra.', container='#toasts')
            except ValidationError as Ex:
                return Response(status=500, response="Coś poszło nie tak")
        else:
            return  build_advanced_form_error_feedback(request, form=form)


@users_blueprint.route("spinner", methods=['GET'])
def spinner(*, context={"user": {"name": "Anonymous", "preferred_username": "Anonymous"}}):
    import time
    time.sleep(5)
    return Response(status=200)
