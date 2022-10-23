
import subprocess
from PIL import Image

import numpy as np




fileLocation = 'content/text_file.txt'







def inicialization():
    proc1 = subprocess.Popen("java -jar plantuml.jar -picoweb")
    proc2 = subprocess.Popen(f"python -m plantuml -s http://127.0.0.1:8080/plantuml/png/ {fileLocation}")
    fillImage()


def fillImage():
    img = Image.open('content/text_file.png')
    right = 300
    left = 300
    top = 0
    bottom = 0
    
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    
    result = Image.new(img.mode, (new_width, new_height), (0, 0, 255))
    
    result.paste(img, (left, top))
    
    result.save('content/text_file.png')


    cor_rosa_magenta = (255, 255, 255)

    im = Image.open('content/text_file.png').convert('RGB')

    # Pega a imagem como um numpy.array com formato altura x largura x num_canais
    data = np.array(im)

    #>>> print(data.shape)
    #    (200, 200, 3)

    # Pego cada canal como um array separado para facilitar reconhecer o branco
    vermelho, verde, azul = data.T

    # Defino a condição (ser branco)
    condicao = (vermelho == 0) & (verde == 0) & (azul == 255)
    # Substitui a cor branca pela cor desejada
    data[condicao.T] = cor_rosa_magenta

    # Volto o array para uma imagem do PIL
    im2 = Image.fromarray(data)
    im2.save('content/text_file.png')

        









        
    

            
