import asyncio
import argparse
import time
from colorama import Fore, Style, init
from textwrap import indent
import sys

init(autoreset=True)

class Benchmark:
    def __init__(self):
        self.timers = {}
        self.metrics = {}
    
    def start_phase(self, phase: str):
        self.timers[phase] = time.time()
    
    def end_phase(self, phase: str):
        if phase in self.timers:
            self.metrics[phase] = time.time() - self.timers[phase]
    
    def add_metric(self, name: str, value: float):
        self.metrics[name] = value
    
    def get_report(self, model) -> str:
        report = "\n📊 Relatório Detalhado de Performance"
        report += (f"\nModelo: {model}\n")
        report += "═" * 50 + "\n"
        
        # Tempos das fases principais
        report += f"{Fore.CYAN}▶ Fases de Processamento{Style.RESET_ALL}\n"
        main_phases = [
            ("Extração do PDF", "Extração e análise do documento"),
            ("Chunking", "Segmentação do texto em chunks"),
            ("Vetorização", "Conversão para embeddings vetoriais"),
            ("Configuração RAG", "Inicialização do sistema de recuperação"),
            ("Processamento", "Geração da resposta completa")
        ]
        
        total = 0
        for phase in main_phases:
            if phase[0] in self.metrics:
                duration = self.metrics[phase[0]]
                total += duration
                report += f"  {phase[1]}: {Fore.YELLOW}{duration:.2f}s{Style.RESET_ALL}\n"
        
        # Métricas adicionais
        report += f"\n{Fore.CYAN}◈ Métricas Chave{Style.RESET_ALL}\n"
        report += f"  Total de chunks: {self.metrics.get('total_chunks', 0)}\n"
        report += f"  Documentos vetoriais: {self.metrics.get('vector_docs', 0)}\n"
        report += f"  Tamanho do contexto: {self.metrics.get('context_size', 0):,} caracteres\n"
        
        # Resumo final
        report += "\n" + "═" * 50 + "\n"
        report += f"{Fore.GREEN}✅ Tempo Total: {total:.2f}s{Style.RESET_ALL}\n"
        return report

benchmark = Benchmark()

async def main():
    print(Fore.BLUE + Style.BRIGHT + r"""
  _________ .__            __    __________________  ___________
  \_   ___ \|  |__ _____ _/  |_  \______   \______ \ \_   _____/
  /    \  \/|  |  \\__  \\   __\  |     ___/|    |  \ |    __)  
  \     \___|   Y  \/ __ \|  |    |    |    |    `   \|     \   
  \______  /___|  (____  /__|    |____|   /_______  /\___  /   
          \/     \/     \/                         \/     \/    
        """ + Style.RESET_ALL)
    print(Fore.BLUE + f"""\n      ~ by @GM7AVILA\n\n""");

    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Benchmark PDF Processing')
    parser.add_argument('pdf_file', type=str, help='Path to the PDF file')
    parser.add_argument('model', type=str, nargs='?', default="llama3.2",
                      help='Ollama model to use (default: llama3.2)')
    args = parser.parse_args()

    doc_path = "./data/linearidade-dos-parametros-regressao-linear.pdf"

    #######################################################################
    #                       MODELOS OLLAMA LLM                            #
    #                      run "ollama pull (model)"                      #
    #######################################################################
    # model = "llama3.2"
    # model = "deepseek-r1"
    # model = "deepscaler"
    model = args.model

    QUESTION = """Faça um resumo detalhado do documento em questão com pelo menos 10 linhas e no maximo 12 linhas."""

    try:
        # Início do processamento
        print(Fore.BLUE + "\n🚀 Iniciando Pipeline...\n")
        print(Fore.BLUE + "\n- Modelo: " + model + "\n")

        # ================================
        # 🔵 Fase 1: Extração do Documento
        # ================================
        benchmark.start_phase("Extração do PDF")
        from langchain_community.document_loaders import UnstructuredPDFLoader
        loader = UnstructuredPDFLoader(doc_path)
        data = loader.load()
        benchmark.end_phase("Extração do PDF")
        
        benchmark.add_metric("context_size", len(data[0].page_content))
        print(Fore.GREEN + f"\n✅ [SUCESSO] Documento carregado ({len(data[0].page_content):,} caracteres) | (1/4) %")

        # ================================
        # 🔵 Fase 2: Pré-processamento
        # ================================
        benchmark.start_phase("Chunking")
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=300
        )
        chunks = text_splitter.split_documents(data)
        benchmark.end_phase("Chunking")
        
        benchmark.add_metric("total_chunks", len(chunks))
        print(Fore.GREEN + f"✅ [SUCESSO] Texto segmentado em {len(chunks)} chunks | (2/4) %")

        # ================================
        # 🔵 Fase 3: Vetorização
        # ================================
        benchmark.start_phase("Vetorização")
        import ollama
        from langchain_community.vectorstores import Chroma
        from langchain_ollama import OllamaEmbeddings
        
        ollama.pull("nomic-embed-text")
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=OllamaEmbeddings(model="nomic-embed-text")
        )
        benchmark.end_phase("Vetorização")
        
        benchmark.add_metric("vector_docs", vector_db._collection.count())
        print(Fore.GREEN + f"✅ [SUCESSO] Vetores armazenados ({vector_db._collection.count()} documentos) | (3/4) %")

        # ================================
        # 🔵 Fase 4: Configuração RAG
        # ================================
        benchmark.start_phase("Configuração RAG")
        from langchain.prompts import ChatPromptTemplate
        from langchain_ollama import ChatOllama
        from langchain.retrievers.multi_query import MultiQueryRetriever
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        
        llm = ChatOllama(model=model)
        retriever = MultiQueryRetriever.from_llm(
            vector_db.as_retriever(),
            llm
        )
        
        prompt_template = ChatPromptTemplate.from_template(
            """Analise o contexto e responda com detalhes:
            {context}
            
            Questão: {question}"""
        )
        
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
        )
        benchmark.end_phase("Configuração RAG")
        print(Fore.GREEN + "✅ [SUCESSO] Sistema RAG configurado | (4/4) %")

        # ================================
        # 🔵 Fase 5: Processamento da Questão
        # ================================
        benchmark.start_phase("Processamento")
        print(Fore.YELLOW + "\n🔍 [TESTE] Espera-se que o modelo responda:")
        print(Fore.YELLOW + f"\n➤ {QUESTION}\n")
        print(Fore.MAGENTA + f"\n⚙️ [{model}] Processando ...\n")
        
        start_time = time.time()
        response = await rag_chain.ainvoke(QUESTION)
        benchmark.end_phase("Processamento")
        
        print(Fore.YELLOW + "\n\n🔍 [RESPOSTA] : ")
        print(Fore.MAGENTA + indent(response, "  "))
        print(f"\n\n{Fore.YELLOW}⏱ Tempo de Resposta: {time.time() - start_time:.2f}s\n\n\n")

        # Relatório final
        print(benchmark.get_report(model=model))

    except Exception as e:
        print(Fore.RED + f"\n❌ Erro crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())