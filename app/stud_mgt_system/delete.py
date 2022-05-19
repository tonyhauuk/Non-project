
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, Regexp, NumberRange

class DeleteForm(FlaskForm):
    name = StringField('学生姓名: ', validators = [InputRequired(), Length(1,10)], render_kw = {"placeholder": '姓名'})

    submit = SubmitField('删除')