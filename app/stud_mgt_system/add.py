
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, Regexp, NumberRange

class AddForm(FlaskForm):
    name = StringField('学生姓名: ', validators = [InputRequired(), Length(1,10)], render_kw = {"placeholder": '姓名'})
    english = IntegerField('英语成绩: ', validators = [InputRequired(), NumberRange(min = 0, max = 100)], render_kw = {"placeholder": '分数'})
    python = IntegerField('python成绩: ', validators = [InputRequired(), NumberRange(min = 0, max = 100)], render_kw = {"placeholder": '分数'})
    java = IntegerField('java成绩: ', validators = [InputRequired(), NumberRange(min = 0, max = 100)], render_kw = {"placeholder": '分数'})

    submit = SubmitField('添加')