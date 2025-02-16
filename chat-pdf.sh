#!/bin/bash

# Paths
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_EXEC="$VENV_DIR/bin/python"
PYTHON_BENCHMARK_SCRIPT="$SCRIPT_DIR/benchmark-pdf.py"
PYTHON_SCRIPT="$SCRIPT_DIR/pdf-rag-bash.py"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Function to display help
usage() {
  echo "Usage: $0 <pdf_file> [--benchmark] [--manual]"
  echo ""
  echo "Arguments:"
  echo "  <pdf_file>     Path to the PDF file to be processed."
  echo "  <pdf_file> --benchmark    Runs the benchmark instead of normal processing."
  echo "  <pdf_file> --benchmark [model]    Runs the benchmark with a specific Ollama model."
  echo "  --manual       Displays the detailed manual."
  echo "  --help         Displays this help message."
  exit 0
}

# Function to display the manual
manual() {
  cat <<EOF

CHAT PDF - Manual

NAME
    $0 - PDF processing and benchmarking utility

SYNOPSIS
    $0 <pdf_file>
    $0 <pdf_file> --benchmark [model]
    $0 --manual
    $0 --help

DESCRIPTION
    Processes PDF files using Python-based text analysis. Supports two modes:
    normal processing and performance benchmarking. Automatically manages
    Python virtual environments and dependencies.

PREREQUISITES
    - POSIX-compliant system (Linux/BSD/macOS)
    - Python 3.7 or newer
    - Bash 4.2 or newer
    - Ollama installed and running with desired models downloaded

OPTIONS
    <pdf_file>        PDF document to process (required for normal operation)
    --benchmark       Execute performance benchmarking mode
                      Optional: Specify model name after --benchmark flag
    --manual          Display this manual page
    --help            Show brief usage information

BEHAVIOR
    The script performs these actions in order:
    1. Creates Python virtual environment in ./venv if missing
    2. Installs packages from requirements.txt (first run only)
    3. Executes either:
       - chat-pdf.py for normal processing
       - benchmark-pdf.py for performance testing with specified model
         (default: llama3.2 if no model specified)

EXAMPLES
    Process a document:
    $0 document.pdf

    Run performance benchmark with default model (llama3.2):
    $0 document.pdf --benchmark

    Run performance benchmark with specific LLM model:
    $0 document.pdf --benchmark deepseek-r1

    Show manual:
    $0 --manual

ENVIRONMENT
    Requires write permissions in the script directory for virtual environment
    creation. Executes in the current shell context - does not modify
    user's Python environment.

FILES
    $SCRIPT_DIR/venv/        Python virtual environment
    $SCRIPT_DIR/requirements.txt  Dependency specification
    $SCRIPT_DIR/pdf-rag-bash.py   Main processing script
    $SCRIPT_DIR/benchmark-pdf.py  Benchmarking script

DIAGNOSTICS
    Exit status 0 on success, 1 if PDF file is missing or invalid, 2 for
    dependency errors, 3 for invalid model specification.

SEE ALSO
    Project repository: <github-url> (installation instructions)
    Python venv documentation: https://docs.python.org/3/library/venv.html
    Ollama documentation: https://ollama.ai/

EOF
  exit 0
}

# Check arguments
if [[ "$#" -lt 1 ]] || [[ "$#" -gt 3 ]]; then
  usage
fi

if [ "$1" == "--help" ]; then
  usage
fi

if [ "$1" == "--manual" ]; then
  manual
fi

PDF_FILE="$1"
BENCHMARK=false
MODEL="llama3.2"  # default model

# Parse remaining arguments
shift
while [[ $# -gt 0 ]]; do
  case $1 in
    --benchmark)
      BENCHMARK=true
      # Check if next argument is a model
      if [[ $# -gt 1 ]] && [[ $2 != --* ]]; then
        MODEL="$2"
        shift
      fi
      ;;
    *)
      usage
      ;;
  esac
  shift
done

if [ "$#" -eq 2 ]; then
  if [ "$2" == "--benchmark" ]; then
    BENCHMARK=true
  else
    usage
  fi
fi


if [ ! -f "$PDF_FILE" ]; then
  echo "Error: The PDF file '$PDF_FILE' does not exist."
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
  
  echo "Activating virtual environment and installing dependencies..."
  source "$VENV_DIR/bin/activate"

  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
  else
    echo "Error: requirements.txt file not found!"
    exit 1
  fi
fi

# Run 
if [ "$BENCHMARK" = true ]; then
  echo "Running benchmark with PDF: $PDF_FILE and Model: $MODEL"
  "$PYTHON_EXEC" "$PYTHON_BENCHMARK_SCRIPT" "$PDF_FILE" "$MODEL"
else
  echo "Running normal processing with PDF: $PDF_FILE"
  "$PYTHON_EXEC" "$PYTHON_SCRIPT" "$PDF_FILE"
fi
