import asyncio
import time
from colorama import Fore, Style, init
from textwrap import indent
from typing import Optional, Dict, Any
import sys

init(autoreset=True)

# ==============================================
# 🛠️ Custom Async Logger System
# ==============================================
class AsyncLogger:
    def __init__(self):
        self.start_time = None
        self.spinner_chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
        self.current_spinner = 0
        self.log_level_colors = {
            "INFO": Fore.CYAN,
            "SUCCESS": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "QUESTION": Fore.LIGHTMAGENTA_EX
        }

    async def _log(
        self,
        level: str,
        message: str,
        details: Optional[str] = None,
        spinner: bool = False,
        indent_level: int = 0
    ):
        color = self.log_level_colors.get(level, Fore.WHITE)
        indent = "  " * indent_level
        spinner_char = f"{self.spinner_chars[self.current_spinner]} " if spinner else ""
        
        log_line = (
            f"{Style.BRIGHT}{color}{spinner_char}[{level}] {Style.RESET_ALL}"
            f"{indent}{message}"
        )
        
        print(log_line)
        
        if details:
            details_indent = "  " * (indent_level + 1)
            print(f"{details_indent}{Fore.LIGHTBLACK_EX}{details}{Style.RESET_ALL}")
        
        if spinner:
            self.current_spinner = (self.current_spinner + 1) % len(self.spinner_chars)
            await asyncio.sleep(0.1)

    async def log_step(self, message: str, details: Optional[str] = None, emoji: str = "🚀"):
        await self._log("INFO", f"{emoji} {message}", details, spinner=True, indent_level=1)
    
    async def log_question(self, message: str, details: Optional[str] = None):
        await self._log("QUESTION", f"{message}", details, spinner=False, indent_level=1)

    async def log_success(self, message: str, details: Optional[str] = None, emoji: str = "✅"):
        await self._log("SUCCESS", f"{emoji} {message}", details, indent_level=1)

    async def log_warning(self, message: str, details: Optional[str] = None, emoji: str = "⚠️"):
        await self._log("WARNING", f"{emoji} {message}", details, indent_level=1)

    async def log_error(self, message: str, details: Optional[str] = None, emoji: str = "❌"):
        await self._log("ERROR", f"{emoji} {message}", details, indent_level=1)
        sys.exit(1)


    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        return f"[{(time.time() - self.start_time):.2f}s]" if self.start_time else ""

logger = AsyncLogger()

