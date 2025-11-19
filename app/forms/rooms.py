from wtforms import Form, StringField, validators

class EditRoomForm(Form):
    room_id = StringField(validators=[validators.InputRequired(message='ID pomieszczenia nie może być puste'), validators.Length(max=500)])
    teacher_name = StringField(validators=[validators.Length(max=400)])