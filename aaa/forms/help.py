from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class HelpingForm(FlaskForm):
    problem = TextAreaField("Опишите Вашу проблему", validators=[DataRequired()])
    geo = StringField("Ваш адрес", validators=[DataRequired()])
    number = StringField("Ваш номер", validators=[DataRequired()])
    submit = SubmitField('Отправить')
