from app import bcrypt, db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    brackets = db.relationship('Bracket', backref='user', lazy=True)

    # Set password (hashing)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    # Check password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    predictions = db.relationship('Prediction', backref='bracket', lazy=True)

class PlayoffSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.Integer, nullable=False)
    team2_id = db.Column(db.Integer, nullable=False)
    team1_wins = db.Column(db.Integer, default=0)
    team2_wins = db.Column(db.Integer, default=0)
    winner_id = db.Column(db.Integer, nullable=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.id'), nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('playoff_series.id'), nullable=False)
    predicted_winner_id = db.Column(db.Integer, nullable=False)
    predicted_games = db.Column(db.Integer, nullable=False)
