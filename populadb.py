from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    
    collection = MongoClient("mongodb+srv://teste_mba:teste123@cluster0-0ri8n.mongodb.net/test?retryWrites=true&w=majority")["agenda"]["usuarios"]

    user = input('Entre com usuario: ')
    password = input('Entre com a senha: ')
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        collection.insert({"_id":user, "password":pass_hash})
        print ('usuario criado')
    except DuplicateKeyError:
        print('usuario ja existe')
    #with collection:
    #    db = collection.agenda
    #    users = db.usuarios.find()
    #    print (list(users))

if __name__ == '__main__':
    main()

