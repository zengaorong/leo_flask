#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,FieldList
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class MaintenForm(FlaskForm):
    work_for = StringField('维修情况', validators=[
        DataRequired(), Length(1, 1024),])
    select_mainten_type = SelectField(label='材料种类',
                         validators=[DataRequired('请选择标签')],render_kw={
                             'class': 'form-control'
                         },
                         choices=[(1, '光猫'), (2, '服务器'), (3, '球机'),(4, '电表'),(5, '其他')],
                         default=1,
                         coerce=int
                         )
    describe = StringField('维修描述', validators=[DataRequired(), Length(1, 255),])
    submit = SubmitField('提交')

class PoliceforForm(FlaskForm):
    work_for = StringField('维护要求', validators=[
        DataRequired(), Length(1, 1024),])
    over_for = StringField('维护情况记录', validators=[Length(0, 255),])
    submit = SubmitField('提交')

class IpFrom(FlaskForm):
    cityIP = StringField('城区IP', validators=[Length(1, 255),])
    townIP = StringField('乡镇IP', validators=[Length(0, 255),])
    submit = SubmitField('提交')


class select_list(FlaskForm):
    qu_name = StringField('IP查询',validators=[DataRequired(), Length(1, 255)],render_kw={"id":"qu_name"})
    position_name = StringField('地点查询',validators=[DataRequired(), Length(1, 255)],render_kw={"id":"position_name"})
    submit = SubmitField('搜索')
