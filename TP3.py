import network   #on importe la librairie network 
import usocket as socket
import urequests, ujson #on importe les librairie pour le http 
from machine import Pin #on importe Pin de la librairie machine
import time

# port 
portTCP  = 2565;
portUDP  = 2563;
IPserveur = '192.168.2.106'; #adresse ip ordi



led = Pin(2, Pin.OUT) #on configure la pin 16 comme sortie (la où est connecté la led)

#Connexion au  WIFI

SSID = 'electroProjectWifi' #nom du wifi
PASSWORD = 'M13#MRSE'       #mdp du wifi


wlan = network.WLAN(network.STA_IF) #Creer un objet WLAN et l'initialise
wlan.active(True)           #Permet d'activer la connexion

if not wlan.isconnected():  #si on est pas conneccté au wifi
    print('Connecting to Wi-Fi...')  #affiche qu'on se connecte
    wlan.connect(SSID, PASSWORD)     #se connecte au wifi en utilisant ssid et WiFi_pass
    while not wlan.isconnected():    #boucle tant qu'on est pas connecté
        pass
    
print('connecte au wifi', SSID)   #affiche qu'on se connecte

#Pret à recevoir des données

led.value(0)    


def envoieTCP(data):
    s = socket.socket()
    addr = socket.getaddrinfo(IPserveur, portTCP)[0][-1]
    print(addr)
    print(data)
    s.connect(addr)
    s.write(str(data).encode())
    #s.sendall(str(data).encode())
    s.close()

def envoieUDP(data):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(IPserveur, portUDP)[0][-1]
    print(addr)
    print(data)
    s1.sendto(str(data).encode(),addr)
    s1.close()

data_to_send = 0

while True:
    led.value(0)  # Allume la LED pour indiquer l'envoi de données

    # Envoi des données sur la socket TCP
    try:
        envoieTCP(data_to_send)
    except Exception as e:
        print("Error sending TCP data:", e)

    # Envoi des données sur la socket UDP
    try:
        envoieUDP(data_to_send)
    except Exception as e:
        print("Error sending UDP data:", e)
    led.value(1)
    time.sleep(0.09)  # Ajoutez un délai en fonction de votre fréquence d'envoi
    data_to_send += 1
    if data_to_send>255:
        data_to_send=0
      # Éteint la LED