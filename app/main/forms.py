#!/usr/bin/python
# coding=utf-8
#__author__ = 'CY'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField ,ValidationError, validators, RadioField, SelectField
from wtforms.validators import  EqualTo, Email, DataRequired
from ..models import users, hosts, pros

class UserAddForm(Form):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', [validators.DataRequired(), EqualTo('password2', message=u'两次密码不一致')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    useremail = StringField('Email', [validators.DataRequired(), Email()])
    role = SelectField('role', choices=[(u'0',u'管理员'),(u'1',u'普通用户')],validators=[DataRequired()])
    status = SelectField('status',choices=[(u'1',u'禁用'),(u'0',u'启用')],validators=[DataRequired()])

    def validate_useremail(self, field):
        if users.query.filter_by(useremail=field.data).first():
            raise ValidationError(u'邮箱已存在!')

    def validate_name(self, field):
        if users.query.filter_by(name=field.data).first():
            raise ValidationError(u'姓名已存在!')

    def validate_username(self, field):
        if users.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户已存在!')



class HostAddForm(Form):
    hostname = StringField('hostname',validators=[DataRequired()])
    hostip = StringField('hostip',validators=[DataRequired()])
    hostuser = StringField('hostuser', validators=[DataRequired()])
    hostport = StringField('hostport', validators=[DataRequired()])
    hostkey = StringField('hostport', validators=[DataRequired()])

    def validate_hostip(self,field):
        if hosts.query.filter_by(hostip=field.data).first():
            raise ValidationError(u'服务器IP已存在!')


class ProAddForm(Form):
    proname = StringField('hostname',validators=[DataRequired()])
    prodomain = StringField('prodomain',validators=[DataRequired()])
    protype = StringField('protype',validators=[DataRequired()])
    propath = StringField('propath',validators=[DataRequired()])
    tomcatpath = StringField('tomcatpath',validators=[DataRequired()])
    svnurl = StringField('svnurl',validators=[DataRequired()])
    svnuser = StringField('svnuser',validators=[DataRequired()])
    svnpass = StringField('svnpass',validators=[DataRequired()])
    select_host = StringField('select_host',validators=[DataRequired()])

    def validate_proname(self,field):
        if pros.query.filter_by(proname=field.data).first():
            raise ValidationError(u'项目名称已存在!')

class SearchForm(Form):
    search_text = StringField('search_text',validators=[DataRequired()])