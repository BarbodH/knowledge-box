from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    passages = db.relationship("Passage", backref="user")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Passage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False, unique=True)
    text = db.Column(db.String(length=4000), nullable=False, unique=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey("topic.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


class Topic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    topic_name = db.Column(db.String(length=50), nullable=False, unique=True)
    passages = db.relationship("Passage", backref="topic")
