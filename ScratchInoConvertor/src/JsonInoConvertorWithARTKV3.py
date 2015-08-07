#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

# from fileinput import close
import zipfile


class JsonInoConvertor(object):

    instructions = dict()
    booleanTests = dict()
    globalVarStr = str()
    setupFunctionStr = str()
    loopFunctionStr = str()
    functionNameStr = str()
    nb_block = 0
    # nbBlockStr = str()
    pins = dict()
    var = []
    unknownVar = []
    servohashlist = []
    indentation = str()
    incr = "j"
    typeArduino = 0
    sleep_var = False

    def __init__(self, indentation="   ", typeArduino=0):
        super(JsonInoConvertor, self).__init__()

        self.instructions = dict()
        self.booleanTests = dict()
        self.globalVarStr = str()
        self.setupFunctionStr = str()
        self.loopFunctionStr = str()
        self.functionNameStr = str()
        self.nb_block = 0
        self.pins = dict()
        self.var = []
        self.unknownVar = []
        self.servohashlist = []
        self.indentation = str()
        self.incr = "j"
        self.typeArduino = 0
        self.sleep_var = False

        self.instructions = {
            'A4S (Arduino For Scratch).digitalWrite':
            self.digitalWriteConvertion,
            'doIf': self.doIfConvertion,
            'doIfElse': self.doIfElseConvertion,
            'readVariable': self.doReadVariable,
            'A4S (Arduino For Scratch).setVar:to:': self.customSetVar,
            'A4S (Arduino For Scratch).changeVar:by:': self.ChangeVar,
            'setVar:to:': self.SetVar,
            'changeVar:by:': self.ChangeVar,
            'A4S (Arduino For Scratch).analogRead':
            self.AnalogReadingConvertion,
            'A4S (Arduino For Scratch).analogWrite':
            self.AnalogWriteConvertion,
            'A4S (Arduino For Scratch).servoWrite':
            self.ServoWriteConvertion,
            'A4S (Arduino For Scratch).tone':
            self.toneConvertion,
            'A4S (Arduino For Scratch).notone':
            self.notoneConvertion,
            '*': self.OpertationConvertion,
            '+': self.OpertationConvertion,
            '-': self.OpertationConvertion,
            '/': self.OpertationConvertion,
            '%': self.OpertationConvertion,
            'doRepeat': self.doRepeatConvertion,
            'doUntil': self.doUntilConvertion,
            'wait:elapsed:from:': self.doWaitConvertion,
            'doWaitUntil': self.doWaitUntilConvertion,

        }

        self.booleanTests = {

            '&': self.reportAndConvertion,
            '|': self.reportOrConvertion,
            '=': self.reportEqualConvertion,
            'A4S (Arduino For Scratch).digitalRead':
            self.reportDigitalReadingConvertion,
            'low': self.reportFalseConvertion,
            'high': self.reportTrueConvertion,
            'not': self.reportNot,
            '<': self.reportCompareConvertion,
            '>': self.reportCompareConvertion,
        }

        self.functionNameStr = "void consumer"
        # self.nbBlockStr = "# define MAX_THREAD_LIST "
        self.setupFunctionStr = "void SetupARTK() {\n"
        # self.loopFunctionStr = "void consumer1() {\n  while(1){\n"
        # Voir pour incrémentation des consumer: créer à chaque
        # fois l'objet loopfunction différent pour chaque groupe de blocs

        self.indentation = indentation
        self.typeArduino = typeArduino

    def doIfConvertion(self, block, i, localVar):
        self.loopFunctionStr += i + "if ( "
        self.booleanTests[block[1][0]](block[1], localVar)
        # self.convertBooleanTestBlock( block[0] )
        self.loopFunctionStr += " ) {\n"
        self.convertScript(block[2], i, localVar)
        # self.convertScript( block[1], i + self.indentation )
        self.loopFunctionStr += i + "}\n"

    def doUntilConvertion(self, block, i, localVar):
        # print block
        self.loopFunctionStr += i + "while ( "
        self.booleanTests[block[1][0]](block[1], localVar)
        self.loopFunctionStr += " ) {\n"
        self.loopFunctionStr += i + self.indentation
        self.convertScript(block[2], i, localVar)
        # self.convertScript( block[1], i + self.indentation )
        if (not (self.sleep_var)):
            self.loopFunctionStr += i + self.indentation + "ARTK_Yield();\n"
        self.sleep_var = False
        self.loopFunctionStr += i+"}\n"

    def doWaitConvertion(self, block, i, localVar):
        x = float(block[1]) * 1000
        self.loopFunctionStr += i + "ARTK_Sleep("
        self.loopFunctionStr += str(int(x))
        self.loopFunctionStr += ");\n"
        self.sleep_var = True

    def doWaitUntilConvertion(self, block, i, localVar):
        # print "lolilol"
        # print block
        self.loopFunctionStr += i + "while ( "
        self.booleanTests[block[1][0]](block[1], localVar)
        # self.convertBooleanTestBlock( block[0] )
        self.loopFunctionStr += " ) {\n"
        self.loopFunctionStr += i + self.indentation + "ARTK_Sleep(50);\n"
        self.loopFunctionStr += i + "}\n"

    def doRepeatConvertion(self, block, i, localVar):
        # à revoir: tester si non à l'intérieur d'un autre dorepeat
        # (changer la variable d'incrémentation)
        this_incr = self.incr
        self.incr += "j"
        self.loopFunctionStr += i + "for (int "+this_incr+"=0; "+this_incr+"< "

        self.loopFunctionStr += str(block[1])
        self.loopFunctionStr += "; "+this_incr+"++) {\n"
        self.convertScript(block[2], i + self.indentation, localVar)
        # self.convertScript( block[1], i + self.indentation )
        if (not (self.sleep_var)):
            self.loopFunctionStr += i + i + "ARTK_Yield();\n"
        self.sleep_var = False
        self.loopFunctionStr += i+"}\n"

    def digitalWriteConvertion(self, block, i, localVar):

        pin = block[1]
        if not (pin in self.pins):
            self.pins[pin] = 'OUTPUT'
            self.setupFunctionStr += self.indentation\
                + "pinMode( " + str(pin) + ", OUTPUT );\n"

        elif self.pins[pin] != 'OUTPUT':
            e = Exception(
                "Warning digitalWriteConvertion : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)

        self.loopFunctionStr += i + "digitalWrite( " + str(pin) + ", "
        self.booleanTests[block[2]](block[2], localVar)
        # self.convertBooleanTestBlock( block[1] )
        self.loopFunctionStr += " );\n"

    def toneConvertion(self, block, i, localVar):

        pin = block[1]
        note = block[2]
        if not (pin in self.pins):
            self.pins[pin] = 'OUTPUT'
            self.setupFunctionStr += self.indentation\
                + "pinMode( " + str(pin) + ", OUTPUT );\n"

        elif self.pins[pin] != 'OUTPUT':
            e = Exception(
                "Warning tone : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)
        self.loopFunctionStr += i + "tone( " + str(pin) + ", "
        if isinstance(note, int) or isinstance(note, basestring):
            self.loopFunctionStr += str(note)
        else:
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
        self.loopFunctionStr += " );\n"

    def notoneConvertion(self, block, i, localVar):

        pin = block[1]
        if not (pin in self.pins):
            self.pins[pin] = 'OUTPUT'
            self.setupFunctionStr += self.indentation\
                + "pinMode( " + str(pin) + ", OUTPUT );\n"

        elif self.pins[pin] != 'OUTPUT':
            e = Exception(
                "Warning notone : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)

        self.loopFunctionStr += i + "noTone( " + str(pin) + " );\n"

    def ServoWriteConvertion(self, block, i, localVar):
        pin = block[1]
        if not any(servo['pin'] == pin for servo in self.servohashlist):
            self.servohashlist.append({"pin": pin})
            self.pins[pin] = 'SERVO'
            self.setupFunctionStr += self.indentation\
                + "myservo" + str(pin) + ".attach(" + str(pin) + ");\n"
        elif self.pins[pin] != 'SERVO':
            e = Exception(
                "Warning ServoWriteConvertion : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)
        self.loopFunctionStr += i + "myservo" + str(pin) + ".write( "
        if isinstance(block[2], int) or isinstance(block[2], basestring):
            self.loopFunctionStr += str(block[2])
        else:
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
        self.loopFunctionStr += " );\n"

    def AnalogWriteConvertion(self, block, i, localVar):
        pin = block[1]
        if not (pin in self.pins):
            self.pins[pin] = 'OUTPUT'
            self.setupFunctionStr += self.indentation\
                + "pinMode( " + str(pin) + ", OUTPUT );\n"

        elif self.pins[pin] != 'OUTPUT':
            e = Exception(
                "Warning AnalogWriteConvertion : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)

        self.loopFunctionStr += i + "AnalogWrite( " + str(pin) + ", "
        if (not isinstance(block[1], basestring) and (
                                            not isinstance(block[1], int))):
            self.instructions[block[1][0]](block[1], "", localVar)
            if "setVar:to:" in block[1][0]:
                    localVar.append(block[1][1])
        else:
            # print block[1]
            self.loopFunctionStr += str(block[1])
        self.loopFunctionStr += " );\n"

    def doIfElseConvertion(self, block, i, localVar):

        self.loopFunctionStr += "if ( "
        self.booleanTests[block[1][0]](block[1], localVar)
        self.loopFunctionStr += " ) {\n"
        self.convertScript(block[2], i + self.indentation, localVar)
        # self.instructions[block[2][0]](block[2],i)
        self.loopFunctionStr += i + "}\n" + i + "else {\n"
        self.convertScript(block[3], i + self.indentation, localVar)
        # self.instructions[block[3][0]](block[3],i)
        self.loopFunctionStr += i + "}\n"

    def reportDigitalReadingConvertion(self, block, localVar):

        pin = block[1]
        if not (pin in self.pins):
            self.pins[pin] = 'INPUT'
            self.setupFunctionStr += self.indentation\
                + "pinMode( " + str(pin) + ", INPUT );\n"

        elif self.pins[pin] != 'INPUT':
            e = Exception(
                "Warning reportDigitalReadingConvertion : pin"
                + str(pin) + "already use in" + str(self.pins[pin]) + "status")
            raise(e)
        self.loopFunctionStr += "digitalRead( " + str(pin) + " )"

    def AnalogReadingConvertion(self, block, i, localVar):
        pin = block[1]
        self.loopFunctionStr += i+"analogRead( " + str(pin) + " )"

    def reportAndConvertion(self, block, localVar):
        # print "( "
        self.loopFunctionStr += "( "
        self.booleanTests[block[1][0]](block[1], localVar)
        # self.convertBooleanTestBlock( block[0] )
        # print " ) && ( "
        self.loopFunctionStr += " ) && ( "
        self.booleanTests[block[2][0]](block[2], localVar)

        self.loopFunctionStr += " )"

    def reportCompareConvertion(self, block, localVar):
        # print block
        if (not isinstance(block[1], basestring)):
            self.instructions[block[1][0]](block[1], "", localVar)
            if "setVar:to:" in block[1][0]:
                    localVar.append(block[1][1])
        else:
            # print block[1]
            self.loopFunctionStr += str(block[1])

        # print " == "
        self.loopFunctionStr += block[0]

        if (not isinstance(block[2], basestring)):
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
        else:
            # print block[2]
            self.loopFunctionStr += str(block[2])

    def OpertationConvertion(self, block, i, localVar):
        # print block
        self.loopFunctionStr += "( "
        if ((not isinstance(block[1], basestring)) and (
                                            not isinstance(block[1], int))):
            self.instructions[block[1][0]](block[1], "", localVar)
            if "setVar:to:" in block[1][0]:
                    localVar.append(block[1][1])
        else:
            # print block[1]
            self.loopFunctionStr += str(block[1])

        # print " == "
        self.loopFunctionStr += " " + block[0] + " "

        if ((not isinstance(block[2], basestring)) and (
                                            not isinstance(block[2], int))):
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
        else:
            # print block[2]
            self.loopFunctionStr += str(block[2])
        self.loopFunctionStr += " )"

    def reportEqualConvertion(self, block, localVar):
        # print block
        self.loopFunctionStr += "( "
        if (not isinstance(block[1], basestring) and (
                                            not isinstance(block[1], int))):
            self.instructions[block[1][0]](block[1], "", localVar)
            if "setVar:to:" in block[1][0]:
                    localVar.append(block[1][1])
        else:
            # print block[1]
            self.loopFunctionStr += str(block[1])

        # print " == "
        self.loopFunctionStr += " == "

        if (not isinstance(block[2], basestring) and (
                                            not isinstance(block[2], int))):
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
        else:
            # print block[2]
            self.loopFunctionStr += str(block[2])
        self.loopFunctionStr += " )"

    def customSetVar(self, block, i, localVar):
        if (block[2] == "global"):
            if (not (block[1] in self.var)):
                self.var.append(block[1])
                self.globalVarStr += str(block[3]) + " " + str(block[4]) +\
                    " " + str(block[1]) + ";\n"
            else:
                e = Exception(
                    "Warning setVar ambiguous : var",
                    "\"" + str(block[1]) + "\"", "already declared globally",
                    "Please use changeValue instead")
                raise(e)
            if (block[1] in self.unknownVar):
                self.unknownVar.remove(block[1])
            self.loopFunctionStr += block[1] + " = "
            if (not isinstance(block[5], basestring) and (
                                            not isinstance(block[5], int))):
                self.instructions[block[5][0]](block[5], "", localVar)
            else:
                self.loopFunctionStr += str(block[5])
            self.loopFunctionStr += ";\n"
        elif (block[2] == "local"):
            if (block[1] in localVar):
                e = Exception(
                    "Warning setVar ambiguous : var",
                    "\"" + str(block[1]) + "\"", "already declared locally")
                raise(e)
            else:
                localVar.append(block[1])
                self.loopFunctionStr += str(block[3]) + " " + str(block[4]) +\
                    " " + str(block[1]) + " = "
                if (not isinstance(block[5], basestring) and (
                                            not isinstance(block[5], int))):
                    self.instructions[block[5][0]](block[5], "", localVar)
                    if "setVar:to:" in block[5][0]:
                        localVar.append(block[5][1])
                else:
                    self.loopFunctionStr += str(block[5])
                self.loopFunctionStr += ";\n"

    def SetVar(self, block, i, localVar):
        e = Exception(
                "Warning do not use internal Scratch setVar.",
                "Possibility of mis understood type")
        raise(e)
        # if (block[1] in localVar):
        #    e = Exception(
        #        "Warning setVar ambiguous : var",
        #        "\"" + str(block[1]) + "\"", "already declared locally")
        #    raise(e)
        # elif (not (block[1] in self.var)):
        #    localVar.append(block[1])
        #    if isinstance(block[2], basestring):
        #        if "." not in str(block[2]):
        #            self.loopFunctionStr += i + "int " + block[1] + " = "
        #        else:
        #            self.loopFunctionStr += i + "float " + block[1] + " = "
        #    elif isinstance(block[2], int):
        #        self.loopFunctionStr += i + "int " + block[1] + " = "
        # if (not isinstance(block[2], basestring) and (
        #                                    not isinstance(block[2], int))):
        #     print "c'est un bloc"
        #     print block[2]
        #    self.instructions[block[2][0]](block[2], "", localVar)
        #    if "setVar:to:" in block[2][0]:
        #            localVar.append(block[2][1])
        #    self.loopFunctionStr += ";\n"
        # else:
        #     print "c'est pas un bloc"
        #     print block[2]
        #    self.loopFunctionStr += str(block[2]) + ";\n"

    def ChangeVar(self, block, i, localVar):
        # print block
        if (not (block[1] in localVar)) and (not (block[1] in self.var)):
            self.unknownVar.append(block[1])
            # self.var.append(block[1])
            # if (block[1] in self.unknownVar):
            #    self.unknownVar.remove(block[1])
            # if isinstance(block[2], basestring):
            #    if "." not in str(block[2]):
            #        self.globalVarStr += "int " + block[1] + ";\n"
            #    else:
            #        self.globalVarStr += "float " + block[1] + ";\n"
            # elif isinstance(block[2], int):
            #    self.globalVarStr += "int " + block[1] + ";\n"
            # elif isinstance(block[2], float):
            #    self.globalVarStr += "float " + block[1] + ";\n"
        self.loopFunctionStr += i + str(block[1])
        self.loopFunctionStr += " = "

        if (not isinstance(block[2], basestring) and (
                                            not isinstance(block[2], int)) and(
                                            not isinstance(block[2], float))):
            # print "c'est un bloc"
            # print block[2]
            self.instructions[block[2][0]](block[2], "", localVar)
            if "setVar:to:" in block[2][0]:
                    localVar.append(block[2][1])
            self.loopFunctionStr += ";\n"
        else:
            # print "c'est pas un bloc"
            # print block[2]
            self.loopFunctionStr += str(block[2]) + ";\n"

    def reportOrConvertion(self, block, localVar):
        self.loopFunctionStr += "( "
        self.booleanTests[block[1][0]](block[1], localVar)
        # self.convertBooleanTestBlock( block[0] )
        # print " ) && ( "
        self.loopFunctionStr += " ) || ( "
        self.booleanTests[block[2][0]](block[2], localVar)

        self.loopFunctionStr += " )"

    def reportNot(self, block, localVar):
        self.loopFunctionStr += "! ("
        if block[1][0] in self.instructions:
            # print "c'est une instruction:"
            # print element
            self.instructions[block[1][0]](block[1], "", localVar)
            if "setVar:to:" in block[1][0]:
                    localVar.append(block[1][1])
        elif block[1][0] in self.booleanTests:
            # print "c'est un test booleen:"
            # print element
            self.booleanTests[block[1][0]](block[1], localVar)
        else:
            e = Exception(
                "Warning script : bloc", block[1][0], "non géré...")
            raise(e)
        self.loopFunctionStr += ")"

    def doReadVariable(self, block, i, localVar):
        # print block
        if (not (block[1] in self.var) and (not (block[1] in localVar))):
            self.unknownVar.append(block[1])
            # self.var.append(block[1])
            # self.globalVarStr += "int " + block[1] + "=0;\n"

        self.loopFunctionStr += i + block[1]

    def reportFalseConvertion(self, block, localVar):

        self.loopFunctionStr += "LOW"

    def reportTrueConvertion(self, block, localVar):

        self.loopFunctionStr += "HIGH"

    def convertSpriteScripts(self, fileINName, fileOUTName):

        fileOUT = open(fileOUTName, "w")

        archive = zipfile.ZipFile(fileINName, 'r')
        json_data = archive.read('project.json')

        # json_data=open(jsondata)

        data = json.loads(json_data)
        curs = None
        for kindern in range(len(data['children'])):
            lala = data['children'][kindern]
            if lala.get('scripts', None) is not None:
                curs = kindern
        if curs is not None:
            for threadScript in data['children'][curs]['scripts']:
                print threadScript[2]
                self.convertThreadScript(threadScript[2], self.indentation, [])
            if (self.unknownVar):
                mess = "Error : Variable "
                for uvar in self.unknownVar:
                    mess += "\"" + str(uvar) + "\" "
                mess += "read but never set"
                raise(Exception(mess))
            self.setupFunctionStr += self.indentation + "ARTK_SetOptions("\
                + str(self.typeArduino) + ") ;\n"
            for i in range(1, self.nb_block + 1):
                self.setupFunctionStr += self.indentation\
                    + "ARTK_CreateTask(consumer" + str(i) + ");\n"
            self.setupFunctionStr += "}\n"
            # self.loopFunctionStr += "ARTK_Yield();\n}\n}\n"

            print "#include <ARTK.h>\n"
            if len(self.servohashlist) > 0:
                print "#include <Servo.h>\n"
                for servohash in self.servohashlist:
                    print "Servo myservo"+str(servohash["pin"])+";\n"
            print self.globalVarStr\
                + self.loopFunctionStr\
                + self.setupFunctionStr
            # Write in file
            fileOUT.write("#include <ARTK.h>\n")
            if len(self.servohashlist) > 0:
                fileOUT.write("#include <Servo.h>\n")
                for servohash in self.servohashlist:
                    fileOUT.write("Servo myservo"+str(servohash["pin"])+";\n")
            fileOUT.write(self.globalVarStr)
            fileOUT.write(self.loopFunctionStr)
            fileOUT.write(self.setupFunctionStr)
        else:
            raise(Exception("Scripts not found in sb2"))
        fileOUT.close()
        # print data

        # json_data.close()
        # print self.loopFunctionStr

    def convertThreadScript(self, threadScript, i, localVar):
        # print "on m'appelle"
        # print threadScript
        if (len(threadScript) >= 2):
            receiveGoBlock = threadScript[0]
            # print receiveGoBlock[0]
            # print doForeverBlock[1]
            if receiveGoBlock[0] != "whenGreenFlag" or (not receiveGoBlock[0]):
                e = Exception(
                    "Warning convertThreadScript : expected block receiveGo")
                raise(e)
            else:
                self.nb_block = self.nb_block + 1
                self.loopFunctionStr += "void consumer" \
                    + str(self.nb_block) + "() {\n"
                for bl in range(1, len(threadScript)):
                    afterGoBlock = threadScript[bl]
                    if afterGoBlock[0] != 'doForever' or (
                                            not afterGoBlock[0]):
                        if "setVar:to:" in afterGoBlock[0]:
                            self.instructions[afterGoBlock[0]](
                                afterGoBlock, self.indentation, localVar)
                            localVar.append(afterGoBlock[1])
                        elif 'changeVar:by:' in afterGoBlock[0]:
                            self.instructions[afterGoBlock[0]](
                                afterGoBlock, self.indentation, localVar)
                        else:
                            e = Exception(
                                "Warning convertThreadScript : "
                                "expected block doForever or variable\
 set/change")
                            raise e
                    else:
                        print i
                        self.loopFunctionStr += i + "while(1){\n"
                        self.convertScript(afterGoBlock[1], i, localVar)
                        self.loopFunctionStr += i + self.indentation\
                            + "ARTK_Yield();\n"

                        self.sleep_var = False
                self.loopFunctionStr += i + "}\n}\n"

    def convertScript(self, script, i, localVar):
        for element in script:
            # print element
            if element[0] in self.instructions:
                # print "c'est une instruction :"
                # print element
                self.instructions[element[0]](element,
                                              i + self.indentation,
                                              localVar)
                if "setVar:to:" in element[0]:
                    localVar.append(element[1])
            elif element[0] in self.booleanTests:
                # print "c'est un test booleen :"
                # print element
                self.booleanTests[element[0]](element, localVar)
            else:
                e = Exception(
                    "Warning script : bloc", element[0], "non géré...")
                raise(e)
