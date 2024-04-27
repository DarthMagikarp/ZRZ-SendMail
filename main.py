import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from send_mail import MailSender
from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def test_functions(self):

    print("Request: "+str(request.json))
    plaintext = ""

    asunto = request.json['asunto']
    sender = "no-responder"
    tarjet = request.json['tarjet']     #pa quien es el correo
    paciente = request.json['paciente'] #si es paciente o no
    
    #try:
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()
    
    sql = '''
        SELECT
            CONCAT(ua.nombre, ' ', ua.apellido) AS nombre_alumno,
            CONCAT(up.nombre, ' ', up.apellido) AS nombre_profesional,
            e.especialidad AS especialidad_profesional,
            ua.telefono AS telefono_estudiante,
            ua.email AS email_estudiante,
            c.fecha,
            c.hora,
            c.estado,
            c.campus AS campus,
            c.fechamod
        FROM
            citas c
        JOIN
            usuarios up ON c.profesional_id = up.id
        JOIN
            usuarios ua ON c.alumno_id = ua.id
        JOIN
            especialidad_user eu ON up.id = eu.usuario_id
        JOIN
            especialidades e ON eu.id_especialidad = e.id
        ORDER BY
            c.fechamod DESC
        LIMIT 1;
    '''
    cursor.execute(sql)
    resp = cursor.fetchone()
    
    estudiante = str(resp[0])
    colaborador = str(resp[1])
    dia = str(resp[5])
    hora = str(resp[6])
    sede = str(resp[8])
    
    if paciente:
        plaintext = "Estimado estudiante, enviamos este mail para informarle que tienes agendada una cita para el día "+dia+", a la hora "+hora+", con el colaborador "+colaborador+", en la sede "+sede+"."
    else:
        plaintext = "Estimado colaborador, enviamos este mail para informarle que tienes agendada una cita para el día "+dia+", a la hora "+hora+", con el estudiante "+estudiante+", en la sede "+sede+"."

    ourmailsender = MailSender('info.eva.everis@gmail.com', 'sbjhvaqwgjcuvwsz', ('smtp.gmail.com', 587))

    #def set_message(self, in_plaintext, in_subject="", in_from=None, in_htmltext=None):


    ourmailsender.set_message(plaintext, asunto, sender)
    ourmailsender.set_recipients([tarjet])
    #ourmailsender.set_from(sender)
    #ourmailsender.set_recipients([request_body["text"]])        
    ourmailsender.connect()
    ourmailsender.send_all()
    print("Success!!")
    
    result = {
                "result": "enviado a "+tarjet
    }
    #except:
    #    result = {
    #                "result": "NO enviado a "+tarjet
    #    }

    print(result)
    return result


if __name__ == "__main__":
    #start_logging_conf()    
    app.run(debug=True, port=8002)
    #test_functions()
