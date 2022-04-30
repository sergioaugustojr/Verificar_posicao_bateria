#Script para monitorar o nível de bateria do rastreador e se o rastreador se deslocou
#Script desenvolvido para fins de estudo, sem objetivos comerciais
#Premissas:
#Se o nível de bateria for menor que xxx % enviar uma mensagem de email
#Se o veículo se deslocar por xxx metros após estar parado por yyy minutos enviar uma mensagem de email
#======================================================
#Changelog
#29/04/2022
#Início do desenvolvimento do script
#=====================================================
#Agradecimentos e referências
#Função para envio de emails:
#https://code.tutsplus.com/pt/tutorials/sending-emails-in-python-with-smtp--cms-29975
#Função para obter o endereço de IP:
#https://www.codegrepper.com/code-examples/python/python+get+public+ip+address


#Bibliotecas utilizadas
import datetime 
import mysql.connector
import json
import sys
import smtplib
from haversine import haversine, Unit
from requests import get
from datetime import timedelta
from mysql.connector import Error
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Variáveis globais
agora = datetime.datetime.now() 
desenvolvimento = 1
id_posicao = 0 #id da ultima posição do banco de dados
percentual_minimo = 35 #percentual minimo da bateria do rastreador
bateria_fraca = 0 #memoria de mensagem de bateria fraca enviada
em_movimento = 0 #o veiculo está em movimento?
distancia_maxima = 20 #20 metros
minutos_movimento = 5 #tempo de veículo parado

#Parâmetros do email
email_usr = "seu_usuario_de_email"
email_pw = "sua_senha_de_email"
email_dest = "destinatario_das_mensagens_de_email"

#Parâmetros do banco de dados SQL
db_host = 'host_do_banco_de_dados'
db_port = 'porta_do_banco_de_dados'
db_usr = 'usuario_do_banco_de_dados'
db_pw = 'senha_do_banco_de_dados'
db_database = 'database'

#funções
def conecta_sql():
    try:
        cnx = mysql.connector.connect(user=db_usr, password=db_pw,
            host=db_host,
            database=db_database,
            port=db_port)
        return cnx
    except Exception as err:
        print('Erro ao conectar com o banco de dados SQL')
        print(err)
        sys.exit()

def status_carro():
    #Função para consultar no banco de dados Mysql a ultima atualização do rastreador
    try:
        connection = conecta_sql()
        mycursor = connection.cursor()
        mycursor.execute("SELECT id, latitude, longitude, servertime, attributes FROM tc_positions where deviceid=1 order by servertime desc LIMIT 2")
        myresult = mycursor.fetchall()
        connection.commit()
        connection.close()
        return myresult
    except Exception as err:
        print('Erro ao realizar a consulta no banco de dados SQL')
        print(err)
        sys.exit()

def distancia_coordenadas(ponto1,ponto2):
    try:
        distancia = haversine(ponto1,ponto2,unit='m')
        return distancia
    except Exception as err:
        print('Erro ao calcular a distância entre as medições')
        sys.exit()
        print(err)
    

def proxima_hora(hora_atual,intervalo_tempo): 
    #Função para determinar a hora da próxima verificação
    try:
        hora = timedelta(hora_atual=+intervalo_tempo)
        return hora
    except Exception as err:
        print('Erro ao calcular a próxima hora')
        print(err)
        sys.exit()

def mensagem_bateria(nivel_bateria):
    #função para enviar o email se a bateria estiver fraca
    try:
        aux_bat = int(nivel_bateria)
    except exception as err:
        print('Falha ao converter o nível da bateria para inteiro')
        print(err)
    if(aux_bat <= percentual_minimo):
        #Verifica se o rastreador já estava com a bateria fraca no log anterior, caso positivo não envia o email
        try:
            connection = conecta_sql()
            mycursor = connection.cursor()
            mycursor.execute("SELECT BATERIA_FRACA FROM Monitoramento_veiculos WHERE ID = 1")
            myresult = mycursor.fetchall()
            connection.commit()
            connection.close()
            bateria_fraca = myresult[0][0]#Verifica se o rastreador já estava com a bateria fraca
            if(bateria_fraca == 1):
                print('O rastreador já estava com a bateria fraca')
            else:
                print('O rastreador agora está com a bateria fraca')
                nibat = 'O Rastreador esta com bateria fraca, nivel de bateria: ' + str(aux_bat) + '%'
                envia_email(email_dest,'O rastreador esta com a bateria fraca',nibat)#envia o email de bateria fraca

        except Exception as err:
            print('Erro ao consultar o monitoramento de bateria')
            print(err)
            sys.exit()

        bateria_fraca = 1
        return bateria_fraca
    else:
        bateria_fraca = 0
        print('O rastreador está com a bateria carregada')
        return bateria_fraca

def ip_servidor():
    try:
        ip = get('https://api.ipify.org').text
        ip = str(ip)
    except Exception as err:
        print('Erro ao obter o endereço de IP')
        print(err)
        sys.exit()
   return ip

