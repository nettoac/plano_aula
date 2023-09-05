from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plano_aulas.db'
db = SQLAlchemy(app)

class PlanoAula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    lingua_estudada = db.Column(db.String(100), nullable=False)
    data_aula = db.Column(db.Date, nullable=False)
    duracao_aula = db.Column(db.Float, nullable=False)
    palavras_aprendidas = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/')
def index():
    planos_aula = PlanoAula.query.all()
    return render_template('templates/index.html', planos_aula=planos_aula)

@app.route('/adicionar_plano', methods=['POST'])
def adicionar_plano():
    if request.method == 'POST':
        nome_aluno = request.form['nome_aluno']
        lingua_estudada = request.form['lingua_estudada']
        data_aula = request.form['data_aula']
        duracao_aula = float(request.form['duracao_aula'])
        palavras_aprendidas = int(request.form['palavras_aprendidas'])

        novo_plano = PlanoAula(nome_aluno=nome_aluno, lingua_estudada=lingua_estudada, data_aula=data_aula,
                               duracao_aula=duracao_aula, palavras_aprendidas=palavras_aprendidas)
        db.session.add(novo_plano)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)