#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,abort
from sqlalchemy import and_,desc,or_
from . import database
from ..models import dbs,user_db,users
from .forms import DBAddForm
from app.main.forms import SearchForm
from flask.ext.login import login_required, current_user
from config import Config, basedir
from .. import db


@database.route('/dblist',methods=['GET','POST'])
@database.route('/dblist/<int:page>', methods=['GET', 'POST'])
@login_required
def dblist(page=1):
    if request.method == 'POST':
        operation = request.form['operation']
        if operation == 'search':
            search_txt = request.form['search_text'].encode('utf8')
            if current_user.role == '0':
                db_all = dbs.query.filter(or_(dbs.name.ilike('%%%s%%' %search_txt),dbs.dbname.ilike('%%%s%%' %search_txt))).paginate(page,Config.POSTS_PER_PAGE,False)
            else:
                user_db_list = db.session.query(user_db).filter_by(user_id=current_user.id).all()
                db_id_list = []
                for db_id in user_db_list:
                    db_id_list.append(db_id[1])
                db_all = dbs.query.filter(and_(dbs.id.in_(db_id_list),or_(dbs.name.ilike('%%%s%%' %search_txt),dbs.dbname.ilike('%%%s%%' %search_txt)))).paginate(page,Config.POSTS_PER_PAGE,False)
            return render_template('dblist.html',db_all=db_all,username=current_user.username)
        elif operation =='db_delete':
            if current_user.role == '0':
                db_id = request.form['db_id']
                db_item = dbs.query.filter_by(id=db_id).first()
                db.session.delete(db_item)
                db.session.commit()
                return u'删除成功!'
            else:
                return u'权限拒绝!'
    else:
        if current_user.role == '0':
            db_all = dbs.query.paginate(page, Config.POSTS_PER_PAGE, False)
        else:
            user_db_list = db.session.query(user_db).filter_by(user_id=current_user.id).all()
            db_id_list = []
            for db_id in user_db_list:
                db_id_list.append(db_id[1])
            db_all = dbs.query.filter(dbs.id.in_(db_id_list)).paginate(page,Config.POSTS_PER_PAGE,False)
        return render_template('dblist.html',db_all=db_all,username=current_user.username)

@database.route('/userdb/<int:userid>', methods=['GET','POST'])
@login_required
def userdb(userid):
    if request.method == 'POST':
        try:
            if current_user.role == '0':
                user = users.query.filter_by(id=userid).first()
                db_list = request.form['db_list'].strip()
                db_obj_list = []
                if not db_list == '':
                    db_list = db_list.split(',')
                    for db_id in db_list:
                        db_obj = dbs.query.filter_by(id=db_id).first()
                        db_obj_list.append(db_obj)

                user.dbs = db_obj_list
                db.session.add(user)
                db.session.commit()
                return  u'更新授权成功!'
            else:
                return u'无权限操作!'
        except Exception, e:
            print e
            return u'更新授权失败!'
    else:
        User_dbs = users.query.filter_by(id=userid).first().dbs
        dbs_all = dbs.query.order_by(dbs.id.desc()).all()
        for db_item in dbs_all:
            if db_item in User_dbs:
                dbs_all.remove(db_item)
        return render_template('user_db.html',User_db=User_dbs,All_db=dbs_all)


@database.route('/dbadd', methods=['GET','POST'])
@login_required
def dbadd():
    form = DBAddForm()
    if form.validate_on_submit():
        db_item = dbs(name=form.name.data,
                      dburl=form.dburl.data,
                      dbname=form.dbname.data,
                      dbuser=form.dbname.data,
                      dbpass=form.dbpass.data,
                      node=form.node.data)
        db.session.add(db_item)
        db.session.commit()
        flash(u'%s 数据库添加成功!' %form.name.data)
        return render_template('dbadd.html',form=form)
    else:
        return render_template('dbadd.html',form=form)
