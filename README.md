# Prompt Master 🤖

> Gerador e formatador de prompts para agentes de IA - Uma ferramenta completa para criar prompts estruturados e profissionais

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0+-red)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📋 Manifesto

**Prompt Master** é uma aplicação web desenvolvida para revolucionar a forma como criamos e gerenciamos prompts para agentes de IA. Nossa missão é fornecer uma ferramenta intuitiva, poderosa e acessível que permite aos usuários criar prompts estruturados, profissionais e otimizados para diferentes tipos de conteúdo e aplicações.

### 🎯 Nossa Visão
- **Inovação**: Interfaces modernas e tecnologia de ponta
- **Qualidade**: Prompts estruturados e profissionais
- **Acessibilidade**: Ferramenta intuitiva para todos os usuários

## 🚀 Funcionalidades

### 📝 Criação de Prompts
- **Texto**: Prompts de texto com configurações avançadas (linguagem, temperatura, tom, persona)
- **Imagem**: Prompts detalhados para geração de imagens (estilo, material, iluminação, cores)
- **Áudio**: Configurações para prompts de áudio
- **Código**: Prompts especializados para desenvolvimento
- **Vídeo**: Configurações completas para conteúdo audiovisual
- **Apresentações**: Estrutura para slides e apresentações
- **Infográficos**: Visualizações de dados e informações
- **Animações**: Configurações para animações digitais
- **Websites**: Prompts para desenvolvimento web
- **Dados**: Análise e visualização de dados
- **Tradução**: Configurações para tradução de textos
- **Resumos**: Estruturação de resumos inteligentes
- **Marketing**: Campanhas e estratégias de marketing
- **Educação**: Conteúdo educacional estruturado

### 🛠️ Gerenciamento
- **CRUD Completo**: Criar, visualizar, editar e excluir prompts
- **Exportação**: Exportar prompts em formato Markdown
- **Organização**: Categorização e busca de prompts
- **Banco de Dados**: Persistência com SQLite

## 🏗️ Arquitetura

### Tecnologias Principais
- **Backend**: Flask 3.0.3, SQLAlchemy, WTForms
- **Frontend**: Bootstrap 5, Tailwind CSS, JavaScript
- **Banco de Dados**: SQLite
- **Templates**: Jinja2

### Estrutura do Projeto
```
prompt-master/
├── app.py                 # Aplicação principal Flask
├── forms.py              # Definições dos formulários WTForms
├── requirements.txt      # Dependências Python
├── promptmaster.db       # Banco de dados SQLite
├── static/               # Arquivos estáticos
│   ├── css/
│   └── js/
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── criar_*.html
└── migrations/           # Migrações do banco de dados
```

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/lscheffel/Prompt-Master.git
   cd Prompt-Master
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 🎨 Interface

A aplicação possui uma interface moderna e responsiva com:

- **Design System**: Bootstrap 5 com temas personalizados
- **Glassmorphism**: Efeitos visuais modernos
- **Responsividade**: Perfeito em desktop, tablet e mobile
- **Acessibilidade**: Suporte completo a leitores de tela
- **Interatividade**: Elementos dinâmicos e animações

## 📊 Uso

### Criando um Prompt de Texto
1. Acesse "Criar Texto" no menu principal
2. Preencha a descrição e objetivos do projeto
3. Configure os parâmetros (linguagem, temperatura, tom, etc.)
4. Clique em "Gerar Prompt"

### Gerenciando Prompts
1. Vá para a seção "Prompts" para ver todos os prompts criados
2. Use as opções de editar, visualizar ou excluir
3. Exporte prompts importantes em formato Markdown

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Tipos de Contribuição
- 🐛 **Bug fixes**
- ✨ **Novas funcionalidades**
- 📚 **Documentação**
- 🎨 **UI/UX improvements**
- 🧪 **Testes**

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- **Flask**: Framework web incrível
- **Bootstrap**: Framework CSS poderoso
- **SQLAlchemy**: ORM excepcional
- **Comunidade Open Source**: Por tornar tudo isso possível

## 📞 Contato

- **Autor**: Leandro Scheffel
- **GitHub**: [@lscheffel](https://github.com/lscheffel)
- **Projeto**: [Prompt Master](https://github.com/lscheffel/Prompt-Master)

---

<div align="center">
  <p><strong>Feito com ❤️ pela comunidade open source</strong></p>
  <p>
    <a href="#prompt-master-">Voltar ao topo</a> •
    <a href="https://github.com/lscheffel/Prompt-Master/issues">Reportar Bug</a> •
    <a href="https://github.com/lscheffel/Prompt-Master/pulls">Contribuir</a>
  </p>
</div>