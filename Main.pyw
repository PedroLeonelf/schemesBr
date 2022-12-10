from subprocess import run

import PySimpleGUI as sg
from blocoDeNotas import *
import Parser as parser
import ParserToUml as parserToUml
import PySimpleGUI as smp



blocoDeNotas = blocoDeNotas()
actualParser = parser.Parser()









if __name__ == '__main__':
    janelaBlocoDeNotas, janelaVizualizador = blocoDeNotas.getWindow(), None
    while True:
        window, event, values = smp.read_all_windows()
        if window == janelaBlocoDeNotas and event in (None, "Exit"): 
            break
        elif event in (newFile, 'n:78', ):
            fileName = blocoDeNotas.new_file()
        elif event in (openFile, 'o:79', ):
            fileName = blocoDeNotas.open_file()
        elif event in (saveFile, 's:83', ):
            blocoDeNotas.save_file(blocoDeNotas.getFileName(), values)
        elif event == "Save as":
            fileName = blocoDeNotas.saveFileAs(values)
        elif event == "About":
            blocoDeNotas.aboutMe()
        elif event == "Compare schemas":
            blocoDeNotas.compare()



            
        elif window == janelaBlocoDeNotas and event == compileTxt or event == 'r:82':
            blocoDeNotas.updateConsole()
            actualParser.setLinhas(blocoDeNotas.readContent(values))
            actualParser.traduzLinhas()
            if actualParser.getModelo() != None:
                actualParser.getModelo().getNomes()
                parserUml = parserToUml.ParserToUml(actualParser.getModelo())

                
        
                
                
                


