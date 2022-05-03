from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from decrypt import hash_pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@127.0.0.1/gestion_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


matiere_classe = db.Table('matieres_classes',
    db.Column('classe_id.id', db.Integer, db.ForeignKey('classe.id'), primary_key=True),
    db.Column('matiere_id', db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_matiere = db.Column(db.Integer,  db.ForeignKey('matiere.id'))
    id_etudiant = db.Column(db.Integer,  db.ForeignKey('etudiant.id'))
    note_ds = db.Column(db.Float, default=0)
    note_examen = db.Column(db.Float, default=0)
    def moy(self):
        return (self.note_ds + self.note_examen*2)/3

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    etudiants = db.relationship('Etudiant', backref=db.backref('classe', lazy='joined'), lazy='select')
    matieres = db.relationship('Matiere', secondary=matiere_classe, lazy='subquery',
                           backref=db.backref('classes', lazy=True))

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30))
    coef = db.Column(db.Float(2, 2))
    notes = db.relationship('Note', backref=db.backref('matiere', lazy='joined'), lazy='select')



class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30))
    prenom = db.Column(db.String(30))
    cin = db.Column(db.String(8), nullable=False, unique=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'))
    notes = db.relationship('Note', backref=db.backref('etudiant', lazy='joined'), lazy='select')
    user = db.relationship("User", uselist=False, backref="etudiant")

    def moyenne(self):
        notes = self.notes
        moy = 0
        coefs = 0
        for note in notes:
            coefs = coefs + note.matiere.coef
        print (coefs)

        for note in notes:
            moy = moy + (float(note.moy())*float(note.matiere.coef))/float(coefs)
        return moy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.String(100), nullable=False)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('etudiant.id'))
    createdat = db.Column(db.DateTime(), nullable=False)
    def __init__(self, username, email, password, phone, is_active, role, createdat):
        self.username = username
        self.email = email
        self.password = hash_pass(password)
        self.is_active = is_active
        self.phone = phone
        self.role = role
        self.createdat = createdat
    def pwd (self) :
        return self.password




#if __name__ == '__main__':
#db.drop_all()
#db.create_all()
    #manager.run()