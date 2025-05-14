from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
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
migrate = Migrate(app, db)

# Modelo de Prompt com UUID
class Prompt(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = db.Column(db.String(100), nullable=False)
    
    # Campos gerais
    project_description = db.Column(db.Text, nullable=False)
    project_objectives = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False, default='texto')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    # Campos específicos de texto
    language = db.Column(db.String(50), nullable=True)
    temperature = db.Column(db.String(20), nullable=True)
    tone = db.Column(db.String(50), nullable=True)
    persona = db.Column(db.Text, nullable=True)
    protocols = db.Column(db.Text, nullable=True)
    
    # Campos específicos de imagem
    positive_prompt = db.Column(db.Text, nullable=True)
    negative_prompt = db.Column(db.Text, nullable=True)
    style = db.Column(db.String(50), nullable=True)
    material = db.Column(db.String(50), nullable=True)
    surface_texture = db.Column(db.String(50), nullable=True)
    lighting_type = db.Column(db.String(50), nullable=True)
    lighting_intensity = db.Column(db.String(20), nullable=True)
    lighting_direction = db.Column(db.String(20), nullable=True)
    primary_color = db.Column(db.String(30), nullable=True)
    post_processing = db.Column(db.Text, nullable=True)

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
    category = SelectField('Categoria', choices=[
        ('texto', 'Texto'),
        ('imagem', 'Imagem'),
        ('audio', 'Áudio'),
        ('codigo', 'Código'),
        ('video', 'Vídeo')
    ], default='texto', validators=[DataRequired()])
    submit = SubmitField('Gerar Prompt')

class ImagePromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    positive_prompt = TextAreaField('Prompt Positivo', validators=[DataRequired()])
    negative_prompt = TextAreaField('Prompt Negativo', validators=[DataRequired()])
    
    # Style and Material
    style = SelectField('Estilo', choices=[
        ('photorealistic', 'Fotorrealista'),
        ('3d_render', 'Render 3D'),
        ('cartoon', 'Cartoon'),
        ('anime', 'Anime'),
        ('digital_art', 'Arte Digital'),
        ('oil_painting', 'Pintura a Óleo'),
        ('watercolor', 'Aquarela'),
        ('sketch', 'Sketch'),
    ], validators=[DataRequired()])
    
    material = SelectField('Material', choices=[
        ('glass', 'Vidro'),
        ('metal', 'Metal'),
        ('wood', 'Madeira'),
        ('plastic', 'Plástico'),
        ('fabric', 'Tecido'),
        ('leather', 'Couro'),
        ('ceramic', 'Cerâmica'),
        ('stone', 'Pedra'),
    ], validators=[DataRequired()])
    
    surface_texture = SelectField('Textura de Superfície', choices=[
        ('smooth', 'Lisa'),
        ('rough', 'Áspera'),
        ('polished', 'Polida'),
        ('matte', 'Fosca'),
        ('glossy', 'Brilhante'),
        ('textured', 'Texturizada'),
    ], validators=[DataRequired()])
    
    # Lighting
    lighting_type = SelectField('Tipo de Iluminação', choices=[
        ('studio_hdri', 'Studio HDRI'),
        ('natural', 'Natural'),
        ('artificial', 'Artificial'),
        ('dramatic', 'Dramática'),
        ('soft', 'Suave'),
    ], validators=[DataRequired()])
    
    lighting_intensity = SelectField('Intensidade da Luz', choices=[
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
    ], validators=[DataRequired()])
    
    lighting_direction = SelectField('Direção da Luz', choices=[
        ('top', 'Superior'),
        ('side', 'Lateral'),
        ('front', 'Frontal'),
        ('back', 'Traseira'),
        ('angled', 'Angular'),
    ], validators=[DataRequired()])
    
    # Color Scheme
    primary_color = SelectField('Cor Primária', choices=[
        ('red', 'Vermelho'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('yellow', 'Amarelo'),
        ('purple', 'Roxo'),
        ('transparent', 'Transparente'),
    ], validators=[DataRequired()])
    
    # Post Processing
    post_processing = SelectMultipleField('Efeitos de Pós-processamento', choices=[
        ('chromatic_aberration', 'Aberração Cromática'),
        ('glow', 'Brilho'),
        ('high_contrast', 'Alto Contraste'),
        ('sharp_details', 'Detalhes Nítidos'),
        ('bloom', 'Bloom'),
        ('vignette', 'Vinheta'),
    ], validators=[DataRequired()])
    
    category = SelectField('Categoria', choices=[
        ('imagem', 'Imagem')
    ], default='imagem', validators=[DataRequired()],
       render_kw={'readonly': True})
    
    submit = SubmitField('Gerar Prompt de Imagem')

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar/texto', methods=['GET', 'POST'])
def criar_texto():
    form = PromptForm()
    if form.validate_on_submit():
        # existing form processing code
        pass
    return render_template('criar_texto.html', form=form)

@app.route('/criar/imagem', methods=['GET', 'POST'])
def criar_imagem():
    form = ImagePromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt(
                project_name=form.project_name.data,
                project_description=form.positive_prompt.data,
                project_objectives=form.negative_prompt.data,
                category='imagem',
                positive_prompt=form.positive_prompt.data,
                negative_prompt=form.negative_prompt.data,
                style=form.style.data,
                material=form.material.data,
                surface_texture=form.surface_texture.data,
                lighting_type=form.lighting_type.data,
                lighting_intensity=form.lighting_intensity.data,
                lighting_direction=form.lighting_direction.data,
                primary_color=form.primary_color.data,
                post_processing=str(form.post_processing.data)
                # NÃO envie language, temperature, tone, persona, protocols aqui!
            )
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de imagem criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de imagem: {str(e)}')
            flash('Erro ao criar prompt de imagem.', 'error')
    return render_template('criar_imagem.html', form=form)

@app.route('/criar/audio')
def criar_audio():
    return render_template('criar_audio.html')

@app.route('/criar/codigo')
def criar_codigo():
    return render_template('criar_codigo.html')

@app.route('/criar/video')
def criar_video():
    return render_template('criar_video.html')

@app.route('/prompts')
def list_prompts():
    prompts = Prompt.query.order_by(Prompt.created_at.desc()).all()
    return render_template('prompts.html', prompts=prompts)

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

@app.route('/prompts/delete/<uuid:id>', methods=['POST'])
def delete_prompt_by_id(id):
    prompt = Prompt.query.get_or_404(id)
    db.session.delete(prompt)
    db.session.commit()
    flash('Prompt excluído com sucesso!', 'success')
    return redirect(url_for('list_prompts'))

@app.route('/prompt/<string:id>/export', methods=['POST'])
def export_prompt(id):
    try:
        prompt = Prompt.query.get_or_404(uuid.UUID(id))
        filename = f"{prompt.project_name}-{prompt.created_at.strftime('%Y%m%d%H%M%S')}.md"
        content = f"""# {prompt.project_name}

**Versão**: 1.0

## Contexto

Este prompt é projetado para configurar um agente de IA como consultor estratégico, fornecendo instruções precisas e profissionais para maximizar a qualidade das respostas.

## Descrição

{prompt.project_description}

## Objetivos

{prompt.project_objectives}
"""
        filepath = os.path.join('static', 'exports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f'Prompt exportado para {filepath}')
        flash('Prompt exportado com sucesso!', 'success')
        return redirect(url_for('view_prompt', id=id))
    except Exception as e:
        logger.error(f'Erro ao exportar prompt {id}: {str(e)}')
        flash('Erro ao exportar prompt.', 'error')
        return redirect(url_for('view_prompt', id=id))

@app.context_processor
def inject_theme():
    return dict(theme='dark')

# Inicialização do banco
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)