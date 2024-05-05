# ProyectoFinal_Python_DB_Flask
Proyecto Final usando Flask y MySQL 

1. Para iniciar el prpyecto es necesario crear una base de datos con MySQL con el siguiente código:

        CREATE DATABASE IF NOT EXISTS proyectoFinalDB;

        USE proyectoFinalDB;

        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );

        ALTER TABLE usuarios MODIFY COLUMN password VARCHAR(255) NOT NULL;
        select * from usuarios;

        CREATE TABLE mensajes_chat (
            id INT AUTO_INCREMENT PRIMARY KEY,
            remitente VARCHAR(100),
            destinatario VARCHAR(100),
            mensaje TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        select * from mensajes_chat;

2. Una vez creada se procede a crear el entorno virtual con:
    python -m venv venv

3. Se activa el entorno virtual con:
    source venv/Scripts/activate

4. Se instalan la dependecias usadas y guardadas en el documentos requirements.txt con:
    pip install -r requirements.txt

5. Se inicia el proyecto con:
    python app.js

Muchas gracias!!!