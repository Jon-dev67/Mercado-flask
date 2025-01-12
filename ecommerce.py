from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import Length, EqualTo,Email, DataRequired, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin


db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mercado.db"
app.config["SECRET_KEY"]='4236e47e5ea65e2ba8918ba1'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
##################################
#CRIANDO MODELOS (TABELAS NO BANCO D.D)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=60),nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False)
    senha = db.Column(db.String(length=30),nullable=False, unique=True)
    valor = db.Column(db.Integer, nullable=False, default=5000)
    itens = db.relationship('Item',backref='dono_user', lazy=True)

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, password_text):
        self.senha = bcrypt.generate_password_hash(password_text).decode('utf-8')

    def converte_senha(self,senha_texto_claro):
        return bcrypt.check_password_hash(self.senha,senha_texto_claro)

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
    def validate_usuario(self, check_user):
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

class Loginform(FlaskForm):
    usuario = StringField(label="usuario", validators=[DataRequired()])
    senha = PasswordField(label="senha", validators=[DataRequired()])
    submit = SubmitField(label="log in", validators=[DataRequired()])

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
        senhacrip = form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("page_produtos"))
    if form.errors != {}:
        for err in form.errors.values():
            flash( err, category="danger")
    return render_template("cadastro.html", form=form)

@app.route("/login", methods=["GET","POST"])
def page_login():
    form = Loginform()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f"login realizado com sucesso! Olá  {usuario_logado.usuario}",category="success")
            return redirect(url_for("page_produtos"))
        else:
            flash(f"senha ou email inválido", category="danger")
    return render_template("login.html",form=form)




##################################
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


