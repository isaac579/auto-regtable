import mysql.connector
import secrets
import string
from dotenv import load_dotenv
import os
import subprocess

# Cargar variables del archivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

# Generar contraseña aleatoria segura
def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

# Parámetros
nuevo_valor = generar_password()
id_objetivo = 656  # Cambia este ID según el registro que quieras actualizar

try:
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Obtener username del ID especificado
    cursor.execute("SELECT username FROM radcheck WHERE id = %s", (id_objetivo,))
    resultado = cursor.fetchone()
    if not resultado:
        print(f"No se encontró el registro con ID = {id_objetivo}")
        exit()

    name = resultado[0]

    # Actualizar el valor del registro
    cursor.execute("UPDATE radcheck SET value = %s WHERE id = %s", (nuevo_valor, id_objetivo))
    conn.commit()

    # Construir cuerpo del correo
    subject = "Datos de acceso a la red de ENI INVITADOS"
    body = f"""\
    Se ha actualizado el acceso para invitados:

    Usuario : {name}
    Password : {nuevo_valor}
    """

    # Enviar correo usando el comando `mail`
    subprocess.run(
        ["mail", "-s", subject, "-a", f"From: {EMAIL_FROM}", EMAIL_TO],
        input=body.encode(),
        check=True
    )

    print("Correo enviado con éxito.")

except Exception as e:
    print("Error:", str(e))

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()

#ESTAS LINEAS DE CODIGO SE AGREGARAN EN UN ARCHIVO .env para que las tome
#DB_HOST= 192.168.1.1(PON LA IP DE TU DB)
#DB_USER= USUARIO
#DB_PASSWORD= PASSWORD(PON TU CONTRASENA)
#DB_NAME= NOMBRE DB
#EMAIL_FROM= EMAIL DE DESTINO mail1@mail.com
#EMAIL_TO=email@mail.com

