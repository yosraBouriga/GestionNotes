from datetime import datetime
#import self as self
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

from manage import User, Note
from manage import Classe
from manage import Etudiant
from manage import Matiere

from decrypt import verify_pass

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/gestion_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)




# This is the index route where we are going to
@app.route('/notes/store/<id_etudiant>', methods=['POST'])
def storeNotes(id_etudiant):
    for i in request.form.keys():
        if i.startswith('ds'):
            id=i.split('-')[1]
            note = Note.query.get(id)
            if note == None:
                note = Note()
                note.note_ds = request.form['ds-'+id]
                note.note_examen = request.form['ex-'+id]
                note.id_etudiant = id_etudiant
                note.id_matiere = id
                db.session.add(note)
                db.session.commit()
            else:
                session = db.session.object_session(note)
                note.note_ds = request.form['ds-' + id]
                note.note_examen = request.form['ex-' + id]
                note.id_etudiant = id_etudiant
                note.id_matiere = id
                session.add(note)
                session.commit()


    return redirect(url_for('etudiants'))
@app.route('/classes/updata/<id>', methods=['POST'])
def updateClasse(id):
    #db.session.query(Classe).filter_by(id=id).update({'nom': request.form['nom']})
    classe = Classe.query.get(id)
    session = db.session.object_session(classe)

    classe.nom = request.form['nom']

    for matiere in classe.matieres:
        classe.matieres.remove(matiere)

    for i in request.form.keys():
        if i != 'nom':
            matiere = Matiere.query.get(request.form[i])
            classe.matieres.append(matiere)
    session.add(classe)
    session.commit()
    return redirect(url_for('showClasse', id=id))
@app.route('/classes/<id>')
def showClasse(id):
    classe = Classe.query.get(id)
    matieres = Matiere.query.all()
    return render_template('show_classe.html', classe=classe, matieres=matieres)
@app.route('/')
def Index():
    all_user = User.query.all()

    return render_template("index.html", users=all_user)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST', 'GET'])
def insert_admin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        userbyusername = User.query.filter_by(username=username).first()
        userbyemail = User.query.filter_by(email=email).first()
        userbyphone = User.query.filter_by(phone=phone).first()
        if(userbyusername): return render_template('user.html', msg_register='Username already existing', success=False)
        if(userbyemail): return render_template('user.html', msg_register='Email already existing', success=False)
        if(userbyphone): return render_template('user.html', msg_register='Username already existing', success=False)

        password = request.form['password']
        confirm = request.form['confirm']
        if(password!=confirm): return render_template('user.html', msg_register='password must be equal', success=False)
        is_active = False
        role = 'admin'
        createdat = datetime.now()
        my_data = User(username, email, password, phone, is_active, role, createdat)
        db.session.add(my_data)
        db.session.commit()

        flash("user Inserted Successfully")

        return redirect(url_for('Index'))
    else:
        return render_template("user.html")

@app.route('/matieres', methods=['GET'])
def matieres():
    matieres = Matiere.query.all()
    return render_template('matieres.html', matieres=matieres)
@app.route('/matieres/store', methods=['POST'])
def matiereStore():
    nom = request.form['nom']
    coef = request.form['coef']
    matiere = Matiere()
    matiere.nom = nom
    matiere.coef = coef
    db.session.add(matiere)
    db.session.commit()
    return redirect(url_for('matieres'))
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if session['role'] == 'admin':
        classes = Classe.query.all()
        return render_template('dashboard.html', classes=classes)
    else:
        user_id = session['user_id']
        user = User.query.get(user_id)
        etudiant = Etudiant.query.get(user.id_etudiant)
        notes = etudiant.notes
        return render_template('dashboard.html', etudiant=etudiant, notes=notes)

@app.route('/classes/store', methods=['POST'])
def classeStore():
    nom = request.form['nom']
    classe = Classe()
    classe.nom = nom
    db.session.add(classe)
    db.session.commit()
    return redirect(url_for('dashboard'))
@app.route('/etudiant/<id>')
def showEtudiant(id):
    etudiant = Etudiant.query.get(id)
    classes = Classe.query.all()
    return render_template('show_etudiant.html', etudiant=etudiant, classes=classes)

@app.route('/etudiant/update/<id>', methods=['POST'])
def updateEtudiant(id):
    db.session.query(Etudiant).filter_by(id=id).update({'nom': request.form['nom'], 'prenom': request.form['prenom'], 'classe_id': request.form['classe_id']})
    return redirect(url_for('etudiants'))

@app.route('/etudiants', methods=['GET'])
def etudiants():
    etudiants = Etudiant.query.all()
    classes = Classe.query.all()
    return render_template('etudiants.html', etudiants=etudiants, classes=classes)
@app.route('/etudiants/store', methods=['POST'])
def etudiantStore():
    etudiants = Etudiant.query.all()
    classes = Classe.query.all()
    nom = request.form['nom']
    prenom = request.form['prenom']
    cin = request.form['cin']
    classe_id = request.form['classe_id']
    test1 = User.query.filter_by(email=request.form['email']).first()
    test2 = User.query.filter_by(username=request.form['username']).first()
    test3 = Etudiant.query.filter_by(cin=cin).first()
    if test1 != None:
        flash("L'adresse email doit être unique")
        return render_template('etudiants.html', etudiants=etudiants, classes=classes)
    if test2 != None:
        flash("Le username doit être unique")
        return render_template('etudiants.html', etudiants=etudiants, classes=classes)
    if test3 != None:
        flash("Le numéro de cin doit être unique")
        return render_template('etudiants.html', etudiants=etudiants, classes=classes)
    if request.form['password'] != request.form['confirm']:
        flash("Les deux mots de passe doivent être identiques")
        return render_template('etudiants.html')

    etudiant = Etudiant()
    etudiant.nom = nom
    etudiant.prenom = prenom
    etudiant.cin = cin
    etudiant.classe_id = classe_id
    db.session.add(etudiant)
    db.session.commit()
    user = User(request.form['username'], request.form['email'], request.form['password'], '', False, 'etudiant', datetime.now())
    user.id_etudiant = etudiant.id
    #session = db.session.object_session(user)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for(('etudiants')))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if(user):

            if verify_pass(request.form['password'], user.password):
                login_user(user)
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect(url_for('dashboard'))
        else:
            flash("user does not exist")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.username = request.form['username']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.password = request.form['password']
        my_data.is_active = request.form['is_active']
        my_data.role = request.form['role']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))



@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('Index'))

@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))
def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()
if __name__ == "__main__":
    configure_database(app)

app.run(debug=True)

