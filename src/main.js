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

document.getElementById('theme-toggle').addEventListener('click', () => {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');

    if (body.classList.contains('bg-gray-900')) {
        body.classList.remove('bg-gray-900', 'text-gray-100');
        body.classList.add('bg-white', 'text-gray-900');
        themeIcon.classList.remove('bi-lightbulb-fill');
        themeIcon.classList.add('bi-lightbulb');
    } else {
        body.classList.remove('bg-white', 'text-gray-900');
        body.classList.add('bg-gray-900', 'text-gray-100');
        themeIcon.classList.remove('bi-lightbulb');
        themeIcon.classList.add('bi-lightbulb-fill');
    }
});