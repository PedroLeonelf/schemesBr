import PySimpleGUI as sg
import random
import string
from grafico.figuras import *

"""
    Demo application to show how to draw rectangles and letters on a Graph Element
    This demo mocks up a crossword puzzle board
    It will place a letter where you click on the puzzle
"""





sg.theme("NeutralBlue")
BOX_SIZE = 60

layout = [
    [sg.Text('Crossword Puzzle Using PySimpleGUI'), sg.Text('', key='-OUTPUT-')],
    [sg.Graph((800, 800), (0, 450), (450, 0), key='-GRAPH-',
              change_submits=True, drag_submits=False)],
    [sg.Button('Show'), sg.Button('Exit')]
]

window = sg.Window('Window Title', layout, finalize=True, resizable=True)

g = window['-GRAPH-']

rectangle(200,200,400,300,g)

line(100,50,200,200,g)
circle(100,10,100,g)

# for row in range(5):
#     for col in range(5):
#         if random.randint(0, 100) > 10:
#             g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
#         else:
#             g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='black')

#         g.draw_text('{}'.format('a'),
#                     (col * BOX_SIZE + 10, row * BOX_SIZE + 8))

while True:             # Event Loop
    
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    mouse = values['-GRAPH-']

    if event == '-GRAPH-':
        if mouse == (None, None):
            continue
        box_x = mouse[0]//BOX_SIZE
        box_y = mouse[1]//BOX_SIZE
        letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
        print(box_x, box_y)
        g.draw_text('{}'.format('a'),
                    letter_location, font='Courier 25')

window.close()