from . import db
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

user_pro = db.Table('user_pro', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('pro_id', db.Integer, db.ForeignKey('pros.id'))
)

user_db = db.Table('user_db', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('db_id', db.Integer, db.ForeignKey('dbs.id'))
)

class users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    useremail = db.Column(db.String(64))
    pros = db.relationship('pros', secondary=user_pro, backref=db.backref('users', lazy='dynamic'))
    dbs = db.relationship('dbs', secondary=user_db, backref=db.backref('users', lazy='dynamic'))
    role  = db.Column(db.String(64),default='1')
    status = db.Column(db.Integer,default=1)
    createtime = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))
    hostip = db.Column(db.String(64), unique=True,index=True)
    hostuser = db.Column(db.String(64))
    hostport = db.Column(db.Integer)
    hostkey = db.Column(db.String(64))
    pros = db.relationship('pros',backref='pros',cascade="all, delete-orphan",passive_deletes=True)

    def __repr__(self):
        return '<Host %r>' % self.hostname

class pros(db.Model):
    __tablename__ = 'pros'
    id = db.Column(db.Integer, primary_key=True)
    proname = db.Column(db.String(64), unique=True, index=True)
    prodomain = db.Column(db.String(64), unique=True)
    protype = db.Column(db.String(64))
    propath = db.Column(db.String(64))
    tomcatpath = db.Column(db.String(64))
    svnurl = db.Column(db.String(64))
    svnuser = db.Column(db.String(64))
    svnpass = db.Column(db.String(64))
    svnver = db.Column(db.String(64))
    svnoldver = db.Column(db.String(64))
    host_ip = db.Column(db.String(64),db.ForeignKey('hosts.hostip',ondelete='CASCADE'))

    def __repr__(self):
        return '<Pro %r>' % self.proname

class dbs(db.Model):
    __tablename__ = 'dbs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    dburl = db.Column(db.String(64))
    dbname = db.Column(db.String(64))
    dbuser = db.Column(db.String(64))
    dbpass = db.Column(db.String(64))
    node = db.Column(db.String(64))

    def __repr__(self):
        return '<db %r>' %self.proname
