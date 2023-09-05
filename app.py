from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import asc

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


# Criar o contexto da aplicação antes de criar o banco de dados
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # planos_aula = PlanoAula.query.all()
    # return render_template('index.html', planos_aula=planos_aula)
    planos_aula = PlanoAula.query.order_by(asc(PlanoAula.data_aula)).all()
    return render_template('index.html', planos_aula=planos_aula)


@app.route('/adicionar_plano', methods=['POST'])
def adicionar_plano():
    if request.method == 'POST':
        nome_aluno = request.form['nome_aluno']
        lingua_estudada = request.form['lingua_estudada']

        # Converter a data de string para um objeto date
        data_aula = datetime.strptime(request.form['data_aula'], '%Y-%m-%d').date()

        duracao_aula = float(request.form['duracao_aula'])
        palavras_aprendidas = int(request.form['palavras_aprendidas'])

        novo_plano = PlanoAula(nome_aluno=nome_aluno, lingua_estudada=lingua_estudada, data_aula=data_aula,
                               duracao_aula=duracao_aula, palavras_aprendidas=palavras_aprendidas)
        db.session.add(novo_plano)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
