from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from .models.user import User

class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired(message="Brukernavn er påkrevd")])
    password = PasswordField('Passord', validators=[DataRequired(message="Passord er påkrevd")])
    submit = SubmitField('Logg inn')

class RegistrationForm(FlaskForm):
    username = StringField('Brukernavn', validators=[
        DataRequired(message="Brukernavn er påkrevd"),
        Length(min=3, max=50, message="Brukernavn må være mellom 3 og 50 tegn")
    ])
    email = EmailField('E-post', validators=[
        DataRequired(message="E-post er påkrevd"),
        Email(message="Ugyldig e-postadresse")
    ])
    password = PasswordField('Passord', validators=[
        DataRequired(message="Passord er påkrevd"),
        Length(min=6, message="Passordet må være minst 6 tegn")
    ])
    submit = SubmitField('Registrer deg')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Dette brukernavnet er allerede i bruk')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Denne e-postadressen er allerede registrert')
