Installation de ScratchInoConvertor

T�l�charger l'IDE Arduino, l'installer avec les drivers.

Coier le dossier ScratchInoConvertor dans un r�pertoire o� l'utilisateur
a les droits d'�criture

Copier le dossier artk dans le dossier HOME/Documents/Arduino/librairies

Pour cr�er un projet avec les blocs Arduino sur Scratch V2 :
- Ouvrir Scratch
- Charger le fichier importBlock.sb2

Il est inutile d'installer l'environnement A4S

Ici tu peux coder ton projet sur ScratchV2

Les sources de l'interface et du parser sont dans le dossier src de ScratchInoConvertor
N�cessite python2.7 et wxPython (32 bit), py2exe pour fonctionner

Pour recompiler l'interface :

python setup.py py2exe