import time
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from neopixel import *

""" VARIABLES GLOABLES DE CONFIGURATION
    ===================================
"""

# Configuration des LED
LED_COUNT      = 256      # Nombre de LED
LED_PIN        = 10       # Pin de connection : mettre le GPIO 10 pour SPI (/dev/spidev0.0)
LED_FREQ_HZ    = 800000   # Frequence du signal en hertz (defaut : 800khz)
LED_DMA        = 5        # Chaine DMA pour generer le signal (defaut : 5)
LED_BRIGHTNESS = 15       # Luminosite de 0 a 255
LED_INVERT     = False    # True pour inverser le signal
LED_CHANNEL    = 0        # Mettre 1 pour les GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Type de matrice et ordre des couleurs (defaut : ws.WS2811_STRIP_GRB)
 
 
""" LISTES DES FONTIONS UTILES AU PROGRAMME 
    =======================================
"""

""" FONCTION : displayMatrix
	========================
	Permet d'afficher une matrice en allumant les LED une a une
	
	PARAMETRES :
	============
	offset : numero de la colonne de depart (/!\ bug: ne fonctionne qu'avec les colonnes paires)
	matrix : matrice ligne 1D contenant les informations de toutes les LED a afficher une a une
"""
def displayMatrix(offset, matrix):
	
	print matrix
	
	offset = 8*offset

	for i in range(0, len(matrix)):
		if matrix[i] > 0 and matrix[i] <= 255:
			matrix[i] = Color(200,200,200)

		strip.setPixelColor(i + offset, matrix[i])
		
	strip.show()
		
""" FONCTION : scroll
    =================
    Permet de faire defiler une matrice trop grande pour etre affichee sur la matrice LED 
    
    PARAMETRES:  
    ===========
    offset : numero de la colonne de depart (/!\ bug: ne fonctionne qu'avec les colonnes paires)
    matrix : matrice ligne 1D contenant les informations de toutes les LED a afficher une a une
    speed  : temps d'actualisation entre chaque déplacement de lettre
"""
def scroll(offset, matrix, speed = 1):	
	
	while True:
		displayMatrix(offset, matrix)
					
		matrix += matrix[:16]
		del matrix[:16]
	
		time.sleep(speed)
			

""" FONCTION : twitterLogo
    ======================
    Permet d'afficher le logo de Twitter en RGB sur un bloc de 8x8 à gauche de la matrice LED
"""			
def twitterLogo():
	
	logo = np.array([[Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0),Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0)],
	                 [Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0)],
	                 [Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238)],
         	         [Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0)],
	                 [Color(  0,  0,  0),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0)],
	                 [Color(  0,  0,  0),Color(  0,  0,  0),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0)],
	                 [Color(  0,  0,  0),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0)],
	                 [Color( 87,172,238),Color( 87,172,238),Color( 87,172,238),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0),Color(  0,  0,  0)]])
						
	return matrixToLine(logo)
	

""" FONCTION : matrixToLine
    =======================
    Permet de transformer une matrice 2D possédant les coordonnées (x,y) en une liste contenant toutes les données de LED adressables de 1 à 256  
    
    PARAMETRES:  
    ===========
    matrix : matrice ligne 2D possédant les coordonnées (x,y) d'un texte/image
"""
def matrixToLine(matrix):
	# Passage d'une matrice 2D a une ligne en trois etapes
	# 1. Transpotion
	matrix = matrix.transpose()
	# 2. Renverse les lignes impaires (anciennement colonnes)
	for i in range(0, len(matrix - 1)):
		if i % 2 != 0:
			matrix[i] = matrix[i][::-1]
	# 3. Passage ligne
	matrix = matrix.flatten()
	
	return matrix.tolist()
	
""" FONCTION : displayText
    ======================
    Permet de générer une matrice N/B de la taille du texte demmandé à l'aide de PILLOW 
    
    PARAMETRES:  
    ===========
    offset : numero de la colonne de depart (/!\ bug: ne fonctionne qu'avec les colonnes paires)
    text   : texte à générer
    font   : nom de la police d'écriture à mettre dans le dossier fonts/NAME_FONT.ttf
    icone  : (bool) s'il y a une icone 8x8 présente 
"""
def displayText(offset, text, font = "SMALL", icone = True):
	# Definition du texte et de sa taille :
	font = ImageFont.truetype("fonts/"+font+"_FONT.ttf", 8)
	wText, hText = font.getsize(text)
	# Creation d'une image de la taille du texte
	image = Image.new("L", (wText, 8), "black")
	draw = ImageDraw.Draw(image)
	draw.text((0, 0), text, fill="white", font=font)
	# Retourne une matrice bitmap si le text est petit / sinon fait defiler le text
	maxLED = 22 if icone else 32
	if wText <= maxLED:
		return displayMatrix(offset, matrixToLine(np.array(image)))
	else:
		return scroll(offset, matrixToLine(np.array(image)), speed = 0.5)

""" PROGRAMME PRINCIPAL
    ===================
"""

if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()
	
	displayMatrix(0, twitterLogo())
	displayText(10, "This  is a simple hello world with a very long text ! ", font="SMALL")
