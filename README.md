# CHAT PDF

Utilize modelos Ollama para resumir PDFs e realizar consultas contextuais no terminal.

## Requisitos

- Python 3
- Ollama

## Instalação por `install.sh`

Basta executar `install.sh` e o ambiente será preparado.

## Instalação Manual

O script `chat-pdf.sh` criará automaticamente um ambiente virtual (venv) caso ele não exista. Certifique-se de que `<span>requirements.txt` esteja no diretório do script.

### Permissões de Execução

Caso o script não tenha permissões de execução, conceda-as com o seguinte comando:

chmod +x chat-pdf.sh

Isso permitirá que o script seja executado diretamente como um comando no terminal.

### Criando Link Simbólico (Linux)

Para facilitar a execução do script, pode-se criar um link simbólico para acessá-lo de qualquer lugar no terminal:

```
ln -s /chat-pdf.sh /usr/local/bin/chat-pdf
```

Agora, basta executar:

```
chat-pdf documento.pdf
```

## Uso

```
./chat-pdf.sh <arquivo.pdf> [--benchmark [modelo]]
```

### Argumentos:

- `<span> <arquivo.pdf></span>`: Caminho para o arquivo PDF a ser processado.
- `<span> --benchmark [modelo]</span>` (opcional): Executa o script em modo benchmark. Pode-se especificar um modelo (padrão: `<span>llama3.2</span>`).
- `<span>--help</span>`: Exibe a mensagem de ajuda.
- `<span>--manual</span>`: Exibe o manual detalhado.

### Exemplos de uso

Executar o processamento normal:

```
./chat-pdf.sh documento.pdf
```

Executar em modo benchmark com modelo padrão:

```
./chat-pdf.sh documento.pdf --benchmark
```

Executar em modo benchmark com modelo específico:

```
./chat-pdf.sh documento.pdf --benchmark gemini-pro
```

## Funcionamento

1. Verifica a existência do arquivo PDF.
2. Configura o ambiente virtual e instala dependências se necessário.
3. Executa o script apropriado:
   - `<span>pdf-rag-bash.py</span>` para processamento normal.
   - `<span>benchmark-pdf.py</span>` para benchmarking.

## Licença

Este projeto está sob a licença MIT.
