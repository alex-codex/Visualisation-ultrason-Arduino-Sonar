import serial
import serial.tools.list_ports
import pygame
import math
import time


# la difficulte la plus importante a surtout ete l'aspect mathematique,
# une fois que l'on peut donner les coordonnes cartesiennes sachant la distance( rayon en polaire)
# on utilise juste les fonctions de trace integrees dans la bibliotheque pygame
#les coordonnées sont données a partir du coin superieur gauche


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
port_serie = "COM3"  
baud_rate = 9600


ports = serial.tools.list_ports.comports()
available_ports = [port.device for port in ports]
if port_serie not in available_ports:
    print(f"Erreur : Le port série {port_serie} indispo")
    exit()

ser = serial.Serial(port_serie, baud_rate)
pygame.init()
largeur = 1000
hauteur = 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Visualisation ultrason")
rayon_max = 200  
angle_balayage = 180  
centre_x = largeur // 2
centre_y = hauteur // 2

def polaire_vers_cartesien(rayon, angle):
    x =  centre_x + rayon* math.cos(math.radians(angle))
    y =   centre_y - rayon * math.sin(math.radians(angle)) 
    return int(x), int(y)

angle =0
deplacement =10
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ser.close()
            exit()

    if ser.in_waiting > 0:
        ligne = ser.readline().decode('utf-8').rstrip()
        print(f"Donnees recues: {ligne}")  
        try:
            distance = float(ligne.split(":")[1].strip())
            rayon = min(distance, rayon_max)
            ecran.fill((0, 0, 0))
            
            #je trace le demi cercle avec des traits radiaux tous les 20°

            pygame.draw.line(ecran, WHITE, (centre_x - rayon_max, centre_y), (centre_x + rayon_max, centre_y), 1)
            pygame.draw.arc(ecran, WHITE, (centre_x - rayon_max, centre_y - rayon_max, 2 * rayon_max, 2 * rayon_max), math.radians(0), math.radians(180), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(20)),centre_y - rayon_max * math.sin(math.radians(20))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(40)), centre_y - rayon_max *math.sin(math.radians(40))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(60)), centre_y - rayon_max * math.sin(math.radians(60))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(80)), centre_y - rayon_max* math.sin(math.radians(80))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(100)), centre_y - rayon_max* math.sin(math.radians(80))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(120)), centre_y - rayon_max * math.sin(math.radians(60))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(140)),centre_y - rayon_max* math.sin(math.radians(40))), 1)
            pygame.draw.line(ecran ,GREEN, (centre_x,centre_y),(centre_x + rayon_max* math.cos(math.radians(160)), centre_y - rayon_max* math.sin(math.radians(20))), 1)
            abcisse_g = centre_x + rayon_max * math.cos(math.radians(angle))
            ordonne_g = centre_y - rayon_max * math.sin(math.radians(angle))  
            abcisse_d = centre_x + rayon_max * math.cos(math.radians(angle + 20))
            ordonne_d = centre_y - rayon_max * math.sin(math.radians(angle + 20))  
            
            line_color = YELLOW
           
           #position= pygame.Surface((40,40), pygame.SRCALPHA)

            if distance <= rayon_max:
                x,y =polaire_vers_cartesien(3*distance, angle-8)
                #pygame.draw.circle(ecran, RED ,(x,y), 5)
                pygame.draw.line(ecran, WHITE, (centre_x - rayon_max, centre_y), (centre_x + rayon_max, centre_y), 1)
                pygame.draw.arc(ecran, WHITE, (centre_x - rayon_max, centre_y - rayon_max, 2 * rayon_max, 2 * rayon_max), math.radians(0), math.radians(180), 1)
                pygame.draw.circle(ecran, RED ,(x,y), 5)
                #surface.blit(position , (x,y))

                #line_color=RED
            pygame.draw.polygon(ecran, line_color, [(centre_x,centre_y), (abcisse_g, ordonne_g),(abcisse_g +1, ordonne_g-1),(abcisse_d -1, ordonne_d -1),(abcisse_d, ordonne_d)])
            
            angle+= deplacement
            if angle >= 160 or angle <= 0:  
                deplacement*= -1

            #ecran.blit(surface , (centre_x, centre_y))
            pygame.display.flip() 
            pygame.time.Clock().tick(60)

        except ValueError as e:
            print(f"Erreur de conversion des données : {e}")  
   

    