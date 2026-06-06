#!/bin/bash


ROOT_DIR=$(pwd)

if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "[ERROR] No se encontraron las carpetas 'backend' y/or 'frontend' en el directorio actual."
    echo "Por favor, ejecutá este script desde la raíz del proyecto estructurado."
    exit 1
fi

echo ""
echo "[1/2] Configurando el entorno del BACKEND..."
cd "$ROOT_DIR/backend"


if [ -d "$ROOT_DIR/.env" ]; then
    VENV_PATH="$ROOT_DIR/.env"
elif [ -d "$ROOT_DIR/venv" ]; then
    VENV_PATH="$ROOT_DIR/venv"
else
    
    if [ ! -d ".venv" ]; then
        echo "Creando entorno virtual (.venv) para el Backend..."
        python3 -m venv .venv
    fi
    VENV_PATH="$PWD/.venv"
fi

echo "Usando entorno virtual: $VENV_PATH"
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "¡Backend configurado exitosamente!"


echo ""
echo "[2/2] Configurando el entorno del FRONTEND..."
cd "$ROOT_DIR/frontend"


if [ -d "$ROOT_DIR/.env" ]; then
    VENV_PATH="$ROOT_DIR/.env"
elif [ -d "$ROOT_DIR/venv" ]; then
    VENV_PATH="$ROOT_DIR/venv"
else
    
    if [ ! -d ".venv" ]; then
        echo "Creando entorno virtual (.venv) para el Frontend..."
        python3 -m venv .venv
    fi
    VENV_PATH="$PWD/.venv"
fi

echo "Usando entorno virtual: $VENV_PATH"
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "¡Frontend configurado exitosamente!"


echo ""
echo "======================================================================"
echo "  ¡Configuración completada con éxito! Todo listo para trabajar.     "
echo "======================================================================"
echo ""
echo "Para ejecutar el proyecto, abrí dos terminales separadas y ejecutá:"
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo "  python app/app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  source .venv/bin/activate"
echo "  python run.py"
echo "======================================================================"