# ==============================================
# 📄 Main Application
# ==============================================
async def main():

    if len(sys.argv) < 2:
        await logger.log_error("Argumentos insuficientes", "Por favor, fornecer o caminho para o PDF como argumento")


    doc_path = sys.argv[1]

    model = "llama3.2"
    # model = "deepseek-r1"

    logger.start_timer()

    try:
        print(Fore.BLUE + Style.BRIGHT + r"""
  _________ .__            __    __________________  ___________
  \_   ___ \|  |__ _____ _/  |_  \______   \______ \ \_   _____/
  /    \  \/|  |  \\__  \\   __\  |     ___/|    |  \ |    __)  
  \     \___|   Y  \/ __ \|  |    |    |    |    `   \|     \   
  \______  /___|  (____  /__|    |____|   /_______  /\___  /   
          \/     \/     \/                         \/     \/      
        """ + Style.RESET_ALL)

        print(Fore.BLUE + f"""\n        ~ by @GM7AVILA\n\n""");


        # ================================
        # 🔵 STEP 1: EXTRACT PDF
        # ================================
        await logger.log_step(
            f"Iniciando extração de PDF em: {doc_path}",
        )
        print("\n")


        from langchain_community.document_loaders import UnstructuredPDFLoader
        

        try:
            loader = UnstructuredPDFLoader(doc_path)
            await logger.log_step("Carregando parser PDF...", "Usando UnstructuredPDFLoader", emoji="📄")
            print("\n")

            data = loader.load()

            if not data or len(data[0].page_content) < 100:
                print("\n")
                await logger.log_error("Conteúdo extraído inválido", "O documento pode estar corrompido ou protegido")
            
            print("\n")
            await logger.log_success(
                "PDF processado com sucesso!",
                f"Tamanho do conteúdo: {len(data[0].page_content)} caracteres\n"
            )

            
        except FileNotFoundError:
            await logger.log_error("Arquivo não encontrado", f"Caminho especificado: {doc_path}")
        except Exception as e:
            await logger.log_error("Erro na extração do PDF", f"{type(e).__name__}: {str(e)}")

        print("\n\n")

        # ================================
        # 🔵 STEP 2: CHUNKING
        # ================================
        await logger.log_step(
            "Inicializando Processo de Chunking",
            "\nConfig: RecursiveCharacterTextSplitter"
            "\nchunk_size=1200 | chunk_overlap=300"
        )

        print("\n")
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=300,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_documents(data)
            await logger.log_success(
                "Etapa de Chunking concluída com sucesso!",
                f"Total de chunks: {len(chunks)}\n"
            )
            
        except Exception as e:
            await logger.log_error("Falha no processo de chunking", f"{type(e).__name__}: {str(e)}")


        print("\n\n")

        # ================================
        # 🔵 STEP 3: VECTOR DATABASE
        # ================================
        await logger.log_step(
            "Inicializando banco de vetores",
            "Config: ChromaDB + Nomic Embeddings"
        )

        try:
            print("\n")
            await logger.log_step("Baixando modelo de embeddings...", "nomic-embed-text", emoji="📦")
            import ollama
            ollama.pull("nomic-embed-text")
            
            from langchain_community.vectorstores import Chroma
            from langchain_ollama import OllamaEmbeddings

            print("\n")
            await logger.log_step("Criando vetores...", "Processamento pode levar alguns minutos...", emoji="📦")
            
            vector_db = Chroma.from_documents(
                documents=chunks,
                embedding=OllamaEmbeddings(model="nomic-embed-text"),
                collection_name="advanced-rag-system",
                persist_directory="./vector_db"
            )
            
            print("\n")

            await logger.log_success(
                "Banco de vetores inicializado com sucesso!",
                f"Coleção: advanced-rag-system\n"
                f"Documentos armazenados: {vector_db._collection.count()}"
            )
            
        except Exception as e:
            await logger.log_error("Falha na inicialização do banco de vetores", f"{type(e).__name__}: {str(e)}")

        print("\n\n")

        # ================================
        # 🔵 STEP 4: RETRIEVAL SYSTEM
        # ================================
        await logger.log_step(
            "Configurando sistema de recuperação",
            "MultiQueryRetriever + RAG Chain",
            emoji="🔧"
        )

        try:
            from langchain.prompts import ChatPromptTemplate, PromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            from langchain_ollama import ChatOllama
            from langchain_core.runnables import RunnablePassthrough
            from langchain.retrievers.multi_query import MultiQueryRetriever

            print("\n")
            await logger.log_step("Inicializando modelo LLM...", f"Modelo: {model}", emoji="🔧")
            llm = ChatOllama(model=model)

            print("\n")
            await logger.log_step("Configurando MultiQueryRetriever...", "Gerando variações de queries", emoji="🔧")
            retriever = MultiQueryRetriever.from_llm(
                vector_db.as_retriever(),
                llm,
                prompt=PromptTemplate(
                    input_variables=["question"],
                    template="""Gere 5 variações da pergunta para busca contextualizada:
                    Pergunta original: {question}"""
                )
            )

            print("\n")
            await logger.log_step("Construindo pipeline RAG...", "Template customizado", emoji="🔧")
            prompt_template = ChatPromptTemplate.from_template(
                """Responda com base exclusivamente no contexto:
                {context}
                Pergunta: {question}
                """
            )

            print("\n")

            rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt_template
                | llm
                | StrOutputParser()
            )

            await logger.log_success(
                "Sistema RAG construído com sucesso!",
                f"\nModelo: {model}"
                f"\nTécnicas usadas: Multi-query expansion, RAG chain",
            )

            print("\n")

            # ================================
            # 🔵 STEP 5: USER INPUT FOR QUESTIONS
            # ================================
            while True:
                print("\n\n")
                print(Fore.MAGENTA + "_____________________\n")
                print(Fore.CYAN + "Digite sua pergunta (ou 'sair' para encerrar): ", end="")
                user_question = input()

                if user_question.lower() == 'sair':
                    print(Fore.YELLOW + "Encerrando o sistema...")
                    break
                print("\n")
                await logger.log_question(user_question, "\nPensando...")
                response = await rag_chain.ainvoke(user_question)
                print(f"\n{Fore.LIGHTMAGENTA_EX}🤖 Resposta: {response}\n")


        except Exception as e:
            await logger.log_error("Falha na configuração do RAG", f"{type(e).__name__}: {str(e)}")

    finally:
        print(f"\n\n{Fore.MAGENTA}⏱️  Processo completo {logger.get_elapsed_time()}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
