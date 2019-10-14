from app import app


class Agenda():

    def __init__(self, nome, endereco, telefone, email):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

    def para_json(self):
        return self.__dict__



