from flask import Request, render_template
from wtforms import Form
import uuid

from app.models.settings import Settings
from app.models.users import Users

def has_privilege(context:dict):
    if context['user']['name'] != "Anonymous":
        currentUserInfo = Users.FindOne({"name": context['user']['preferred_username']})
        currentUserPriviledge = currentUserInfo["permission"]
    else:
        currentUserPriviledge = True # False na prod
    return currentUserPriviledge

def build_advanced_form_error_feedback(request:Request, form:Form, message="Wystąpił błąd", container='#alerts'):
    error_messages = [msg for field, messages in form.errors.items() for msg in messages]
    new_uuid = uuid.uuid4()
    return render_template('alert_error_feedback.html', error_messages=error_messages, form=form, message=message, uuid=new_uuid, container=container)

def build_temporary_alert(request:Request, message:str, duration:int=3000, container='#alerts'):
    new_uuid = uuid.uuid4()
    return render_template('alert_temporary.html', message=message, uuid=new_uuid, duration=duration, container=container)

def build_basic_alert(request:Request, tag:str, message:str, container='#alerts'):
    new_uuid = uuid.uuid4()
    return render_template('alert_basic.html', message=message, uuid=new_uuid, tag=tag, container=container)
