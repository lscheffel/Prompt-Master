from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv
from forms import (
    PromptForm, ImagePromptForm, AudioPromptForm, CodePromptForm, VideoPromptForm,
    DocumentPromptForm, PresentationPromptForm, InfographicPromptForm, AnimationPromptForm,
    WebsitePromptForm, DataPromptForm, TranslationPromptForm, SummaryPromptForm,
    MarketingPromptForm, EducationPromptForm
)
from api import api_bp  # API Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///promptmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register API Blueprint
app.register_blueprint(api_bp)

# Modelo de Prompt com UUID
class Prompt(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = db.Column(db.String(100), nullable=False)

    # Campos gerais
    project_description = db.Column(db.Text, nullable=False)
    project_objectives = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False, default='texto')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    # Foreign key to User (optional for backward compatibility)
    # user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    
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

    # Campos específicos de áudio
    audio_duration = db.Column(db.String(20), nullable=True)
    audio_genre = db.Column(db.String(50), nullable=True)
    audio_mood = db.Column(db.String(50), nullable=True)
    audio_instruments = db.Column(db.Text, nullable=True)

    # Campos específicos de código
    code_language = db.Column(db.String(50), nullable=True)
    code_framework = db.Column(db.String(50), nullable=True)
    code_complexity = db.Column(db.String(20), nullable=True)
    code_purpose = db.Column(db.String(50), nullable=True)

    # Campos específicos de vídeo
    video_duration = db.Column(db.String(20), nullable=True)
    video_style = db.Column(db.String(50), nullable=True)
    video_resolution = db.Column(db.String(20), nullable=True)
    video_frame_rate = db.Column(db.String(10), nullable=True)
    video_aspect_ratio = db.Column(db.String(10), nullable=True)

    # Campos específicos de documento
    doc_type = db.Column(db.String(50), nullable=True)
    doc_length = db.Column(db.String(20), nullable=True)
    doc_format = db.Column(db.String(20), nullable=True)
    doc_audience = db.Column(db.String(50), nullable=True)

    # Campos específicos de apresentação
    pres_slides = db.Column(db.String(10), nullable=True)
    pres_audience = db.Column(db.String(50), nullable=True)
    pres_style = db.Column(db.String(50), nullable=True)
    pres_duration = db.Column(db.String(20), nullable=True)

    # Campos específicos de infográfico
    info_data_type = db.Column(db.String(50), nullable=True)
    info_viz_type = db.Column(db.String(50), nullable=True)
    info_theme = db.Column(db.String(50), nullable=True)
    info_elements = db.Column(db.Text, nullable=True)

    # Campos específicos de animação
    anim_style = db.Column(db.String(50), nullable=True)
    anim_duration = db.Column(db.String(20), nullable=True)
    anim_characters = db.Column(db.String(100), nullable=True)
    anim_technique = db.Column(db.String(50), nullable=True)

    # Campos específicos de website
    web_type = db.Column(db.String(50), nullable=True)
    web_technologies = db.Column(db.Text, nullable=True)
    web_features = db.Column(db.Text, nullable=True)
    web_responsive = db.Column(db.String(10), nullable=True)

    # Campos específicos de dados
    data_source = db.Column(db.String(50), nullable=True)
    data_analysis_type = db.Column(db.String(50), nullable=True)
    data_viz_tools = db.Column(db.Text, nullable=True)
    data_output_format = db.Column(db.String(50), nullable=True)

    # Campos específicos de tradução
    trans_source_lang = db.Column(db.String(10), nullable=True)
    trans_target_lang = db.Column(db.String(10), nullable=True)
    trans_domain = db.Column(db.String(50), nullable=True)
    trans_tone = db.Column(db.String(50), nullable=True)

    # Campos específicos de resumo
    sum_source_type = db.Column(db.String(50), nullable=True)
    sum_length = db.Column(db.String(20), nullable=True)
    sum_key_points = db.Column(db.Text, nullable=True)
    sum_format = db.Column(db.String(50), nullable=True)

    # Campos específicos de marketing
    market_campaign_type = db.Column(db.String(50), nullable=True)
    market_target_audience = db.Column(db.String(100), nullable=True)
    market_platform = db.Column(db.String(50), nullable=True)
    market_objective = db.Column(db.String(100), nullable=True)

    # Campos específicos de educação
    edu_level = db.Column(db.String(50), nullable=True)
    edu_subject = db.Column(db.String(100), nullable=True)
    edu_format = db.Column(db.String(50), nullable=True)
    edu_duration = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Prompt {self.project_name}>'

