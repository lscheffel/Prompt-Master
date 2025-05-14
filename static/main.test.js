// Testes para main.js
import { init } from '../src/main.js';

describe('Testes da função init', () => {
  beforeEach(() => {
    // Mock do DOM
    document.body.innerHTML = '<section id="content"></section>';
  });

  test('Deve atualizar o conteúdo corretamente', () => {
    init();
    const content = document.getElementById('content');
    expect(content.textContent).toBe('Projeto inicial carregado com sucesso!');
  });

  test('Deve lançar erro se elemento não for encontrado', () => {
    document.body.innerHTML = '';
    console.error = jest.fn();
    init();
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Elemento #content não encontrado'));
  });
});