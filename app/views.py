from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm,AgendaForm
from .user import User
from bson.objectid import ObjectId

from .model.model import Agenda

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            #flash("Logado com Sucesso!", category='success')
            return redirect(request.args.get("next") or url_for("menu"))
        flash("Usuario ou Senha incorreta!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/agenda', methods=['GET','POST'])
def agenda():

    if request.method == 'POST':
        agenda = Agenda(nome=request.values.get('inputnome'), 
                        endereco=request.values.get('inputend'), 
                        email=request.values.get('inputemail'), 
                        telefone=request.values.get('inputtel'))
        app.config['AGENDA_COLLECTION'].insert_one(agenda.para_json())
        flash("Cadastro com sucesso!", category='success')
        return redirect(request.args.get("next") or url_for("menu"))

    return render_template('agenda.html')

@app.route('/mostrar', methods=['GET','POST'])
def mostrar():
    agendas = app.config['AGENDA_COLLECTION'].find()
    return render_template('listar.html', query=agendas)

@app.route("/remove")  
def remove ():  
    key=request.values.get("_id") 
    #flash(key, category='info')
    app.config['AGENDA_COLLECTION'].delete_one({'_id': ObjectId(key)})
    flash("Cadastro excluido com sucesso!", category='success')
    return redirect(request.args.get("next") or url_for("mostrar"))

@app.route("/achaporID" , methods=['GET', 'POST'])  
def achaporId ():  
    key=request.values.get("_id") 
    agenda = app.config['AGENDA_COLLECTION'].find_one({'_id': ObjectId(key)})
    if request.method == 'POST':
        agenda = Agenda(nome=request.values.get('inputnome'), 
                        endereco=request.values.get('inputend'), 
                        email=request.values.get('inputteal'), 
                        telefone=request.values.get('inputemail'))
        app.config['AGENDA_COLLECTION'].update({"_id":ObjectId(key)}, 
        {'$set': agenda.para_json()})
        flash("Cadastro atualizado com sucesso!", category='success')
        return redirect(request.args.get("next") or url_for("mostrar"))
    return render_template('agenda_alterar.html', query=agenda)

@app.route("/agenda_retorna" , methods=['GET', 'POST'])  
def agenda_retorna ():
    return render_template('menu.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    return render_template('menu.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])