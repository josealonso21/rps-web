from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nekoGame.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__='USERS'
    idUser: int
    username: str
    password: str

    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        return self.password == password

@dataclass
class Game(db.Model):
    __tablename__ = 'GAMES'
    idGame = int
    idUser_1: int
    idUser_2: int

    idGame = db.Column(db.Integer, primary_key=True)
    idUser_1 = db.Column(db.Integer, db.ForeignKey('USERS.idUser'),primary_key=True)
    idUser_2 = db.Column(db.Integer, db.ForeignKey('USERS.idUser'),primary_key=True)

    def __repr__(self):
        return f'<Game{self.idGame}>'
    
@dataclass
class Set(db.Model):
    __tablename__ = 'SETS'
    idGame = int
    idSet = int
    user_status_1 = str 
    user_status_2 = str

    idGame = db.Column(db.Integer, db.ForeignKey('GAMES.idGame'),primary_key=True)
    idSet = db.Column(db.Integer, primary_key=True)
    user_status_1 = db.Column(db.String(1), nullable=False)
    user_status_2 = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f'<Set{self.idSet}>'
    
with app.app_context():
    db.create_all()


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]

        user_exists = User.query.filter_by(username=username).first() is not None
 
        if user_exists:
            return jsonify({"error": "User already exists"}), 409
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"sucess":"user created"})
    elif request.method == 'GET':
        users = User.query.all()
        return jsonify(users)

@app.route("/login", methods=["POST","GET"])
def login_user():
    username = request.json["username"]
    password = request.json["password"]
  
    user = User.query.filter_by(username=username).first()
    password = User.query.filter_by(password=password).first()
  
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
  
    if password is None:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({'username':username, 'password':password})

if __name__ == '__main__':
    app.run(debug=True)