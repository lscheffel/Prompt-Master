// src/main.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript carregado.');
});

function downloadMarkdown() {
    try {
        const markdownElement = document.getElementById('prompt-markdown');
        const markdownText = markdownElement.textContent;
        const blob = new Blob([markdownText], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'prompt.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log('Markdown baixado com sucesso.');
    } catch (err) {
        console.error('Erro ao baixar Markdown:', err);
        alert('Erro ao baixar o prompt.');
    }
}