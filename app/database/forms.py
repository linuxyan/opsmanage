#!/usr/bin/python
# coding=utf-8
#__author__ = 'CY'

from flask.ext.wtf import Form
from wtforms import StringField, ValidationError,SelectField
from wtforms.validators import  DataRequired
from ..models import dbs


class DBAddForm(Form):
    name = StringField('name', validators=[DataRequired()])
    dburl = StringField('dburl', validators=[DataRequired()])
    dbname = StringField('dbname', validators=[DataRequired()])
    dbuser = StringField('dbuser', validators=[DataRequired()])
    dbpass = StringField('dbpass', validators=[DataRequired()])
    node = SelectField('node', choices=[(u'杭州节点',u'杭州节点'),(u'青岛节点',u'青岛节点'),(u'金融云',u'金融云')],validators=[DataRequired()])

    def validate_name(self, field):
        if dbs.query.filter_by(name=field.data).first():
            raise ValidationError(u'平台名称已存在!')