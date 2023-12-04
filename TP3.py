
import usocket as socket
import network   #on importe la librairie network 
import machine #on importe Pin de la librairie machine
import urequests, ujson #on importe les librairie pour le http 
import time
pin = machine.Pin(2, machine.Pin.OUT) #définition du pin de la led


# port utilisé 
portTCP  = 2565;
portUDP  = 2563;
IPserveur = '192.168.2.106'; #adresse ip ordi



#led = Pin(2, Pin.OUT) #on configure la pin 16 comme sortie (la où est connecté la led)

#Connexion au  WIFI

SSID = 'electroProjectWifi' #nom du wifi
PASSWORD = 'M13#MRSE'       #mdp du wifi


wlan = network.WLAN(network.STA_IF) #Creer un objet WLAN et l'initialise
wlan.active(True)           #Permet d'activer la connexion

if not wlan.isconnected():  #si pas connecté
    wlan.connect(SSID, PASSWORD)     #se connecte au wifi en utilisant ssid et WiFi_pass
    while not wlan.isconnected():    #boucle tant que la connection n'est pas établit 
        pass
    
print('connectée', SSID)   #affiche qu'on se connecte



  
pin.value(0) # allume la led

def envoieTCP(data):  #fonction d'envoie TCP
    s = socket.socket() #crée un objet socket
    # ci-dessous recherche les info de l'IP et le port du seveur
    # ça renvoie une liste d'informations d'adresse et [0][-1] sélectionne la dernière adresse de cette liste.
    addr = socket.getaddrinfo(IPserveur, portTCP)[0][-1] 
    print(addr) # affiche l'adresse obtenue
    print(data) # affiche data 
    s.connect(addr) #  établit une connexion avec le serveur en utilisant l'adresse
    # Convertit les données (data) en chaîne de caractères,puis les encode en utilisant UTF-8 avant de les envoyer
    # à travers la connexion TCP à l'aide de la méthode write(). 
    s.write(str(data).encode()) 
    #s.sendall(str(data).encode())
    s.close() # ferme la connexion socket

def envoieUDP(data): #fonction d'envoie TCP
    # Crée un objet socket s1 spécifiant que l'utilisation sera pour le protocole IPv4 (socket.AF_INET)
    # et pour le type de socket datagramme (socket.SOCK_DGRAM), ce qui indique l'utilisation d'UDP.
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(IPserveur, portUDP)[0][-1] # récupération adresse, similaire à la fonction plus au-dessus
    print(addr)  # affiche l'adresse obtenue
    print(data)  # affiche data
    #  Convertit les données (data) en chaîne de caractères, puis les encode en utilisant UTF-8 avant de les envoyer
    # à l'adresse spécifiée (via le tuple addr) à l'aide de la méthode sendto() de l'objet socket UDP s1.
    s1.sendto(str(data).encode(),addr)
    s1.close() # Ferme la socket UDP après l'envoi des données.

donnees_a_envoyer = 0

while True:
    pin.value(0)  # Allume la LED pour indiquer l'envoi de données

    # données transmises sur le socket  TCP
    try:
        envoieTCP(donnees_a_envoyer)
    except Exception as e:
        print("Erreur d'envoie donnée TCP:", e)

    # données transmises sur le socket  UDP
    try:
        envoieUDP(donnees_a_envoyer)
    except Exception as e:
        print("Erreur d'envoie donnée UDP:", e)
    pin.value(1) # éteint la LED
    time.sleep(0.09)  # délai d'envoie
    donnees_a_envoyer += 1 
    if donnees_a_envoyer>255:
        donnees_a_envoyer=0
      