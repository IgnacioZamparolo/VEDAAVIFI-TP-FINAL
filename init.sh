#!/bin/bash

echo "Instalando dependencias del backend..."
cd backend
pip install -r requirements.txt
cd ..

echo "Instalando dependencias del frontend..."
cd frontend
pip install -r requirements.txt
cd ..

echo "Listo para correr el proyecto."
