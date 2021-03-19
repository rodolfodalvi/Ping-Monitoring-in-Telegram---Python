from telethon import TelegramClient, events, sync
from datetime import datetime, timedelta
from telethon.tl.types import UpdateShortMessage
import time, threading
import telnetlib
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

global ip_teste
global ip_name
ip_name = []
ip_teste = []
cont = 0
with open("config.txt", "r") as f:
    line = f.readline()
    pos_final = line.find("\n")
    line = line[0:pos_final]
    cont=cont+1
    ip_teste.append(str(line))
    while line:
        line = f.readline()
        pos_final = line.find("\n")
        line = line[0:pos_final]
        cont=cont+1
        if cont%2==1:
            ip_teste.append(str(line))
        if cont%2==0:
            ip_name.append(str(line))
f.close()


if len(ip_teste)>len(ip_name):
	ip_name.append(str(line))
if len(ip_teste_telnet)>len(ip_name_telnet):
	ip_name_telnet.append(str(line))
if len(ip_teste_telnet)>len(porta_teste_telnet):
	porta_teste_telnet.append(str(line))
    
user_atual = 'roboCheckIP'
api_id = SUBSTITUIR PELO ID DO ROBÔ DO TELEGRAM
api_hash = 'SUBSTITUIR PELO HASH DO ROBÔ DO TELEGRAM'
global client
client = TelegramClient(user_atual, api_id, api_hash)
client.start(bot_token='SUBSTITUIR PELO TOKEN DO ROBÔ DO TELEGRAM')
global chat_id
chat_id = SUBSTITUIR PELO ID DO CHAT DO TELEGRAM ONDE SERÁ DISPARADO O ALERTA

print("Detalhes da conta:\n")
print(client.get_me().stringify())

global servidoroff
servidoroff = []
print("Srvs teste ping:")
print(ip_teste)
print(ip_name)

@client.on(events.NewMessage)
async def my_event_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    user = sender.username
    print(str(chat))
    t_now = datetime.now()
    
    if event.raw_text.find("listar ips")!=-1 or event.raw_text.find("Listar ips")!=-1:
        await client.send_message(entity=chat, message=str(ip_teste))
    if event.raw_text.find("listar servidores")!=-1 or event.raw_text.find("Listar servidores")!=-1:
        await client.send_message(entity=chat, message=str(ip_name))
    elif event.raw_text.find("servidores off")!=-1 or event.raw_text.find("Servidores off")!=-1:
        servidoresOff()
    else:
        await client.send_message(entity=chat, message="Digite uma das opcoes: Listar ips; Servidores off; Listar servidores")
	
	

async def sendMessage(ent,msg):
    global client
    print(ent)
    print(msg)
    await client.send_message(entity=ent, message=msg)

def checarConexao():
    global primeira
    global client
    global servidoroff
    global chat_id
    if primeira==0:
        for i in range(0,len(ip_teste)):
            ping_result = ping(ip_teste[i])
            if ping_result==False:
                tem=0
                for ipoff in servidoroff:
                    if ipoff==ip_name[i]:
                        tem=1
                if tem==0:
                    servidoroff.append(ip_name[i])
                    try:
                        if len(ip_teste[i])>1:
                            client.loop.create_task(sendMessage(ent=chat_id, msg="Srv "+str(ip_name[i])+" ("+str(ip_teste[i])+") sem resposta"))
                    except:
                        x=1
            for ipoff in servidoroff:
                if ipoff==ip_name[i] and ping_result==True:
                    servidoroff.remove(ip_name[i])
                    try:
                        if len(ip_teste[i])>1:
                            client.loop.create_task(sendMessage(ent=chat_id, msg="Srv "+str(ip_name[i])+" ("+str(ip_teste[i])+") com conexao restabelecida"))
                    except:
                        x=1
        
    primeira = 0
    threading.Timer(20, checarConexao).start()  


def servidoresOff():
    global servidoroff
    global primeira
    print("srvoff")
    print(servidoroff)
    if primeira==0:
        if len(servidoroff)>1:
            try:
                client.loop.create_task(sendMessage(ent=chat_id, msg=("Srvs desconectados: "+str(servidoroff))))
            except:
                x=1
    
    threading.Timer(1*60, servidoresOff).start()

    
def ping(host):
    import os, platform

    if  platform.system().lower()=="windows":
        ping_str = "-n 1"
    else:
        ping_str = "-c 1"

    resposta = os.system("ping " + ping_str + " " + host)
    return resposta == 0

    
global primeira
primeira = 1
checarConexao()
servidoresOff()
while (1==1):
    HoraAtual = datetime.now()
    client.run_until_disconnected()   
    
