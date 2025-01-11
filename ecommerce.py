from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField 
from wtforms.validators import Length, EqualTo,Email, DataRequired, ValidationError
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mercado.db"
app.config["SECRET_KEY"]='4236e47e5ea65e2ba8918ba1'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
##################################
#CRIANDO MODELOS (TABELAS NO BANCO D.D)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=60),nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False)
    senha = db.Column(db.Integer,nullable=False, unique=True)
    valor = db.Column(db.Integer, nullable=False, default=5000) 
    itens = db.relationship('Item',backref='dono_user', lazy=True)
 # encrypting user password   
    @property
    def Pass_crypt(self, password_text):
        self.senha = bcrypt.generate_password_hash(password_text).decode('utf-8')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=60),nullable=False, unique=True)
    preco = db.Column(db.Integer, nullable=False)
    cod_barra = db.Column(db.String(length=60),nullable=False, unique=True)
    descricao = db.Column(db.String(length=60),nullable=False, unique=False)  
    dono = db.Column(db.Integer, db.ForeignKey('user.id'))
################################## 
#CRIANDO CLASSE DO FLASK-FORM
# construindo logica de validação de dados
# fazendo validação se usuario,emal,senha já existem

class CadastroForm(FlaskForm):
    def validate_username(self, check_user):
        user = User.query.filter_by(usuario=check_user.data).first()
        if user:
            raise ValidationError("nome de usuário já existe, tente outro nome de usuário")
    
    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError("email já cadastrado, cadastre outro email")
            
    def validate_senha(self, check_senha):
        senha = User.query.filter_by(senha=check_senha.data).first()
        if senha:
            raise ValidationError("senha já existe, por favor cadastre outra senha")             


    usuario = StringField(label="username : ", validators=[Length(min=2,max=30),DataRequired()])
    email = StringField("E-mail : ", validators=[Email(), DataRequired()])
    senha1 = PasswordField(label="senha : ",validators=[Length(min=6),DataRequired()])
    senha2 = PasswordField(label=" confirmação de senha : ", validators=[EqualTo("senha1"),DataRequired()])
    submit = SubmitField(label="cadastrar")

##################################
# CRIANDO ROTAS

#rota principal(HOME)
@app.route("/")
def home():
    return render_template("home.html")

#recuperando dados de uma tabela
#OBSERVAÇÃO(produtos.html é uma table html.)
@app.route("/produtos")
def page_produtos():
    itens = Item.query.all()
    return render_template("produtos.html",itens=itens)

#criando rota do formulario de cadastro
#fazendo a validação dos dados
#e salvando no banco de dados
#e ja em seguida direcionando o usuario para 
# a page_produtos
@app.route("/cadastro", methods=["GET","POST"])

def page_cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = User(
        usuario = form.usuario.data,
        email = form.email.data,
        senha = form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("page_produtos"))
    if form.errors != {}:
        for err in form.errors.values():
            flash( err, category="danger")
    return render_template("cadastro.html", form=form)
    
    
##################################   
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