def mensagem_movimento(movendo,dista):
    #função para enviar o emails e o veículo estiver em movimento
    #se o veículo estiver em movimento, atualizar a variável
    #se o veículo estiver parado por mais de xxx minutos enviar email
    if(movendo == 1):
        try:#Obtém as informações no DB
            connection = conecta_sql()
            mycursor = connection.cursor()
            mycursor.execute("SELECT EM_MOVIMENTO, ULTIMO_MOVIMENTO FROM Monitoramento_veiculos WHERE ID = 1")
            myresult = mycursor.fetchall()
            connection.commit()
            connection.close()
            movend = myresult[0][0]#Verifica se o rastreador já estava em movimento no DB
            ult_mov = myresult[0][1]#Obtém a data e a hora do último movimento
            if(movend == 0):#O veículo estava parado e começou a se mover
                hora_atual = datetime.datetime.now()
                hora_registro = datetime.datetime.strptime(ult_mov, '%Y-%m-%d %H:%M:%S.%f')
                hora_parado = hora_registro + timedelta(minutes = minutos_movimento)#Hora em que o veículo deve estar parado para considerar o movimento (Ex: Evitar de enviar email por causa de trânsito)
                print('Hora registro: ' + str(hora_registro))
                print('Hora parado: ' + str(hora_parado))
                if(hora_atual > hora_parado):
                    print('O veículo está em movimento após estar parado por pelo menos ' + str(minutos_movimento) + ' minutos')
                    movendo = 1
                    msg = "O veiculo esta se movendo, endereco de IP do servidor: " + str(ip_servidor)
                    envia_email(email_dest,'O veiculo esta se movimentando!',msg)

        except Exception as err:
            print('Erro ao obter a hora do último movimento no banco de dados')
            print(err)
            sys.exit()
    else:
        movendo = 0
    return movendo

def envia_email(destinatario,assunto,mensagem):
    #função para enviar o email
    # create message object instance
    try:
        msg = MIMEMultipart()
        message = mensagem
        
        # setup the parameters of the message
        password = email_pw
        msg['From'] = email_usr
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()
        print('Mensagem de email enviada com sucesso')
    except Exception as err:
        print('Erro ao enviar a mensagem de email')
        print(err)


def atualiza_db(bat,mov,dist):
    #função para atualizar o mysql com o status do veículo
    try:
        connection = conecta_sql()
        mycursor = connection.cursor()
        hora_atual = datetime.datetime.now()
        if(mov == 1):
            mycursor.execute("UPDATE Monitoramento_veiculos SET BATERIA_FRACA=%s, EM_MOVIMENTO=%s, DISTANCIA=%s, ULTIMO_MOVIMENTO=%s, TIMESTAMP=%s WHERE ID = 1", (int(bat), int(mov), str(dist), str(datetime.datetime.now()), str(datetime.datetime.now())))
        else:
            mycursor.execute("UPDATE Monitoramento_veiculos SET BATERIA_FRACA=%s, EM_MOVIMENTO=%s, DISTANCIA=%s, TIMESTAMP=%s WHERE ID = 1", (int(bat), int(mov), str(dist), str(datetime.datetime.now())))   
        connection.commit()
        connection.close()
        print('O banco de dados foi atualizado com sucesso')
    except Exception as err:
        print('Falha ao atualizar o banco de dados')
        print(err)

def verificar_carro():
    print('iniciando a verificação do carro....')
    try:
        status = status_carro()#Obtém o status do carro
    except Exception as err:
        print('Erro ao obter o status do carro')
        print(err)
        sys.exit()
    try:
        data = json.loads(str(status[0][4])) #query json recebida do rastreador
        ponto1=(status[0][1],status[0][2]) #ponto da última localização
        ponto2=(status[1][1],status[1][2]) #ponto da penúltima localização
        dist = distancia_coordenadas(ponto1,ponto2) #calcula a distância entre os pontos
        bat_level = data["batteryLevel"]
    except Exception as err:
        print('Erro ao calcular a distância entre os pontos')
        print(err)
        sys.exit()
    try:
        link = "https://www.google.com/maps/place/" + str(status[0][1]) + "," + str(status[0][2]) #link para o google maps com a ultima localização
        bateria = data["batteryLevel"]
        #Printa o status do carro no console
        print('==================================================')
        print('Status do veículo')
        print('Última localização: ' + str(status[0][1]) + "," + str(status[0][2]))
        print(link)
        print('Nível de bateria: ' + str(bat_level) + '%')
    except Exception as err:
        print('Erro ao imprimir o LOG no console')
        print(err)
        sys.exit()
    try:
        if(dist >= distancia_maxima):
            em_movimento = 1
        else:
            em_movimento = 0
        if(em_movimento == 1):
            print('Veículo em movimento')
        else:
            print('Veículo parado')
            print('Distância entre as posições: ' + str(distancia_maxima) + ' metros')
    except Exception as err:
        print('Falha ao detectar o movimento')
        print(err)
        sys.exit()
    
    bateria_fraca = mensagem_bateria(bat_level)
    em_movimento = mensagem_movimento(em_movimento,dist)
    atualiza_db(bateria_fraca,em_movimento,dist)

#Executa o programa
verificar_carro()