# User Model for Authentication
class User(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

    # Relationship with prompts (commented out until migration is resolved)
    # prompts = db.relationship('Prompt', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Attach db, Prompt, and User to app for API access
app.db = db
app.Prompt = Prompt
app.User = User

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar/texto', methods=['GET', 'POST'])
def criar_texto():
    form = PromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'texto'
            prompt.language = form.language.data
            prompt.temperature = form.temperature.data
            prompt.tone = form.tone.data
            prompt.persona = form.persona.data
            prompt.protocols = form.protocols.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de texto criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de texto: {str(e)}')
            flash('Erro ao criar prompt de texto.', 'error')
    return render_template('criar_texto.html', form=form)

@app.route('/criar/imagem', methods=['GET', 'POST'])
def criar_imagem():
    form = ImagePromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.positive_prompt.data
            prompt.project_objectives = form.negative_prompt.data
            prompt.category = 'imagem'
            prompt.positive_prompt = form.positive_prompt.data
            prompt.negative_prompt = form.negative_prompt.data
            prompt.style = form.style.data
            prompt.material = form.material.data
            prompt.surface_texture = form.surface_texture.data
            prompt.lighting_type = form.lighting_type.data
            prompt.lighting_intensity = form.lighting_intensity.data
            prompt.lighting_direction = form.lighting_direction.data
            prompt.primary_color = form.primary_color.data
            prompt.post_processing = str(form.post_processing.data)
            # NÃO envie language, temperature, tone, persona, protocols aqui!
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de imagem criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de imagem: {str(e)}')
            flash('Erro ao criar prompt de imagem.', 'error')
    return render_template('criar_imagem.html', form=form)

@app.route('/criar/audio', methods=['GET', 'POST'])
def criar_audio():
    form = AudioPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'audio'
            prompt.audio_duration = form.duration.data
            prompt.audio_genre = form.genre.data
            prompt.audio_mood = form.mood.data
            prompt.audio_instruments = str(form.instruments.data)
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de áudio criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de áudio: {str(e)}')
            flash('Erro ao criar prompt de áudio.', 'error')
    return render_template('criar_audio.html', form=form)

@app.route('/criar/codigo', methods=['GET', 'POST'])
def criar_codigo():
    form = CodePromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'codigo'
            prompt.code_language = form.language.data
            prompt.code_framework = form.framework.data
            prompt.code_complexity = form.complexity.data
            prompt.code_purpose = form.purpose.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de código criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de código: {str(e)}')
            flash('Erro ao criar prompt de código.', 'error')
    return render_template('criar_codigo.html', form=form)

@app.route('/criar/video', methods=['GET', 'POST'])
def criar_video():
    form = VideoPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'video'
            prompt.video_duration = form.duration.data
            prompt.video_style = form.style.data
            prompt.video_resolution = form.resolution.data
            prompt.video_frame_rate = form.frame_rate.data
            prompt.video_aspect_ratio = form.aspect_ratio.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de vídeo criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de vídeo: {str(e)}')
            flash('Erro ao criar prompt de vídeo.', 'error')
    return render_template('criar_video.html', form=form)

@app.route('/criar/documento', methods=['GET', 'POST'])
def criar_documento():
    form = DocumentPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'documento'
            prompt.doc_type = form.doc_type.data
            prompt.doc_length = form.doc_length.data
            prompt.doc_format = form.doc_format.data
            prompt.doc_audience = form.doc_audience.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de documento criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de documento: {str(e)}')
            flash('Erro ao criar prompt de documento.', 'error')
    return render_template('criar_documento.html', form=form)

@app.route('/criar/apresentacao', methods=['GET', 'POST'])
def criar_apresentacao():
    form = PresentationPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'apresentacao'
            prompt.pres_slides = form.pres_slides.data
            prompt.pres_audience = form.pres_audience.data
            prompt.pres_style = form.pres_style.data
            prompt.pres_duration = form.pres_duration.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de apresentação criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de apresentação: {str(e)}')
            flash('Erro ao criar prompt de apresentação.', 'error')
    return render_template('criar_apresentacao.html', form=form)

@app.route('/criar/infografico', methods=['GET', 'POST'])
def criar_infografico():
    form = InfographicPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'infografico'
            prompt.info_data_type = form.info_data_type.data
            prompt.info_viz_type = form.info_viz_type.data
            prompt.info_theme = form.info_theme.data
            prompt.info_elements = str(form.info_elements.data)
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de infográfico criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de infográfico: {str(e)}')
            flash('Erro ao criar prompt de infográfico.', 'error')
    return render_template('criar_infografico.html', form=form)

@app.route('/criar/animacao', methods=['GET', 'POST'])
def criar_animacao():
    form = AnimationPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'animacao'
            prompt.anim_style = form.anim_style.data
            prompt.anim_duration = form.anim_duration.data
            prompt.anim_characters = form.anim_characters.data
            prompt.anim_technique = form.anim_technique.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de animação criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de animação: {str(e)}')
            flash('Erro ao criar prompt de animação.', 'error')
    return render_template('criar_animacao.html', form=form)

@app.route('/criar/website', methods=['GET', 'POST'])
def criar_website():
    form = WebsitePromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'website'
            prompt.web_type = form.web_type.data
            prompt.web_technologies = str(form.web_technologies.data)
            prompt.web_features = str(form.web_features.data)
            prompt.web_responsive = form.web_responsive.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de website criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de website: {str(e)}')
            flash('Erro ao criar prompt de website.', 'error')
    return render_template('criar_website.html', form=form)

@app.route('/criar/dados', methods=['GET', 'POST'])
def criar_dados():
    form = DataPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'dados'
            prompt.data_source = form.data_source.data
            prompt.data_analysis_type = form.data_analysis_type.data
            prompt.data_viz_tools = str(form.data_viz_tools.data)
            prompt.data_output_format = form.data_output_format.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de dados criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de dados: {str(e)}')
            flash('Erro ao criar prompt de dados.', 'error')
    return render_template('criar_dados.html', form=form)

@app.route('/criar/traducao', methods=['GET', 'POST'])
def criar_traducao():
    form = TranslationPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'traducao'
            prompt.trans_source_lang = form.trans_source_lang.data
            prompt.trans_target_lang = form.trans_target_lang.data
            prompt.trans_domain = form.trans_domain.data
            prompt.trans_tone = form.trans_tone.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de tradução criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de tradução: {str(e)}')
            flash('Erro ao criar prompt de tradução.', 'error')
    return render_template('criar_traducao.html', form=form)

@app.route('/criar/resumo', methods=['GET', 'POST'])
def criar_resumo():
    form = SummaryPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'resumo'
            prompt.sum_source_type = form.sum_source_type.data
            prompt.sum_length = form.sum_length.data
            prompt.sum_key_points = form.sum_key_points.data
            prompt.sum_format = form.sum_format.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de resumo criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de resumo: {str(e)}')
            flash('Erro ao criar prompt de resumo.', 'error')
    return render_template('criar_resumo.html', form=form)

@app.route('/criar/marketing', methods=['GET', 'POST'])
def criar_marketing():
    form = MarketingPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'marketing'
            prompt.market_campaign_type = form.market_campaign_type.data
            prompt.market_target_audience = form.market_target_audience.data
            prompt.market_platform = form.market_platform.data
            prompt.market_objective = form.market_objective.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de marketing criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de marketing: {str(e)}')
            flash('Erro ao criar prompt de marketing.', 'error')
    return render_template('criar_marketing.html', form=form)

@app.route('/criar/educacao', methods=['GET', 'POST'])
def criar_educacao():
    form = EducationPromptForm()
    if form.validate_on_submit():
        try:
            prompt = Prompt()
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.category = 'educacao'
            prompt.edu_level = form.edu_level.data
            prompt.edu_subject = form.edu_subject.data
            prompt.edu_format = form.edu_format.data
            prompt.edu_duration = form.edu_duration.data
            db.session.add(prompt)
            db.session.commit()
            flash('Prompt de educação criado com sucesso!', 'success')
            return redirect(url_for('list_prompts'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao criar prompt de educação: {str(e)}')
            flash('Erro ao criar prompt de educação.', 'error')
    return render_template('criar_educacao.html', form=form)

@app.route('/prompts')
def list_prompts():
    prompts = Prompt.query.order_by(Prompt.created_at.desc()).all()
    return render_template('prompts.html', prompts=prompts)

@app.route('/prompt/<string:id>')
def view_prompt(id):
    try:
        prompt = Prompt.query.get_or_404(uuid.UUID(id))
        logger.info(f'Prompt {id} visualizado.')

        # Base instructions text
        base_instructions = """Chatbot, as instruções a seguir são apresentadas em formato estruturado JSON, contendo regras, diretrizes e configurações detalhadas para seu comportamento. É imprescindível que você siga rigorosamente todas as especificações, garantindo respostas precisas, concisas e alinhadas com as preferências do usuário. Todas as respostas devem ser exclusivamente em português brasileiro, sem exceção. Caso qualquer informação necessária para uma resposta esteja ausente ou ambígua, você deve solicitar esclarecimentos ao usuário de forma clara e educada, evitando qualquer suposição ou invenção de dados que possa levar a alucinações. Priorize a clareza, a aderência às instruções e a consistência no tom e estilo definidos."""

        # Create complete JSON data for export
        prompt_data = {
            'base_instructions': base_instructions,
            'project_name': prompt.project_name,
            'project_description': prompt.project_description,
            'project_objectives': prompt.project_objectives,
            'category': prompt.category,
            'created_at': prompt.created_at.strftime('%d/%m/%Y %H:%M:%S') if prompt.created_at else None,
        }

        # Add category-specific fields
        if prompt.category == 'texto':
            prompt_data.update({
                'language': prompt.language,
                'temperature': prompt.temperature,
                'tone': prompt.tone,
                'persona': prompt.persona,
                'protocols': prompt.protocols,
            })
        elif prompt.category == 'imagem':
            prompt_data.update({
                'positive_prompt': prompt.positive_prompt,
                'negative_prompt': prompt.negative_prompt,
                'style': prompt.style,
                'material': prompt.material,
                'surface_texture': prompt.surface_texture,
                'lighting_type': prompt.lighting_type,
                'lighting_intensity': prompt.lighting_intensity,
                'lighting_direction': prompt.lighting_direction,
                'primary_color': prompt.primary_color,
                'post_processing': prompt.post_processing,
            })
        elif prompt.category == 'audio':
            prompt_data.update({
                'audio_duration': prompt.audio_duration,
                'audio_genre': prompt.audio_genre,
                'audio_mood': prompt.audio_mood,
                'audio_instruments': prompt.audio_instruments,
            })
        elif prompt.category == 'codigo':
            prompt_data.update({
                'code_language': prompt.code_language,
                'code_framework': prompt.code_framework,
                'code_complexity': prompt.code_complexity,
                'code_purpose': prompt.code_purpose,
            })
        elif prompt.category == 'video':
            prompt_data.update({
                'video_duration': prompt.video_duration,
                'video_style': prompt.video_style,
                'video_resolution': prompt.video_resolution,
                'video_frame_rate': prompt.video_frame_rate,
                'video_aspect_ratio': prompt.video_aspect_ratio,
            })
        elif prompt.category == 'documento':
            prompt_data.update({
                'doc_type': prompt.doc_type,
                'doc_length': prompt.doc_length,
                'doc_format': prompt.doc_format,
                'doc_audience': prompt.doc_audience,
            })
        elif prompt.category == 'apresentacao':
            prompt_data.update({
                'pres_slides': prompt.pres_slides,
                'pres_audience': prompt.pres_audience,
                'pres_style': prompt.pres_style,
                'pres_duration': prompt.pres_duration,
            })
        elif prompt.category == 'infografico':
            prompt_data.update({
                'info_data_type': prompt.info_data_type,
                'info_viz_type': prompt.info_viz_type,
                'info_theme': prompt.info_theme,
                'info_elements': prompt.info_elements,
            })
        elif prompt.category == 'animacao':
            prompt_data.update({
                'anim_style': prompt.anim_style,
                'anim_duration': prompt.anim_duration,
                'anim_characters': prompt.anim_characters,
                'anim_technique': prompt.anim_technique,
            })
        elif prompt.category == 'website':
            prompt_data.update({
                'web_type': prompt.web_type,
                'web_technologies': prompt.web_technologies,
                'web_features': prompt.web_features,
                'web_responsive': prompt.web_responsive,
            })
        elif prompt.category == 'dados':
            prompt_data.update({
                'data_source': prompt.data_source,
                'data_analysis_type': prompt.data_analysis_type,
                'data_viz_tools': prompt.data_viz_tools,
                'data_output_format': prompt.data_output_format,
            })
        elif prompt.category == 'resumo':
            prompt_data.update({
                'sum_source_type': prompt.sum_source_type,
                'sum_length': prompt.sum_length,
                'sum_key_points': prompt.sum_key_points,
                'sum_format': prompt.sum_format,
            })
        elif prompt.category == 'marketing':
            prompt_data.update({
                'market_campaign_type': prompt.market_campaign_type,
                'market_target_audience': prompt.market_target_audience,
                'market_platform': prompt.market_platform,
                'market_objective': prompt.market_objective,
            })
        elif prompt.category == 'educacao':
            prompt_data.update({
                'edu_level': prompt.edu_level,
                'edu_subject': prompt.edu_subject,
                'edu_format': prompt.edu_format,
                'edu_duration': prompt.edu_duration,
            })
        elif prompt.category == 'traducao':
            prompt_data.update({
                'trans_source_lang': prompt.trans_source_lang,
                'trans_target_lang': prompt.trans_target_lang,
                'trans_domain': prompt.trans_domain,
                'trans_tone': prompt.trans_tone,
            })

        import json
        prompt_data_json = json.dumps(prompt_data, ensure_ascii=False, indent=2)

        logger.info(f'[VERBOSE] JSON data for prompt {id}: length={len(prompt_data_json)}, keys={list(prompt_data.keys())}')
        logger.info(f'[VERBOSE] JSON content preview: {prompt_data_json[:200]}...')

        return render_template('view_prompt.html', prompt=prompt, prompt_data_json=prompt_data_json)
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

@app.route('/prompt/<string:id>/export')
def export_prompt(id):
    try:
        prompt = Prompt.query.get_or_404(uuid.UUID(id))
        filename = f"{prompt.project_name}-{prompt.created_at.strftime('%Y%m%d%H%M%S')}.md"

        # Base instructions text
        base_instructions = """Chatbot, as instruções a seguir são apresentadas em formato estruturado JSON, contendo regras, diretrizes e configurações detalhadas para seu comportamento. É imprescindível que você siga rigorosamente todas as especificações, garantindo respostas precisas, concisas e alinhadas com as preferências do usuário. Todas as respostas devem ser exclusivamente em português brasileiro, sem exceção. Caso qualquer informação necessária para uma resposta esteja ausente ou ambígua, você deve solicitar esclarecimentos ao usuário de forma clara e educada, evitando qualquer suposição ou invenção de dados que possa levar a alucinações. Priorize a clareza, a aderência às instruções e a consistência no tom e estilo definidos."""

        # Conteúdo base
        content = f"""{base_instructions}

# {prompt.project_name}

**Versão**: 1.0
**Categoria**: {prompt.category.title()}
**Data de Criação**: {prompt.created_at.strftime('%d/%m/%Y %H:%M:%S')}

## Contexto

Este prompt é projetado para configurar um agente de IA como consultor estratégico, fornecendo instruções precisas e profissionais para maximizar a qualidade das respostas.

## Descrição

{prompt.project_description}

## Objetivos

{prompt.project_objectives}
"""

        # Adicionar campos específicos por categoria
        if prompt.category == 'texto':
            if prompt.language:
                content += f"\n## Linguagem Principal\n\n{prompt.language}"
            if prompt.temperature:
                content += f"\n## Temperatura do Chat\n\n{prompt.temperature}"
            if prompt.tone:
                content += f"\n## Tom do Chat\n\n{prompt.tone}"
            if prompt.persona:
                content += f"\n## Persona\n\n{prompt.persona}"
            if prompt.protocols:
                content += f"\n## Protocolos\n\n{prompt.protocols}"

        elif prompt.category == 'imagem':
            if prompt.positive_prompt:
                content += f"\n## Prompt Positivo\n\n{prompt.positive_prompt}"
            if prompt.negative_prompt:
                content += f"\n## Prompt Negativo\n\n{prompt.negative_prompt}"
            if prompt.style:
                content += f"\n## Estilo\n\n{prompt.style}"
            if prompt.material:
                content += f"\n## Material\n\n{prompt.material}"
            if prompt.surface_texture:
                content += f"\n## Textura de Superfície\n\n{prompt.surface_texture}"
            if prompt.lighting_type:
                content += f"\n## Tipo de Iluminação\n\n{prompt.lighting_type}"
            if prompt.lighting_intensity:
                content += f"\n## Intensidade da Luz\n\n{prompt.lighting_intensity}"
            if prompt.lighting_direction:
                content += f"\n## Direção da Luz\n\n{prompt.lighting_direction}"
            if prompt.primary_color:
                content += f"\n## Cor Primária\n\n{prompt.primary_color}"
            if prompt.post_processing:
                content += f"\n## Pós-processamento\n\n{prompt.post_processing}"

        elif prompt.category == 'audio':
            if prompt.audio_duration:
                content += f"\n## Duração\n\n{prompt.audio_duration}"
            if prompt.audio_genre:
                content += f"\n## Gênero\n\n{prompt.audio_genre}"
            if prompt.audio_mood:
                content += f"\n## Clima/Atmosfera\n\n{prompt.audio_mood}"
            if prompt.audio_instruments:
                content += f"\n## Instrumentos\n\n{prompt.audio_instruments}"

        elif prompt.category == 'codigo':
            if prompt.code_language:
                content += f"\n## Linguagem de Programação\n\n{prompt.code_language}"
            if prompt.code_framework:
                content += f"\n## Framework/Biblioteca\n\n{prompt.code_framework}"
            if prompt.code_complexity:
                content += f"\n## Complexidade\n\n{prompt.code_complexity}"
            if prompt.code_purpose:
                content += f"\n## Propósito\n\n{prompt.code_purpose}"

        elif prompt.category == 'video':
            if prompt.video_duration:
                content += f"\n## Duração\n\n{prompt.video_duration}"
            if prompt.video_style:
                content += f"\n## Estilo Visual\n\n{prompt.video_style}"
            if prompt.video_resolution:
                content += f"\n## Resolução\n\n{prompt.video_resolution}"
            if prompt.video_frame_rate:
                content += f"\n## Taxa de Quadros\n\n{prompt.video_frame_rate}"
            if prompt.video_aspect_ratio:
                content += f"\n## Proporção de Tela\n\n{prompt.video_aspect_ratio}"

        elif prompt.category == 'documento':
            if prompt.doc_type:
                content += f"\n## Tipo de Documento\n\n{prompt.doc_type}"
            if prompt.doc_length:
                content += f"\n## Comprimento\n\n{prompt.doc_length}"
            if prompt.doc_format:
                content += f"\n## Formato\n\n{prompt.doc_format}"
            if prompt.doc_audience:
                content += f"\n## Público-Alvo\n\n{prompt.doc_audience}"

        elif prompt.category == 'apresentacao':
            if prompt.pres_slides:
                content += f"\n## Número de Slides\n\n{prompt.pres_slides}"
            if prompt.pres_audience:
                content += f"\n## Público-Alvo\n\n{prompt.pres_audience}"
            if prompt.pres_style:
                content += f"\n## Estilo Visual\n\n{prompt.pres_style}"
            if prompt.pres_duration:
                content += f"\n## Duração Estimada\n\n{prompt.pres_duration}"

        elif prompt.category == 'infografico':
            if prompt.info_data_type:
                content += f"\n## Tipo de Dados\n\n{prompt.info_data_type}"
            if prompt.info_viz_type:
                content += f"\n## Tipo de Visualização\n\n{prompt.info_viz_type}"
            if prompt.info_theme:
                content += f"\n## Tema/Tom\n\n{prompt.info_theme}"
            if prompt.info_elements:
                content += f"\n## Elementos Visuais\n\n{prompt.info_elements}"

        elif prompt.category == 'animacao':
            if prompt.anim_style:
                content += f"\n## Estilo de Animação\n\n{prompt.anim_style}"
            if prompt.anim_duration:
                content += f"\n## Duração\n\n{prompt.anim_duration}"
            if prompt.anim_characters:
                content += f"\n## Personagens/Elementos\n\n{prompt.anim_characters}"
            if prompt.anim_technique:
                content += f"\n## Técnica\n\n{prompt.anim_technique}"

        elif prompt.category == 'website':
            if prompt.web_type:
                content += f"\n## Tipo de Site\n\n{prompt.web_type}"
            if prompt.web_technologies:
                content += f"\n## Tecnologias\n\n{prompt.web_technologies}"
            if prompt.web_features:
                content += f"\n## Funcionalidades\n\n{prompt.web_features}"
            if prompt.web_responsive:
                content += f"\n## Design Responsivo\n\n{prompt.web_responsive}"

        elif prompt.category == 'dados':
            if prompt.data_source:
                content += f"\n## Fonte de Dados\n\n{prompt.data_source}"
            if prompt.data_analysis_type:
                content += f"\n## Tipo de Análise\n\n{prompt.data_analysis_type}"
            if prompt.data_viz_tools:
                content += f"\n## Ferramentas de Visualização\n\n{prompt.data_viz_tools}"
            if prompt.data_output_format:
                content += f"\n## Formato de Saída\n\n{prompt.data_output_format}"

        elif prompt.category == 'traducao':
            if prompt.trans_source_lang:
                content += f"\n## Idioma de Origem\n\n{prompt.trans_source_lang}"
            if prompt.trans_target_lang:
                content += f"\n## Idioma de Destino\n\n{prompt.trans_target_lang}"
            if prompt.trans_domain:
                content += f"\n## Domínio\n\n{prompt.trans_domain}"
            if prompt.trans_tone:
                content += f"\n## Tom\n\n{prompt.trans_tone}"

        elif prompt.category == 'resumo':
            if prompt.sum_source_type:
                content += f"\n## Tipo de Fonte\n\n{prompt.sum_source_type}"
            if prompt.sum_length:
                content += f"\n## Comprimento do Resumo\n\n{prompt.sum_length}"
            if prompt.sum_key_points:
                content += f"\n## Pontos-Chave\n\n{prompt.sum_key_points}"
            if prompt.sum_format:
                content += f"\n## Formato de Saída\n\n{prompt.sum_format}"

        elif prompt.category == 'marketing':
            if prompt.market_campaign_type:
                content += f"\n## Tipo de Campanha\n\n{prompt.market_campaign_type}"
            if prompt.market_target_audience:
                content += f"\n## Público-Alvo\n\n{prompt.market_target_audience}"
            if prompt.market_platform:
                content += f"\n## Plataforma Principal\n\n{prompt.market_platform}"
            if prompt.market_objective:
                content += f"\n## Objetivo da Campanha\n\n{prompt.market_objective}"

        elif prompt.category == 'educacao':
            if prompt.edu_level:
                content += f"\n## Nível Educacional\n\n{prompt.edu_level}"
            if prompt.edu_subject:
                content += f"\n## Assunto/Matéria\n\n{prompt.edu_subject}"
            if prompt.edu_format:
                content += f"\n## Formato\n\n{prompt.edu_format}"
            if prompt.edu_duration:
                content += f"\n## Duração\n\n{prompt.edu_duration}"

        # Return the file directly for download
        from flask import Response
        response = Response(
            content,
            mimetype='text/markdown',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Length': len(content.encode('utf-8'))
            }
        )
        return response
    except Exception as e:
        logger.error(f'Erro ao exportar prompt {id}: {str(e)}')
        flash('Erro ao exportar prompt.', 'error')
        return redirect(url_for('view_prompt', id=id))

@app.route('/prompt/<string:id>/edit', methods=['GET', 'POST'])
def edit_prompt(id):
    prompt = Prompt.query.get_or_404(uuid.UUID(id))
    if prompt.category == 'imagem':
        form = ImagePromptForm(obj=prompt)
        # Corrigir campo de múltipla seleção
        if request.method == 'GET' and prompt.post_processing:
            if isinstance(prompt.post_processing, str):
                # Remove colchetes e aspas se vier como string
                import ast
                try:
                    form.post_processing.data = ast.literal_eval(prompt.post_processing)
                except Exception:
                    form.post_processing.data = []
            else:
                form.post_processing.data = prompt.post_processing
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.positive_prompt = form.positive_prompt.data
            prompt.negative_prompt = form.negative_prompt.data
            prompt.style = form.style.data
            prompt.material = form.material.data
            prompt.surface_texture = form.surface_texture.data
            prompt.lighting_type = form.lighting_type.data
            prompt.lighting_intensity = form.lighting_intensity.data
            prompt.lighting_direction = form.lighting_direction.data
            prompt.primary_color = form.primary_color.data
            prompt.post_processing = str(form.post_processing.data)
            db.session.commit()
            flash('Prompt de imagem atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_imagem.html', form=form, editar=True)
    elif prompt.category == 'audio':
        form = AudioPromptForm(obj=prompt)
        if request.method == 'GET' and prompt.audio_instruments:
            if isinstance(prompt.audio_instruments, str):
                import ast
                try:
                    form.instruments.data = ast.literal_eval(prompt.audio_instruments)
                except Exception:
                    form.instruments.data = []
            else:
                form.instruments.data = prompt.audio_instruments
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.audio_duration = form.duration.data
            prompt.audio_genre = form.genre.data
            prompt.audio_mood = form.mood.data
            prompt.audio_instruments = str(form.instruments.data)
            db.session.commit()
            flash('Prompt de áudio atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_audio.html', form=form, editar=True)
    elif prompt.category == 'codigo':
        form = CodePromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.code_language = form.language.data
            prompt.code_framework = form.framework.data
            prompt.code_complexity = form.complexity.data
            prompt.code_purpose = form.purpose.data
            db.session.commit()
            flash('Prompt de código atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_codigo.html', form=form, editar=True)
    elif prompt.category == 'video':
        form = VideoPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.video_duration = form.duration.data
            prompt.video_style = form.style.data
            prompt.video_resolution = form.resolution.data
            prompt.video_frame_rate = form.frame_rate.data
            prompt.video_aspect_ratio = form.aspect_ratio.data
            db.session.commit()
            flash('Prompt de vídeo atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_video.html', form=form, editar=True)
    elif prompt.category == 'documento':
        form = DocumentPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.doc_type = form.doc_type.data
            prompt.doc_length = form.doc_length.data
            prompt.doc_format = form.doc_format.data
            prompt.doc_audience = form.doc_audience.data
            db.session.commit()
            flash('Prompt de documento atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_documento.html', form=form, editar=True)
    elif prompt.category == 'apresentacao':
        form = PresentationPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.pres_slides = form.pres_slides.data
            prompt.pres_audience = form.pres_audience.data
            prompt.pres_style = form.pres_style.data
            prompt.pres_duration = form.pres_duration.data
            db.session.commit()
            flash('Prompt de apresentação atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_apresentacao.html', form=form, editar=True)
    elif prompt.category == 'infografico':
        form = InfographicPromptForm(obj=prompt)
        if request.method == 'GET' and prompt.info_elements:
            if isinstance(prompt.info_elements, str):
                import ast
                try:
                    form.info_elements.data = ast.literal_eval(prompt.info_elements)
                except Exception:
                    form.info_elements.data = []
            else:
                form.info_elements.data = prompt.info_elements
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.info_data_type = form.info_data_type.data
            prompt.info_viz_type = form.info_viz_type.data
            prompt.info_theme = form.info_theme.data
            prompt.info_elements = str(form.info_elements.data)
            db.session.commit()
            flash('Prompt de infográfico atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_infografico.html', form=form, editar=True)
    elif prompt.category == 'animacao':
        form = AnimationPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.anim_style = form.anim_style.data
            prompt.anim_duration = form.anim_duration.data
            prompt.anim_characters = form.anim_characters.data
            prompt.anim_technique = form.anim_technique.data
            db.session.commit()
            flash('Prompt de animação atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_animacao.html', form=form, editar=True)
    elif prompt.category == 'website':
        form = WebsitePromptForm(obj=prompt)
        if request.method == 'GET' and prompt.web_technologies:
            if isinstance(prompt.web_technologies, str):
                import ast
                try:
                    form.web_technologies.data = ast.literal_eval(prompt.web_technologies)
                except Exception:
                    form.web_technologies.data = []
            else:
                form.web_technologies.data = prompt.web_technologies
        if request.method == 'GET' and prompt.web_features:
            if isinstance(prompt.web_features, str):
                import ast
                try:
                    form.web_features.data = ast.literal_eval(prompt.web_features)
                except Exception:
                    form.web_features.data = []
            else:
                form.web_features.data = prompt.web_features
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.web_type = form.web_type.data
            prompt.web_technologies = str(form.web_technologies.data)
            prompt.web_features = str(form.web_features.data)
            prompt.web_responsive = form.web_responsive.data
            db.session.commit()
            flash('Prompt de website atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_website.html', form=form, editar=True)
    elif prompt.category == 'dados':
        form = DataPromptForm(obj=prompt)
        if request.method == 'GET' and prompt.data_viz_tools:
            if isinstance(prompt.data_viz_tools, str):
                import ast
                try:
                    form.data_viz_tools.data = ast.literal_eval(prompt.data_viz_tools)
                except Exception:
                    form.data_viz_tools.data = []
            else:
                form.data_viz_tools.data = prompt.data_viz_tools
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.data_source = form.data_source.data
            prompt.data_analysis_type = form.data_analysis_type.data
            prompt.data_viz_tools = str(form.data_viz_tools.data)
            prompt.data_output_format = form.data_output_format.data
            db.session.commit()
            flash('Prompt de dados atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_dados.html', form=form, editar=True)
    elif prompt.category == 'traducao':
        form = TranslationPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.trans_source_lang = form.trans_source_lang.data
            prompt.trans_target_lang = form.trans_target_lang.data
            prompt.trans_domain = form.trans_domain.data
            prompt.trans_tone = form.trans_tone.data
            db.session.commit()
            flash('Prompt de tradução atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_traducao.html', form=form, editar=True)
    elif prompt.category == 'resumo':
        form = SummaryPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.sum_source_type = form.sum_source_type.data
            prompt.sum_length = form.sum_length.data
            prompt.sum_key_points = form.sum_key_points.data
            prompt.sum_format = form.sum_format.data
            db.session.commit()
            flash('Prompt de resumo atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_resumo.html', form=form, editar=True)
    elif prompt.category == 'marketing':
        form = MarketingPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.market_campaign_type = form.market_campaign_type.data
            prompt.market_target_audience = form.market_target_audience.data
            prompt.market_platform = form.market_platform.data
            prompt.market_objective = form.market_objective.data
            db.session.commit()
            flash('Prompt de marketing atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_marketing.html', form=form, editar=True)
    elif prompt.category == 'educacao':
        form = EducationPromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.edu_level = form.edu_level.data
            prompt.edu_subject = form.edu_subject.data
            prompt.edu_format = form.edu_format.data
            prompt.edu_duration = form.edu_duration.data
            db.session.commit()
            flash('Prompt de educação atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_educacao.html', form=form, editar=True)
    else:
        form = PromptForm(obj=prompt)
        if form.validate_on_submit():
            prompt.project_name = form.project_name.data
            prompt.project_description = form.project_description.data
            prompt.project_objectives = form.project_objectives.data
            prompt.language = form.language.data
            prompt.temperature = form.temperature.data
            prompt.tone = form.tone.data
            prompt.persona = form.persona.data
            prompt.protocols = form.protocols.data
            db.session.commit()
            flash('Prompt de texto atualizado com sucesso!', 'success')
            return redirect(url_for('view_prompt', id=id))
        return render_template('criar_texto.html', form=form, editar=True)

@app.context_processor
def inject_theme():
    return dict(theme='dark')

# Inicialização do banco
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)