from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nekoGame.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__='USERS'
    idUser: int
    username: str
    password: str

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    username_1: str
    username_2: str

    idGame = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username_1 = db.Column(db.String(30), db.ForeignKey('USERS.username'))
    username_2 = db.Column(db.String(30), db.ForeignKey('USERS.username'))

    def __repr__(self):
        return f'<Game{self.idGame}>'
    
@dataclass
class Set(db.Model):
    __tablename__ = 'SETS'
    idGame = int
    set_number = int
    user_status_1 = str 
    user_status_2 = str

    idGame = db.Column(db.Integer, db.ForeignKey('GAMES.idGame'),primary_key=True)
    set_number = db.Column(db.Integer)
    user_status_1 = db.Column(db.String(1), nullable=False) ## W=Win, L=Lose, D=draw
    user_status_2 = db.Column(db.String(1), nullable=False) ## W=Win, L=Lose, D=draw

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
        elif username == "" or password == "":
            return jsonify({"error":"no user or password added"})
        else:
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

@app.route("/CreateJoinGame/<username>", methods=["GET","POST","PUT"])
def create_join_game(username):
    if request.method == 'POST':
        idGame = request.json["idGame"]
        username_1 = request.json["username_1"]
        username_2 = request.json["username_2"]

        idGame_exists = Game.query.filter_by(idGame=idGame).first()
        if idGame_exists:
            return jsonify({"error": "Game id already exists"}), 401
        else: 
            new_game = Game(idGame=idGame, username_1=username_1, username_2=username_2)
            new_set = Set(idGame=idGame, set_number=1, user_status_1="",user_status_2="")
            db.session.add(new_set)
            db.session.add(new_game)
            db.session.commit()
            return jsonify({"sucess":"game and set created"})
    elif request.method == "PUT":
        data = request.get_json()
        idGame = data["idGame"]
        username_2 = data["username_2"]
        print(username_2)
        game = Game.query.get(idGame)
        if game:
            game.username_2 = username_2
            db.session.commit()
            return jsonify({"sucess":"game updated"})
        
@app.route("/Game/<username>/<randomId>/<set_number>", methods=["GET","POST","PUT"])
def set_game_status(username,randomId, set_number):
    return jsonify({"To do"})

if __name__ == '__main__':
    app.run(debug=True)