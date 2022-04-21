from subprocess import run

import PySimpleGUI as sg
from blocoDeNotas import *
import Parser as parser
import ParserToUml as parserToUml
import PySimpleGUI as smp
import plantUmlLocal
import Vizualizador



vizualizador = Vizualizador.Visuazador()
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
        elif event == "Word counter":
            blocoDeNotas.wordCounter(values)
        elif event == "About":
            blocoDeNotas.aboutMe()
        if window == janelaVizualizador and event == sg.WIN_CLOSED:
            janelaVizualizador.close()
        if window == janelaVizualizador and event == "Save":
            vizualizador.save_image()

            
        elif window == janelaBlocoDeNotas and event == "Run code" or event == 'r:82':
            blocoDeNotas.updateConsole()
            actualParser.setLinhas(blocoDeNotas.readContent(values))
            actualParser.traduzLinhas()
            if actualParser.getModelo() != None:
                actualParser.getModelo().getNomes()
                parserUml = parserToUml.ParserToUml(actualParser.getModelo())
                plantUmlLocal.inicialization()
                janelaVizualizador = vizualizador.getWindow()
                
        
                
                
                


