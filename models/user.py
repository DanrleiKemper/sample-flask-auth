from database import db
from flask_login import UserMixin


#criação das colunas do abnco de dados para armazenar as informações  do usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)