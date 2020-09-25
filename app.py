from flask import Flask
from flask_restful import Resource, Api,request
from models import Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

class Usuario(Resource):

    def get(self, nome):
        usuario = Usuarios.query.filter_by(nome=nome).first()
        try:
            response = {
                'id':usuario.id,
                'nome':usuario.nome,
            }
        except AttributeError:
            response ={
                'status':'error',
                'mensagem':'Usuario nao encontrado'
            }
        return response

    def put(self, nome):
        usuario = Usuarios.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            usuario.nome = dados['nome']
        usuario.save()
        response = {
            'id': usuario.id,
            'nome': usuario.nome,
        }
        return response

    def delete(self, nome):
        usuario = Usuarios.query.filter_by(nome=nome).first()
        mensagem = 'Usuario {} excluido com sucesso'.format(usuario.nome)
        usuario.delete()
        return {'status':'sucesso', 'mensagem':mensagem}

class LstaUsuario(Resource):

    def get(self):
        usuarios = Usuarios.query.all()
        response = [{'id':i.id, 'nome':i.nome} for i in usuarios]
        return response

    def post(self):
        dados = request.json
        usuario = Usuarios(nome=dados['nome'])
        usuario.save()
        response = {
            'id': usuario.id,
            'nome': usuario.nome,
        }
        return response



api.add_resource(Usuario, '/usuario/<string:nome>/')
api.add_resource(LstaUsuario, '/usuario/')


if __name__ == '__main__':
    app.run(debug=True)