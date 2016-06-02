# -*- coding: UTF-8 -*-
from flask import  render_template, request, flash,abort,redirect,url_for
from .. import db
from ..models import hosts,dbs,user_db,pros,users,user_pro
from . import main
from .forms import HostAddForm, ProAddForm,UserAddForm
from sqlalchemy import and_,desc,or_
from flask.ext.login import login_required, current_user
from config import Config, basedir
import ssh.SSH
import os,json,time


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return  render_template('index.html')

@main.route('/prolist', methods=['GET', 'POST'])
@main.route('/prolist/<int:page>', methods=['GET', 'POST'])
@login_required
def prolist(page=1):
    if request.method == 'POST':
        operation = request.form['operation']

        if not operation == 'search':
            product_id = request.form['product_id']
            pro = pros.query.filter_by(id=product_id).first()

        if operation == 'search':
            search_txt = request.form['search_text'].encode('utf8')
            if current_user.role == '0':
                pro_all = pros.query.filter(or_(pros.proname.ilike('%%%s%%' %search_txt),
                                                pros.prodomain.ilike('%%%s%%' %search_txt))).paginate(page,Config.POSTS_PER_PAGE,False)
            else:
                user_pro_list = db.session.query(user_pro).filter_by(user_id=current_user.id).all()
                pro_id_list = []
                for pro_id in user_pro_list:
                    pro_id_list.append(pro_id[1])
                pro_all = pros.query.filter(and_(pros.id.in_(pro_id_list),or_(pros.proname.ilike('%%%s%%' %search_txt),
                                                                             pros.prodomain.ilike('%%%s%%' %search_txt)))).paginate(page,Config.POSTS_PER_PAGE,False)
            return  render_template('prolist.html',pros=pro_all,current_user=current_user)

        elif operation == 'delete_product':
            try:
                proname = pro.proname
                db.session.delete(pro)
                db.session.commit()
                return u"%s 项目删除成功!" %proname
            except Exception, e:
                print e
                return u'删除失败!'
        elif operation == 'get_curversion':
            cur_version = pro.svnver
            old_version = pro.svnoldver
            data = {"cur_version":cur_version,"old_version":old_version}
            return json.dumps(data,sort_keys=True,indent=4)
        elif operation == 'update':
            up_version = request.form['version']
            if up_version == '':
                cmd = "\/usr/bin/svn co %s %s --username %s --password '%s'" %(pro.svnurl,pro.propath,pro.svnuser,pro.svnpass)
                host = hosts.query.filter_by(hostip=pro.host_ip).first()
                try:
                    cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,cmd)
                    if cmd_status == 'SUCCESS':
                        print cmd_status,cmd_result
                        cur_version = cmd_result.split('\n')[-2].split()[-1]
                        old_version = pro.svnver
                        pro.svnoldver = old_version
                        pro.svnver = cur_version
                        db.session.add(pro)
                        db.session.commit()
                        return cmd_result.replace('\n','</br>')
                    else:
                        return cmd_result
                except Exception, e:
                    print e
                    return u'ERROR!'
            else:
                cmd = "\/usr/bin/svn co %s %s --username %s --password '%s' -r %s" %(pro.svnurl,pro.propath,pro.svnuser,pro.svnpass,up_version)
                host = hosts.query.filter_by(hostip=pro.host_ip).first()
                try:
                    cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,cmd)
                    if cmd_status == 'SUCCESS':
                        cur_version = cmd_result.split('\n')[-2].split()[-1]
                        old_version = pro.svnver
                        pro.svnoldver = old_version
                        pro.svnver = cur_version
                        db.session.add(pro)
                        db.session.commit()
                        return cmd_result.replace('\n','</br>')
                    else:
                        return cmd_result
                except Exception, e:
                    print e
                    return u'ERROR!'
        elif operation == 'start':
            cmd = "%s/bin/startup.sh" %pro.tomcatpath
            try:
                host = hosts.query.filter_by(hostip=pro.host_ip).first()
                cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,cmd)
                if cmd_status == 'SUCCESS':
                    print cmd_result
                    return u'启动成功!'
                else:
                    print cmd_result
                    return u'启动失败!'
            except Exception, e:
                print e
                print cmd_result
                return u'启动失败!'
        elif operation == 'stop':
            cmd = '''ps aux | grep %s |grep -v grep | awk '{print $2}' | xargs kill -9''' %pro.tomcatpath.split('/')[-1]
            print cmd
            try:
                host = hosts.query.filter_by(hostip=pro.host_ip).first()
                cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,cmd)
                if cmd_status == 'SUCCESS':
                    return u'关闭成功!'
                else:
                    return u'关闭失败!'
            except Exception, e:
                print e
                print cmd_result
                return u'关闭失败!'
        elif operation == 'restart':
            cmd = '''ps aux | grep %s |grep -v grep | awk '{print $2}' | xargs kill -9; %s/bin/startup.sh''' %(pro.tomcatpath.split('/')[-1],pro.tomcatpath)
            print cmd
            try:
                host = hosts.query.filter_by(hostip=pro.host_ip).first()
                cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,cmd)
                if cmd_status == 'SUCCESS':
                    return u'重启成功!'
                else:
                    return u'重启失败!'
            except Exception, e:
                print e
                print cmd_result
                return u'重启失败!'
    else:
        if current_user.role == '0':
            pro = pros.query.paginate(page, Config.POSTS_PER_PAGE, False)
        else:
            user_pro_list = db.session.query(user_pro).filter_by(user_id=current_user.id).all()
            pro_id_list = []
            for proid in user_pro_list:
                pro_id_list.append(proid[1])
            pro = pros.query.filter(pros.id.in_(pro_id_list)).paginate(page, Config.POSTS_PER_PAGE, False)
        return  render_template('prolist.html',pros=pro,current_user=current_user)

