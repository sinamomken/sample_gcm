from app import db


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(1024))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return 'username: %r' % self.username


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keloud_username = db.Column(db.String(1024))
    gcm_token = db.Column(db.String(1024), unique=True)

    def __init__(self, keloud_username, gcm_token):
        self.keloud_username = keloud_username
        self.gcm_token = gcm_token

    def __repr__(self):
        return '%r' % self.gcm_token




