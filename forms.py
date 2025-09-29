from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

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
        ('video', 'Vídeo'),
        ('documento', 'Documento'),
        ('apresentacao', 'Apresentação'),
        ('infografico', 'Infográfico'),
        ('animacao', 'Animação'),
        ('website', 'Website/App'),
        ('dados', 'Dados'),
        ('traducao', 'Tradução'),
        ('resumo', 'Resumo'),
        ('marketing', 'Marketing'),
        ('educacao', 'Educação')
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

class AudioPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Audio specific fields
    duration = SelectField('Duração', choices=[
        ('short', 'Curto (até 30s)'),
        ('medium', 'Médio (30s - 2min)'),
        ('long', 'Longo (acima de 2min)'),
    ], validators=[DataRequired()])

    genre = SelectField('Gênero', choices=[
        ('classical', 'Clássico'),
        ('electronic', 'Eletrônico'),
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('jazz', 'Jazz'),
        ('ambient', 'Ambiente'),
        ('soundtrack', 'Trilha Sonora'),
    ], validators=[DataRequired()])

    mood = SelectField('Clima/Atmosfera', choices=[
        ('calm', 'Calmo'),
        ('energetic', 'Energético'),
        ('melancholic', 'Melancólico'),
        ('uplifting', 'Elevador'),
        ('dark', 'Escuro'),
        ('playful', 'Brincalhão'),
    ], validators=[DataRequired()])

    instruments = SelectMultipleField('Instrumentos', choices=[
        ('piano', 'Piano'),
        ('guitar', 'Guitarra'),
        ('drums', 'Bateria'),
        ('bass', 'Baixo'),
        ('strings', 'Cordas'),
        ('brass', 'Metais'),
        ('woodwind', 'Madeiras'),
        ('synthesizer', 'Sintetizador'),
        ('vocals', 'Vocais'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('audio', 'Áudio')
    ], default='audio', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Áudio')

class CodePromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Code specific fields
    language = SelectField('Linguagem de Programação', choices=[
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('typescript', 'TypeScript'),
    ], validators=[DataRequired()])

    framework = SelectField('Framework/Biblioteca', choices=[
        ('none', 'Nenhum'),
        ('flask', 'Flask'),
        ('django', 'Django'),
        ('react', 'React'),
        ('vue', 'Vue.js'),
        ('angular', 'Angular'),
        ('spring', 'Spring'),
        ('express', 'Express.js'),
        ('laravel', 'Laravel'),
        ('rails', 'Rails'),
    ], validators=[DataRequired()])

    complexity = SelectField('Complexidade', choices=[
        ('simple', 'Simples'),
        ('medium', 'Médio'),
        ('complex', 'Complexo'),
        ('advanced', 'Avançado'),
    ], validators=[DataRequired()])

    purpose = SelectField('Propósito', choices=[
        ('web_app', 'Aplicação Web'),
        ('api', 'API'),
        ('cli', 'Linha de Comando'),
        ('library', 'Biblioteca'),
        ('script', 'Script'),
        ('game', 'Jogo'),
        ('data_analysis', 'Análise de Dados'),
        ('automation', 'Automação'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('codigo', 'Código')
    ], default='codigo', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Código')

class VideoPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Video specific fields
    duration = SelectField('Duração', choices=[
        ('short', 'Curto (até 30s)'),
        ('medium', 'Médio (30s - 2min)'),
        ('long', 'Longo (acima de 2min)'),
        ('feature', 'Longa-metragem'),
    ], validators=[DataRequired()])

    style = SelectField('Estilo Visual', choices=[
        ('realistic', 'Realista'),
        ('animated', 'Animado'),
        ('abstract', 'Abstrato'),
        ('documentary', 'Documentário'),
        ('music_video', 'Videoclipe'),
        ('commercial', 'Comercial'),
        ('educational', 'Educacional'),
    ], validators=[DataRequired()])

    resolution = SelectField('Resolução', choices=[
        ('720p', '720p HD'),
        ('1080p', '1080p Full HD'),
        ('4k', '4K Ultra HD'),
        ('8k', '8K'),
    ], validators=[DataRequired()])

    frame_rate = SelectField('Taxa de Quadros', choices=[
        ('24', '24 fps (Cinema)'),
        ('30', '30 fps (NTSC)'),
        ('60', '60 fps (Alta Velocidade)'),
    ], validators=[DataRequired()])

    aspect_ratio = SelectField('Proporção de Tela', choices=[
        ('16:9', '16:9 (Widescreen)'),
        ('4:3', '4:3 (Padrão)'),
        ('21:9', '21:9 (Ultrawide)'),
        ('1:1', '1:1 (Quadrado)'),
        ('9:16', '9:16 (Vertical)'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('video', 'Vídeo')
    ], default='video', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Vídeo')

class DocumentPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Document specific fields
    doc_type = SelectField('Tipo de Documento', choices=[
        ('report', 'Relatório'),
        ('article', 'Artigo'),
        ('contract', 'Contrato'),
        ('manual', 'Manual'),
        ('proposal', 'Proposta'),
        ('presentation', 'Apresentação'),
        ('ebook', 'E-book'),
    ], validators=[DataRequired()])

    doc_length = SelectField('Comprimento', choices=[
        ('short', 'Curto (1-5 páginas)'),
        ('medium', 'Médio (5-20 páginas)'),
        ('long', 'Longo (20+ páginas)'),
    ], validators=[DataRequired()])

    doc_format = SelectField('Formato', choices=[
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('html', 'HTML'),
        ('markdown', 'Markdown'),
        ('text', 'Texto Puro'),
    ], validators=[DataRequired()])

    doc_audience = SelectField('Público-Alvo', choices=[
        ('general', 'Geral'),
        ('technical', 'Técnico'),
        ('executive', 'Executivo'),
        ('academic', 'Acadêmico'),
        ('children', 'Infantil'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('documento', 'Documento')
    ], default='documento', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Documento')

class PresentationPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Presentation specific fields
    pres_slides = SelectField('Número de Slides', choices=[
        ('5-10', '5-10 slides'),
        ('10-20', '10-20 slides'),
        ('20-30', '20-30 slides'),
        ('30+', '30+ slides'),
    ], validators=[DataRequired()])

    pres_audience = SelectField('Público-Alvo', choices=[
        ('students', 'Estudantes'),
        ('professionals', 'Profissionais'),
        ('executives', 'Executivos'),
        ('general', 'Geral'),
        ('technical', 'Técnico'),
    ], validators=[DataRequired()])

    pres_style = SelectField('Estilo Visual', choices=[
        ('minimalist', 'Minimalista'),
        ('corporate', 'Corporativo'),
        ('creative', 'Criativo'),
        ('educational', 'Educacional'),
        ('technical', 'Técnico'),
    ], validators=[DataRequired()])

    pres_duration = SelectField('Duração Estimada', choices=[
        ('5-10', '5-10 minutos'),
        ('10-20', '10-20 minutos'),
        ('20-30', '20-30 minutos'),
        ('30+', '30+ minutos'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('apresentacao', 'Apresentação')
    ], default='apresentacao', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Apresentação')

class InfographicPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Infographic specific fields
    info_data_type = SelectField('Tipo de Dados', choices=[
        ('statistics', 'Estatísticas'),
        ('timeline', 'Linha do Tempo'),
        ('process', 'Processo'),
        ('comparison', 'Comparação'),
        ('geographic', 'Geográfico'),
        ('hierarchical', 'Hierárquico'),
    ], validators=[DataRequired()])

    info_viz_type = SelectField('Tipo de Visualização', choices=[
        ('chart', 'Gráfico'),
        ('diagram', 'Diagrama'),
        ('map', 'Mapa'),
        ('timeline', 'Timeline'),
        ('icons', 'Ícones'),
        ('photography', 'Fotografia'),
    ], validators=[DataRequired()])

    info_theme = SelectField('Tema/Tom', choices=[
        ('professional', 'Profissional'),
        ('fun', 'Divertido'),
        ('serious', 'Sério'),
        ('educational', 'Educacional'),
        ('marketing', 'Marketing'),
        ('minimalist', 'Minimalista'),
    ], validators=[DataRequired()])

    info_elements = SelectMultipleField('Elementos Visuais', choices=[
        ('icons', 'Ícones'),
        ('illustrations', 'Ilustrações'),
        ('photos', 'Fotos'),
        ('charts', 'Gráficos'),
        ('text', 'Texto'),
        ('colors', 'Cores'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('infografico', 'Infográfico')
    ], default='infografico', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Infográfico')

class AnimationPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Animation specific fields
    anim_style = SelectField('Estilo de Animação', choices=[
        ('2d_cartoon', '2D Cartoon'),
        ('3d_realistic', '3D Realista'),
        ('stop_motion', 'Stop Motion'),
        ('motion_graphics', 'Motion Graphics'),
        ('whiteboard', 'Whiteboard'),
        ('cutout', 'Cutout'),
    ], validators=[DataRequired()])

    anim_duration = SelectField('Duração', choices=[
        ('short', 'Curto (5-15s)'),
        ('medium', 'Médio (15-60s)'),
        ('long', 'Longo (1-5min)'),
        ('feature', 'Longo-metragem'),
    ], validators=[DataRequired()])

    anim_characters = TextAreaField('Personagens/Elementos', validators=[DataRequired()])

    anim_technique = SelectField('Técnica', choices=[
        ('traditional', 'Tradicional'),
        ('digital', 'Digital'),
        ('hybrid', 'Híbrida'),
        ('cgi', 'CGI'),
        ('hand_drawn', 'Desenhado à Mão'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('animacao', 'Animação')
    ], default='animacao', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Animação')

class WebsitePromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Website specific fields
    web_type = SelectField('Tipo de Site', choices=[
        ('landing_page', 'Landing Page'),
        ('corporate', 'Corporativo'),
        ('ecommerce', 'E-commerce'),
        ('blog', 'Blog'),
        ('portfolio', 'Portfólio'),
        ('webapp', 'Web App'),
        ('educational', 'Educacional'),
    ], validators=[DataRequired()])

    web_technologies = SelectMultipleField('Tecnologias', choices=[
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('react', 'React'),
        ('vue', 'Vue.js'),
        ('angular', 'Angular'),
        ('python', 'Python'),
        ('php', 'PHP'),
        ('nodejs', 'Node.js'),
        ('wordpress', 'WordPress'),
    ], validators=[DataRequired()])

    web_features = SelectMultipleField('Funcionalidades', choices=[
        ('responsive', 'Responsivo'),
        ('contact_form', 'Formulário de Contato'),
        ('blog', 'Blog'),
        ('ecommerce', 'E-commerce'),
        ('user_auth', 'Autenticação'),
        ('dashboard', 'Dashboard'),
        ('api', 'API'),
        ('multilingual', 'Multilíngue'),
    ], validators=[DataRequired()])

    web_responsive = SelectField('Design Responsivo', choices=[
        ('yes', 'Sim'),
        ('no', 'Não'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('website', 'Website/App')
    ], default='website', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Website')

class DataPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Data specific fields
    data_source = SelectField('Fonte de Dados', choices=[
        ('database', 'Banco de Dados'),
        ('api', 'API'),
        ('csv', 'CSV/Excel'),
        ('web_scraping', 'Web Scraping'),
        ('survey', 'Pesquisa'),
        ('sensors', 'Sensores/IoT'),
        ('social_media', 'Redes Sociais'),
    ], validators=[DataRequired()])

    data_analysis_type = SelectField('Tipo de Análise', choices=[
        ('descriptive', 'Descritiva'),
        ('diagnostic', 'Diagnóstica'),
        ('predictive', 'Preditiva'),
        ('prescriptive', 'Prescritiva'),
        ('exploratory', 'Exploratória'),
    ], validators=[DataRequired()])

    data_viz_tools = SelectMultipleField('Ferramentas de Visualização', choices=[
        ('tableau', 'Tableau'),
        ('powerbi', 'Power BI'),
        ('excel', 'Excel'),
        ('python', 'Python (Matplotlib/Seaborn)'),
        ('r', 'R'),
        ('d3', 'D3.js'),
        ('chartjs', 'Chart.js'),
        ('ggplot', 'ggplot2'),
    ], validators=[DataRequired()])

    data_output_format = SelectField('Formato de Saída', choices=[
        ('dashboard', 'Dashboard'),
        ('report', 'Relatório'),
        ('presentation', 'Apresentação'),
        ('interactive', 'Interativo'),
        ('static_charts', 'Gráficos Estáticos'),
        ('api', 'API'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('dados', 'Dados')
    ], default='dados', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Dados')

class TranslationPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Translation specific fields
    trans_source_lang = SelectField('Idioma de Origem', choices=[
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
        ('fr', 'Francês'),
        ('de', 'Alemão'),
        ('it', 'Italiano'),
        ('pt', 'Português'),
        ('ja', 'Japonês'),
        ('ko', 'Coreano'),
        ('zh', 'Chinês'),
        ('ar', 'Árabe'),
    ], validators=[DataRequired()])

    trans_target_lang = SelectField('Idioma de Destino', choices=[
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
        ('fr', 'Francês'),
        ('de', 'Alemão'),
        ('it', 'Italiano'),
        ('pt', 'Português'),
        ('ja', 'Japonês'),
        ('ko', 'Coreano'),
        ('zh', 'Chinês'),
        ('ar', 'Árabe'),
    ], validators=[DataRequired()])

    trans_domain = SelectField('Domínio', choices=[
        ('general', 'Geral'),
        ('technical', 'Técnico'),
        ('medical', 'Médico'),
        ('legal', 'Jurídico'),
        ('marketing', 'Marketing'),
        ('literary', 'Literário'),
        ('academic', 'Acadêmico'),
        ('gaming', 'Games'),
    ], validators=[DataRequired()])

    trans_tone = SelectField('Tom', choices=[
        ('formal', 'Formal'),
        ('informal', 'Informal'),
        ('neutral', 'Neutro'),
        ('friendly', 'Amigável'),
        ('professional', 'Profissional'),
        ('creative', 'Criativo'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('traducao', 'Tradução')
    ], default='traducao', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Tradução')

class SummaryPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Summary specific fields
    sum_source_type = SelectField('Tipo de Fonte', choices=[
        ('article', 'Artigo'),
        ('book', 'Livro'),
        ('report', 'Relatório'),
        ('video', 'Vídeo'),
        ('podcast', 'Podcast'),
        ('meeting', 'Reunião'),
        ('research', 'Pesquisa'),
        ('news', 'Notícias'),
    ], validators=[DataRequired()])

    sum_length = SelectField('Comprimento do Resumo', choices=[
        ('brief', 'Breve (1-2 parágrafos)'),
        ('medium', 'Médio (3-5 parágrafos)'),
        ('detailed', 'Detalhado (1-2 páginas)'),
        ('comprehensive', 'Abrangente (múltiplas páginas)'),
    ], validators=[DataRequired()])

    sum_key_points = TextAreaField('Pontos-Chave a Incluir', validators=[DataRequired()])

    sum_format = SelectField('Formato de Saída', choices=[
        ('paragraph', 'Parágrafos'),
        ('bullet_points', 'Pontos'),
        ('numbered_list', 'Lista Numerada'),
        ('executive_summary', 'Resumo Executivo'),
        ('abstract', 'Resumo/Abstract'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('resumo', 'Resumo')
    ], default='resumo', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Resumo')

class MarketingPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Marketing specific fields
    market_campaign_type = SelectField('Tipo de Campanha', choices=[
        ('brand_awareness', 'Consciência de Marca'),
        ('product_launch', 'Lançamento de Produto'),
        ('seasonal', 'Sazonal'),
        ('promotional', 'Promocional'),
        ('content', 'Conteúdo'),
        ('social_media', 'Redes Sociais'),
        ('email', 'Email Marketing'),
    ], validators=[DataRequired()])

    market_target_audience = TextAreaField('Público-Alvo', validators=[DataRequired()])

    market_platform = SelectField('Plataforma Principal', choices=[
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('google_ads', 'Google Ads'),
        ('print', 'Impresso'),
        ('tv', 'TV'),
    ], validators=[DataRequired()])

    market_objective = TextAreaField('Objetivo da Campanha', validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('marketing', 'Marketing')
    ], default='marketing', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Marketing')

class EducationPromptForm(FlaskForm):
    project_name = StringField('Nome do Projeto', validators=[DataRequired()])
    project_description = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    project_objectives = TextAreaField('Objetivos do Projeto', validators=[DataRequired()])

    # Education specific fields
    edu_level = SelectField('Nível Educacional', choices=[
        ('elementary', 'Ensino Fundamental'),
        ('middle', 'Ensino Médio'),
        ('high_school', 'Ensino Superior'),
        ('professional', 'Profissional'),
        ('adult', 'Educação de Adultos'),
        ('specialized', 'Especializada'),
    ], validators=[DataRequired()])

    edu_subject = TextAreaField('Assunto/Matéria', validators=[DataRequired()])

    edu_format = SelectField('Formato', choices=[
        ('lesson_plan', 'Plano de Aula'),
        ('presentation', 'Apresentação'),
        ('worksheet', 'Atividade/Ficha'),
        ('quiz', 'Quiz/Teste'),
        ('video_tutorial', 'Vídeo Tutorial'),
        ('interactive', 'Interativo'),
        ('textbook', 'Livro Didático'),
    ], validators=[DataRequired()])

    edu_duration = SelectField('Duração', choices=[
        ('15min', '15 minutos'),
        ('30min', '30 minutos'),
        ('1hour', '1 hora'),
        ('2hours', '2 horas'),
        ('full_day', 'Dia inteiro'),
        ('multi_session', 'Múltiplas sessões'),
    ], validators=[DataRequired()])

    category = SelectField('Categoria', choices=[
        ('educacao', 'Educação')
    ], default='educacao', validators=[DataRequired()],
       render_kw={'readonly': True})

    submit = SubmitField('Gerar Prompt de Educação')