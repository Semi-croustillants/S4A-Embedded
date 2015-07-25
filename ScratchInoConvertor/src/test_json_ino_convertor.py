import sys
import os
import JsonInoConvertor as JsonInoConvertor
from ScratchInoConv import ExtractionDuNom

fileName = ExtractionDuNom(sys.argv[1].decode('utf8'))
convertor = JsonInoConvertor(typeArduino=sys.argv[2])
# controls_scratch/controls.sb2
# print ExtractionDuNom(sys.argv[1].decode('utf8'))
if not os.path.exists("sketch/" + fileName):
    os.makedirs("sketch/" + fileName)

convertor.convertSpriteScripts(
        sys.argv[1].decode('utf8'),
        "sketch/" + fileName + "/" + fileName + ".ino")
os.chdir("sketch")
os.chdir(fileName)
os.startfile(fileName + ".ino")
