from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(min=5)])
    password2 = PasswordField('Repeat Password',
                              validators=[EqualTo('password')])
    submit = SubmitField('Request Password Reset')
