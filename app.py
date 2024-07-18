from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
#configuração para inserir chave secreta do banco de dados
app.config['SECRET_KEY'] = "sua_chave_secreta"
#configuração para inserir o caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
#criada variável db para fazer a conexão com o banco de dados
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login'

#recupera o registro do usuário no banco
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#rota para receber os dados do usuário no login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    #condição para conferir se as credenciais existem 
    if username and password:
        #verifica se foi encontrado
        user = User.query.filter_by(username=username).first()
        #verifica se o usuário foi encontrado no banco de dados e se a senha cadastrada corresponde com a senha recebida e faz a autenticação
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso."})
    
    return jsonify({"message": "Credenciais inválidas."}), 400

#rota de logout 
@app.route('/logout', methods=['GET'])
@login_required 
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})

#rota para criar um novo usuário
@app.route('/user', methods=['POST'])
@login_required
def create_user():
    data =  request.json
    username = data.get("username")
    password = data.get("password")
    
    #condição para inserir os dados no banco de dados
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso."})
    
    return jsonify({"message": "Dados inválidos."}), 400

#rota para recuperar/leitura dado do usuário
@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    #condição que retorna o dado do usuário
    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuário não encotrado."}), 404

#rota para alterar dado do usuário
@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    
    #condição que verifica se o usuário existe para alterar a senha
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso."})
    
    return jsonify({"message": "Usuário não encotrado."}), 404

#rota para deletar o usuário
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    
    #condição para não permitir a deleção de um usuário com ID igual que esta autenticado no momento
    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida."}), 403
    #condição para verificar se o usuário é encontrado e deletar do banco de dados
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})

    return jsonify({"message": "Usuário não encotrado."}), 404


if __name__ == '__main__':
    app.run(debug=True)