@main.route('/proadd', methods=['GET', 'POST'])
@login_required
def proadd():
    form = ProAddForm()
    host = hosts.query.all()
    if form.validate_on_submit():
        try:
            server_ip = request.form['select_host']
            pro = pros(proname=form.proname.data,
                       prodomain=form.prodomain.data,
                       protype=form.protype.data,
                       propath=form.propath.data,
                       tomcatpath=form.tomcatpath.data,
                       svnurl=form.svnurl.data,
                       svnuser=form.svnuser.data,
                       svnpass=form.svnpass.data)
            print pro
            pro.host_ip = server_ip
            db.session.add(pro)
            db.session.commit()
            flash(u'%s项目 添加记录成功!' %form.proname.data)
            return render_template('proadd.html',form=form,hosts=host)
        except Exception, e:
            print e
            flash(u'添加记录失败!')
            return render_template('proadd.html',form=form,hosts=host)
    else:
        return  render_template('proadd.html',hosts=host,form=form)


@main.route('/hostlist', methods=['GET', 'POST'])
@main.route('/hostlist/<int:page>', methods=['GET', 'POST'])
@login_required
def hostlist(page=1):
    if request.method == 'POST':
        operation = request.form['operation']
        server_id = request.form['server_id']
        if operation == 'delete_server':
            try:
                host = hosts.query.filter_by(id=server_id).first()
                hostname = host.hostname
                db.session.delete(host)
                db.session.commit()
                #hostname = u'测试平台!'
                return u'删除 %s 成功!' %hostname
            except Exception, e:
                print e
                return u'删除失败!'
        elif operation == 'test_server':
            try:
                host = hosts.query.filter_by(id=server_id).first()
                cmd_status,cmd_result = ssh.SSH.ssh_cmd(host.hostip,int(host.hostport),host.hostuser,host.hostkey,'hostname;echo "<br>";date')
                if cmd_result != 'Error':
                    return cmd_result
                else:
                    return u"验证失败!"
            except Exception, e:
                print e
                return u"验证失败!"
    else:
        host = hosts.query.paginate(page, Config.POSTS_PER_PAGE, False)
        return  render_template('hostlist.html',hosts=host)

