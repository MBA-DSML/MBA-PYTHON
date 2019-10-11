from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'aula'
DB_NAME = 'agenda'

DATABASE = MongoClient("mongodb+srv://teste_mba:teste123@cluster0-0ri8n.mongodb.net/test?retryWrites=true&w=majority")[DB_NAME]
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.usuarios
SETTINGS_COLLECTION = DATABASE.settings
AGENDA_COLLECTION = DATABASE.agendas

DEBUG = True