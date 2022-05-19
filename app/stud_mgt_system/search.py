from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, Regexp, NumberRange


class SearchForm(FlaskForm):
    name = StringField('学生姓名: ', render_kw = {"placeholder": '姓名'})

    submitOne = SubmitField('查询')
    submitAll = SubmitField('查询所有')
