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

       stage('Iniciar servicio') {
        steps {
            script {
                def serviceName = 'prueba_fastapi_main'
                def servicePath = "/etc/systemd/system/${serviceName}.service"
                def workingDir = "${env.WORKSPACE}"
                def gunicornPath = "${env.WORKSPACE}/.venv/bin/gunicorn"

                sh """
                if [ ! -f ${servicePath} ]; then
                    echo "Creando archivo de servicio systemd para ${serviceName}..."

                    echo "[Unit]" > ${serviceName}.service
                    echo "Description=Gunicorn para proyecto FastAPI (${serviceName})" >> ${serviceName}.service
                    echo "After=network.target" >> ${serviceName}.service
                    echo "" >> ${serviceName}.service
                    echo "[Service]" >> ${serviceName}.service
                    echo "User=root" >> ${serviceName}.service
                    echo "Group=root" >> ${serviceName}.service
                    echo "WorkingDirectory=${workingDir}" >> ${serviceName}.service
                    echo "ExecStart=${gunicornPath} --workers 3 --bind 0.0.0.0:5000 main:app" >> ${serviceName}.service
                    echo "EnvironmentFile=${workingDir}/.env" >> ${serviceName}.service
                    echo "Restart=always" >> ${serviceName}.service
                    echo "" >> ${serviceName}.service
                    echo "[Install]" >> ${serviceName}.service
                    echo "WantedBy=multi-user.target" >> ${serviceName}.service

                    sudo mv ${serviceName}.service ${servicePath}
                    sudo systemctl daemon-reload
                    sudo systemctl enable ${serviceName}
                else
                    echo "El archivo ${servicePath} ya existe. Usando configuración existente."
                fi

                sudo systemctl restart ${serviceName}
                sleep 3

                if systemctl is-active --quiet ${serviceName}; then
                    echo "✅ Servicio ${serviceName} iniciado correctamente."
                else
                    echo "❌ Error al iniciar el servicio ${serviceName}"
                    journalctl -u ${serviceName} --no-pager -n 50
                    exit 1
                fi
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
