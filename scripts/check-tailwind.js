// scripts/check-tailwind.js
const fs = require('fs');
const path = require('path');

console.log('Verificando configuração do Tailwind...');

const stylePath = './src/style.css';
const tailwindConfigPath = './tailwind.config.js';

if (!fs.existsSync(stylePath)) {
  console.error('Erro: src/style.css não encontrado.');
  process.exit(1);
}

if (!fs.existsSync(tailwindConfigPath)) {
  console.error('Erro: tailwind.config.js não encontrado.');
  process.exit(1);
}

const styleContent = fs.readFileSync(stylePath, 'utf8');
if (!styleContent.includes('@tailwind base')) {
  console.error('Erro: src/style.css não contém diretivas do Tailwind.');
  process.exit(1);
}

const configContent = fs.readFileSync(tailwindConfigPath, 'utf8');
if (!configContent.includes('content')) {
  console.error('Erro: tailwind.config.js não contém configuração de content.');
  process.exit(1);
}

console.log('Configuração do Tailwind OK.');