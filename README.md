# Package-Affichage-LED-pour-Constellation-
Ce paquet permet de gérer l’affichage de différents paquets constellation sur une seule matrice LED RGB 8x32. Le paquet gère l’affichage d’une icône RGB (8x8), d’un texte blanc avec défilement ou alors directement d’une matrice 8x32 RGB (pour un affichage personnalisé).

## Installation
### Liste des composants 
Pour utiliser ce paquet vous aurez besoin des trois composants suivants :
* Matrice LED RGB 8x32 : [Amazon](https://www.amazon.fr/gp/product/B01DC0IPVU/)
* Raspberry Pi 3 : [Amazon](https://www.amazon.fr/Raspberry-Pi-Carte-Mère-Model/dp/B01CD5VC92/)
* 3x câble de connexion F/F : [Amazon](https://www.amazon.fr/Philonext-Multicolore-M%C3%A2le-Femelle-Femelle-Femelle-Breadboard/dp/B072NSLB98)

_Note:_ il est également possible d'utiliser un Raspberry Pi Zero à la place du Raspberry Pi 3, moins coûteux mais aussi non testé à la création du paquet !

### Connexion de la matrice LED 
La matrice LED possède 8 connexions différentes.

| Matrice pin | Description                 | RPi Pin | RPi Fonction |
| ----------- | --------------------------- | ------- | ------------ |
| **5V**      | Alimentation +5V            | 2       | 5V0          |
| **GND**     | Terre                       | 6       | GND          |
| **DIN**     | Entrée données              | 40      | GIO 21       |
| 5V          | Alimentation supplémentaire | •       | •            |
| DIN         | Entrée données              | •       | •            |
| _5V_        | Sortie                      | •       | •            |
| _GND_       | Sortie                      | •       | •            |
| _DOUT_      | Sortie                      | •       | •            |

Les **pins en gras** sont obligatoires pour l'affichage. 
Les _pins en italiques_ permettent de relier la matrice LED à une autre en série et donc de transférer l'information simplement. Les deux pins centraux ne sont utiles que dans le cas où de nombreuses LED sont utilisées à pleine puissance.

_Note:_ Il n'est pas recommandé d'allumer toutes les LED de la matrice en blanc en même temps quel que soit le mode de branchement. De plus, il est fortement conseillé d'allimenter le Raspberry Pi ainsi que la matrice LED à l'aide d'une source indépendante afin de ne pas trop tirer sur le pin 5V (ce qui résultera d'une instabilité générale du système). 

### Configuration
Le package ne fonctionne que sur Raspberry Pi et possède deux dépendances qu'il est nécessaire d'installer au préalable :  [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) pour la gestion des LED et [PILLOW](https://github.com/python-pillow/Pillow) pour la génération de texte.
`$ sudo pip2 install rpi_ws281x`
`$ sudo pip2 install Pillow`

### Utilisation
---------------
Le package n'a pas de configuration ni d'intelligence particulière, il ne fait qu'attendre un `message Callback` de Constellation pour se mettre à jour avec la syntaxe suivante :
```python
DISPLAY_PACKAGE = "ConstellationAffichageLED"
Constellation.SendMessage(DISPLAY_PACKAGE, "DisplayContent", {"icon":"votreIcone", "text":"Votre texte","time":None,"matrix":None})
```
Voici la description des paramètres 
- `icon` : nom de l'icone au format .jpg 8x8 à afficher à gauche de la matrice. L'image doit être placée dans le dossier ./img avec "Copy if Newer"
- `text` : texte à afficher à droite de l'icone
- `time` : à utiliser pour afficher l'affichage comme une notification push pendant le temps spécifié (en secondes) / Mettre None sinon
- `matrix` : matrice 8x32 avec des truples RGB pour un affichage 100% personnalisé. Prioritaire sur 'icon' et 'text'.
_Note :_ les attributs `time` et `matrix` sont existants mais non implémantés 
