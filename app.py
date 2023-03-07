# bibliotecas
from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#Data base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.config['SECRET_KEY'] = "random string"


db = SQLAlchemy(app)


class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)
    
    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch
        
with app.app_context():
    db.create_all()
    
    


# Lista de frutas - index.html
frutas = []
# Lista de Registro pag Professores
registros = []


#index.html - frutas
@app.route('/', methods=["GET", "POST"])
def principal():
	#frutas = ["Morango", "Uva", "Laranja", "Mamão", "Maçã", "Pêra", "Melão", "Abacaxi"]
	if request.method == "POST":
		if request.form.get("fruta"):
			frutas.append(request.form.get("fruta"))
	return render_template("index.html", frutas=frutas)


#pagina Professores
@app.route('/sobre', methods=["GET", "POST"])
def sobre():
	#notas = {"Fulano":5.0, "Beltrano":6.0, "Aluno": 7.0, "Sicrano":8.5, "Rodrigo":9.5}
	if request.method == "POST":
		if request.form.get("aluno") and request.form.get("nota"):
			registros.append({"aluno": request.form.get("aluno"),"nota": request.form.get("nota")})

	return render_template("sobre.html", registros=registros)


#pag filmes
@app.route('/filmes<propiedade>')
def filmes(propiedade):
    if propiedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=d4ec995fe57eb20540e34ceaa70350df"
    # elif propiedade == 'kids':
    #    url = "https://api.themoviedb.org/3//discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=d4ec995fe57eb20540e34ceaa70350df"
    elif propiedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=d4ec995fe57eb20540e34ceaa70350df"
    elif propiedade == 'drama':
        url = "https://api.themoviedb.org/3//discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=d4ec995fe57eb20540e34ceaa70350df"
    # elif propiedade == 'tom_cruise':
    #     url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=d4ec995fe57eb20540e34ceaa70350df"
        
    resposta = urllib.request.urlopen(url)
    
    dados = resposta.read()
    
    jsondata = json.loads(dados)
    
    return render_template("filmes.html", filmes=jsondata["results"])


# index.cursos --- com banco de dados
@app.route('/cursos')
def lista_cursos():
    return render_template("cursos.html", cursos=cursos.query.all())

#novo curso
@app.route('/cria_curso', methods=["GET", "POST"])
def cria_curso():
	nome = request.form.get('nome')
	descricao = request.form.get('descricao')
	ch = request.form.get('ch')

	if request.method == 'POST':
		if not nome or not descricao or not ch:
			flash("Preencha todos os campos do formulário","error")
		else:
			curso = cursos(nome, descricao, ch)
			db.session.add(curso)
			db.session.commit()
			return redirect(url_for('lista_cursos'))
	return render_template("novo_curso.html")

#editar banco
@app.route('/<int:id>/atualiza_curso', methods=["GET", "POST"])
def atualiza_curso(id):
	curso = cursos.query.filter_by(id=id).first()
	if request.method == 'POST':
		nome = request.form["nome"]
		descricao = request.form["descricao"]
		ch = request.form["ch"]

		cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})
		db.session.commit()
		return redirect(url_for('lista_cursos'))
	return render_template("atualiza_curso.html", curso=curso)


#debug active
if __name__ == "__main__":
    app.run(debug=True)