@main.route('/hostadd', methods=['GET', 'POST'])
@login_required
def hostadd():
    form = HostAddForm()
    if form.validate_on_submit():
        try:
            hostip = form.hostip.data
            prv_file = request.files['hostkey']
            file_name = os.path.join(Config.prv_key_path,hostip)
            prv_file.save(file_name)

            host = hosts(hostname=form.hostname.data,
                             hostip=hostip,
                             hostuser=form.hostuser.data,
                             hostport=form.hostport.data,
                             hostkey=file_name)
            print host
            db.session.add(host)
            db.session.commit()
            flash(u'%s服务器 添加记录成功!' %form.hostname.data)
            return render_template('hostadd.html',form=form)
        except Exception, e:
            print e
            flash(u'添加记录失败!')
            return render_template('hostadd.html',form=form)
    else:
        return render_template('hostadd.html',form=form)

@main.route('/useradd', methods=['GET', 'POST'])
@login_required
def useradd():
    form = UserAddForm()
    if form.validate_on_submit():
            user = users(username=form.username.data,
                         name=form.name.data,
                         password=form.password.data,
                         useremail=form.useremail.data,
                         role=form.role.data,
                         status=form.status.data)
            db.session.add(user)
            db.session.commit()
            flash(u'%s 用户添加成功!' %form.username.data)
            return render_template('useradd.html',form=form)
    else:
        return render_template('useradd.html',form=form)


@main.route('/userlist', methods=['GET', 'POST'])
@main.route('/userlist/<int:page>', methods=['GET', 'POST'])
@login_required
def userlist(page=1):
    if request.method == 'POST':
        operation = request.form['operation']
        if operation == 'del_user':
            try:
                user_id = request.form['user_id']
                user = users.query.filter_by(id=user_id).first()
                username = user.username
                db.session.delete(user)
                db.session.commit()
                return u'删除用户 %s 成功!' %username
            except Exception, e:
                print e
                return u'删除用户失败!'
    else:
        user = users.query.paginate(page, Config.POSTS_PER_PAGE, False)
        return render_template('userlist.html',users=user)


@main.route('/userpro/<int:userid>', methods=['GET','POST'])
@login_required
def userpro(userid):
    if request.method == 'POST':
            try:
                user = users.query.filter_by(id=userid).first()
                pro_list = request.form['pro_list'].strip()
                domain_list = []
                pro_obj_list = []
                if not pro_list == '':
                    pro_list = pro_list.split(',')
                    for pro in pro_list:
                        prodomain = pro.split('-')[1]
                        domain_list.append(prodomain)
                        pro_obj = pros.query.filter_by(prodomain=prodomain).first()
                        pro_obj_list.append(pro_obj)

                user.pros = pro_obj_list
                db.session.add(user)
                db.session.commit()
                return  u'更新权限成功!'
            except Exception, e:
                print e
                return u'更新权限失败!'
    else:
        User_Pro = users.query.filter_by(id=userid).first().pros
        pros_all = pros.query.order_by(pros.id.desc()).all()
        for pro in pros_all:
            if pro in User_Pro:
                pros_all.remove(pro)
        return render_template('user_pro.html',User_Pro=User_Pro,All_Pro=pros_all)

@main.route('/dbapi', methods=['GET','POST'])
def dbapi():
    if request.method == 'POST':
        opr = request.form['operation']
        if opr == 'dblist':
            username = request.form['username']
            data = {}
            data_list = {}
            user = users.query.filter_by(username=username).first()
            if user and user.role != '0':
                db_id_list = db.session.query(user_db).filter_by(user_id=user.id).all()
                db_list = dbs.query.filter(dbs.id.in_(db_id_list)).all()
            else:
                db_list = dbs.query.order_by(dbs.id).all()
            for db_item in db_list:
                data_list[db_item.name] = db_item.id
            data['dblist'] = data_list
            return json.dumps(data)
        elif opr == 'auth':
            username = request.form['username']
            password = request.form['password']
            db_id = request.form['db_id']
            db_item = dbs.query.filter_by(id=db_id).first()
            user = users.query.filter_by(username=username).first()
            if user is not None and user.verify_password(password):
                if db_item in user.dbs or user.role == '0':
                    data = {'auth':'ok','dbhost':db_item.dburl,'dbname':db_item.dbname,'dbuser':db_item.dbuser,'dbpass':db_item.dbpass}
                    return json.dumps(data)
                else:
                    data = {'auth':'login'}
                    return json.dumps(data)
            else:
                data = {'auth':'failed'}
                return json.dumps(data)
    else:
        return 'ok'