// Configuração de logging para debug
const logger = {
  info: (msg) => console.log(`[INFO] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`)
};

// Função principal de inicialização
function init() {
  try {
    logger.info('Inicializando aplicação...');
    const content = document.getElementById('content');
    if (!content) {
      throw new Error('Elemento #content não encontrado');
    }
    content.textContent = 'Projeto inicial carregado com sucesso!';
    logger.info('Conteúdo atualizado com sucesso');
  } catch (error) {
    logger.error(`Falha na inicialização: ${error.message}`);
  }
}

// Garante que o DOM esteja carregado antes de executar
document.addEventListener('DOMContentLoaded', () => {
  logger.info('DOM carregado');
  init();
});

// Exporta função para testes
export { init };