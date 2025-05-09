pipeline {
    agent any
    environment {
        VENV_PATH = './.venv'
        REQUIREMENTS = 'requirements.txt'
    }
    stages {
        stage('Clonar repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/gobiernodigitalmonterrey/gdmty-gracias-ma-backend.git'
            }
        }

        stage('Preparar entorno') {
            steps {
                script {
                    // verificamos la version del piton
                    sh 'python3 --version'
                    // Crear el entorno virtual
                    sh 'python3 -m venv ${VENV_PATH}'
                    // Actualizar pip
                    sh './.venv/bin/pip install --upgrade pip'
                    // Limpiar caché de pip
                    sh './.venv/bin/pip cache purge'
                    // Instalar dependencias
                    sh './.venv/bin/pip install --no-cache-dir -r ${REQUIREMENTS}'
                    // Instalar python-dotenv
                    sh './.venv/bin/pip install python-dotenv'
                }
            }
        }

        stage('Configurar archivo .env') {
            steps {
                script {
                    // Copiar el archivo .env al contenedor
                    sh 'cp ${WORKSPACE}/.env .env-file'
                }
            }
        }

        stage('Crear script de servicio') {
            steps {
                script {
                    // Crear directorio para logs
                    sh 'mkdir -p ${WORKSPACE}/logs'

                    // Crear script de servicio persistente
                    writeFile file: "${WORKSPACE}/run_service.sh", text: """#!/bin/bash
# Script para ejecutar la aplicación FastAPI como un servicio persistente
cd ${WORKSPACE}

# Log de inicio
echo "Iniciando servicio FastAPI en \$(date)" >> ${WORKSPACE}/logs/service.log

# Establecer variables de entorno desde .env
set -a
[ -f ${WORKSPACE}/.env ] && . ${WORKSPACE}/.env
set +a

# Detener instancias previas
PID_FILE=${WORKSPACE}/app.pid
if [ -f \$PID_FILE ]; then
    OLD_PID=\$(cat \$PID_FILE)
    if ps -p \$OLD_PID > /dev/null; then
        echo "Deteniendo proceso anterior: \$OLD_PID" >> ${WORKSPACE}/logs/service.log
        kill \$OLD_PID || true
        sleep 2
    fi
fi

# Iniciar la aplicación con nohup para que persista
export PYTHONPATH=${WORKSPACE}
nohup ${WORKSPACE}/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 5000 --log-level debug > ${WORKSPACE}/logs/app.log 2>&1 &

# Guardar el PID para futura referencia
echo \$! > \$PID_FILE
echo "Servicio iniciado con PID: \$(cat \$PID_FILE) en \$(date)" >> ${WORKSPACE}/logs/service.log

# Verificar que el proceso esté realmente corriendo después de un breve período
sleep 5
if ps -p \$(cat \$PID_FILE) > /dev/null; then
    echo "Servicio verificado y en ejecución" >> ${WORKSPACE}/logs/service.log
    exit 0
else
    echo "ERROR: El servicio no pudo iniciarse correctamente" >> ${WORKSPACE}/logs/service.log
    cat ${WORKSPACE}/logs/app.log >> ${WORKSPACE}/logs/service.log
    exit 1
fi
"""

                    // Hacer ejecutable el script
                    sh "chmod +x ${WORKSPACE}/run_service.sh"
                }
            }
        }

        stage('Iniciar servicio') {
            steps {
                script {
                    // Ejecutar el script de servicio
                    sh "${WORKSPACE}/run_service.sh"

                    // Verificar que el servicio esté corriendo
                    sh """
                    sleep 3
                    if [ -f ${WORKSPACE}/app.pid ] && ps -p \$(cat ${WORKSPACE}/app.pid) > /dev/null; then
                        echo "Servicio iniciado correctamente con PID: \$(cat ${WORKSPACE}/app.pid)"
                    else
                        echo "Error al iniciar el servicio"
                        cat ${WORKSPACE}/logs/app.log
                        exit 1
                    fi
                    """

                    // Verificar logs para diagnóstico
                    sh """
                    echo "=== LOGS DE LA APLICACIÓN ==="
                    cat ${WORKSPACE}/logs/app.log || echo "No hay logs de la aplicación"

                    echo "=== LOGS DEL SERVICIO ==="
                    cat ${WORKSPACE}/logs/service.log || echo "No hay logs del servicio"
                    """
                }
            }
        }

        stage('Verificar API') {
            steps {
                script {
                    // Intentar hacer una solicitud a la API
                    sh """
                    sleep 2
                    curl -s -I http://localhost:5000/ || echo "No se pudo conectar a la API"
                    """
                }
            }
        }
    }

    post {
        always {
            // Guardar los logs como artefactos
            archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true
        }
    }
}
