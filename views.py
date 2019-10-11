from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm,AgendaForm
from .user import User

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
            flash("Sucesso !!", category='success')
            '''return redirect(request.args.get("next") or url_for("write"))'''
            return render_template('listar.html', title='login', form=form)
        flash("Senha Incorreta", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    form = AgendaForm()
    if request.method == 'POST' and form.validate_on_submit():
        agenda = Agenda(nome=form.nome.data, endereco=form.endereco.data, email=form.email.data, telefone=form.telefone.data)
        app.config['AGENDA_COLLECTION'].insert_one(agenda.para_json())
        flash("Cadastro com sucesso", category='success')
        return redirect(request.args.get("next") or url_for("write"))
    return render_template('agenda.html', title='cadastro', form=form)

@app.route('/mostrar', methods=['GET','POST'])
def mostrar():
    agendas = app.config['AGENDA_COLLECTION'].find()
    return render_template('listar.html', query=agendas)

@app.route("/remove")  
def remove ():  
    key=request.values.get("_id") 
    flash(key, category='info')
    app.config['AGENDA_COLLECTION'].delete_one({"_id":"ObjectId(""" + key + "" + ")"})  
    return redirect(request.args.get("next") or url_for("mostrar"))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    return render_template('write.html')


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