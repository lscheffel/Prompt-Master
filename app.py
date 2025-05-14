from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import logging
import uuid

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secure-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/promptmaster'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Prompt com UUID
class Prompt(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_objectives = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.String(20), nullable=False)
    tone = db.Column(db.String(50), nullable=False)
    persona = db.Column(db.Text, nullable=False)
    protocols = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<Prompt {self.project_name}>'

# Formulário WTForms
class PromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])
    language = SelectField('Linguagem Principal', choices=[
        ('texto_puro', 'Texto Puro'), ('markdown', 'Markdown'), ('html', 'HTML'),
        ('css', 'CSS'), ('python', 'Python'), ('javascript', 'JavaScript')
    ], validators=[DataRequired()])
    temperature = SelectField('Temperatura do Chat', choices=[
        ('0.3', 'Muito Preciso'), ('0.5', 'Preciso'), ('0.7', 'Balanceado'),
        ('0.9', 'Criativo'), ('1.0', 'Muito Criativo')
    ], validators=[DataRequired()])
    tone = SelectField('Tom do Chat', choices=[
        ('formal', 'Formal'), ('informal', 'Informal'), ('tecnico', 'Técnico'),
        ('amigavel', 'Amigável'), ('autoritario', 'Autoritário')
    ], validators=[DataRequired()])
    persona = TextAreaField('Persona', validators=[DataRequired()])
    protocols = TextAreaField('Protocolos', validators=[DataRequired()])
    submit = SubmitField('Gerar Prompt')

# Rotas
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt(
                project_name=form.project_name.data,
                project_description=form.project_description.data,
                project_objectives=form.project_objectives.data,
                language=form.language.data,
                temperature=form.temperature.data,
                tone=form.tone.data,
                persona=form.persona.data,
                protocols=form.protocols.data
            )
            db.session.add(prompt)
            db.session.commit()
            logger.info(f'Prompt "{prompt.project_name}" criado com sucesso. ID: {prompt.id}')
            flash('Prompt criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt: {str(e)}')
            flash('Erro ao criar prompt.', 'error')
    return render_template('index.html', form=form)

@app.route('/prompts')
def list_prompts():
    try:
        prompts = Prompt.query.all()
        logger.info('Lista de prompts carregada.')
        return render_template('prompts.html', prompts=prompts)
    except Exception as e:
        logger.error(f'Erro ao listar prompts: {str(e)}')
        flash('Erro ao listar prompts.', 'error')
        return redirect(url_for('index'))

@app.route('/prompt/<string:id>')
def view_prompt(id):
    try:
        prompt = Prompt.query.get_or_404(uuid.UUID(id))
        logger.info(f'Prompt {id} visualizado.')
        return render_template('view_prompt.html', prompt=prompt)
    except Exception as e:
        logger.error(f'Erro ao visualizar prompt {id}: {str(e)}')
        flash('Erro ao visualizar prompt.', 'error')
        return redirect(url_for('list_prompts'))

@app.route('/prompt/<string:id>/delete', methods=['POST'])
def delete_prompt(id):
    try:
        prompt = Prompt.query.get_or_404(uuid.UUID(id))
        db.session.delete(prompt)
        db.session.commit()
        logger.info(f'Prompt {id} deletado.')
        flash('Prompt deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f'Erro ao deletar prompt {id}: {str(e)}')
        flash('Erro ao deletar prompt.', 'error')
    return redirect(url_for('list_prompts'))

# Inicialização do banco
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)