# CHAT PDF

Utilize modelos Ollama para resumir PDFs e realizar consultas contextuais no terminal.

<br>
<div style="display: flex; gap: 10px;">
  <img src="https://github.com/user-attachments/assets/cac49f47-e419-4894-bfaa-620ae9d6ad54" style="width: 48%;">
  <img src="https://github.com/user-attachments/assets/d6f18664-b1e2-4bf6-bc68-3d80e75c7c39" style="width: 48%;">
</div>
<br>

## **Sumário**

1. [Requisitos](#requisitos)
2. Instalação
   - [Instalação por `install.sh`](#instalação-por-installsh)
   - [Instalação Manual](#instalação-manual)
3. [Uso](#uso)
4. [Funcionamento](#funcionamento)
5. [Licença](#licença)


## **Requisitos**

- Python 3
- Ollama

## Instalação por `install.sh`

Basta executar `install.sh` e o ambiente será preparado.

## Instalação Manual

O script `chat-pdf.sh` criará automaticamente um ambiente virtual (venv) caso ele não exista. Certifique-se de que `requirements.txt` esteja no diretório do script.

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

- `<arquivo.pdf>`: Caminho para o arquivo PDF a ser processado.
- `--benchmark [modelo]` (opcional): Executa o script em modo benchmark. Pode-se especificar um modelo (padrão: `llama3.2`).
- `--help`: Exibe a mensagem de ajuda.
- `--manual`: Exibe o manual detalhado.

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
./chat-pdf.sh documento.pdf --benchmark deepseek-r1
```


## Funcionamento

1. Verifica a existência do arquivo PDF.
2. Configura o ambiente virtual e instala dependências se necessário.
3. Executa o script apropriado:
   - `pdf-rag-bash.py` para processamento normal.
   - `benchmark-pdf.py` para benchmarking.

## Licença

Este projeto está sob a licença MIT.
