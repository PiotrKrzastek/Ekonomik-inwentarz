from wtforms import Form, StringField, validators, Field, ValidationError, BooleanField

class CreateUserForm(Form):
    name = StringField(validators=[validators.InputRequired(message='Nazwa nie może być pusta'), validators.Length(max=400)])
    permission = BooleanField()

    def validate_name(self, field:Field):
        if '@' in field.data:
            raise ValidationError(message="Znak '@' nie może znajdować się w nazwie użytkownika")
        field.data = f'{field.data}@ekonomik.gniezno.pl'

    def validate_permission(self, field:Field):
        if field.data is None:
            field.data = False
        if field.data == 'on':
            field.data = True


class UpdateUserForm(Form):
    user_id = StringField(validators=[validators.InputRequired(message='ID użytkownika nie może być puste'), validators.Length(max=400)])
    permission = BooleanField()

    def validate_permission(self, field:Field):
        if field.data is None:
            field.data = False
        if field.data == 'on':
            field.data = True

class DeleteUserForm(Form):
    user_id = StringField(validators=[validators.InputRequired(message='ID użytkownika nie może być puste'), validators.Length(max=400)])


class UpdateGlobalFilterForm(Form):
    is_active = BooleanField()

    def validate_is_active(self, field:Field):
        if field.data is None:
            field.data = False
        if field.data == 'on':
            field.data = True
