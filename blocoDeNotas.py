import PySimpleGUI as smp
import Parser as parser
import testGraphs as tg

newFile = "New (CTRL + N)"
openFile = "Open...(CTRL + O)"
saveFile = "Save(CTRL + S)"
class blocoDeNotas:
    def __init__(self) -> None:
        smp.change_look_and_feel("DarkBlack")
        WIN_W = 90
        WIN_H = 30
        self.fileName = None

        layoutMenu = [
            ["File", [newFile, openFile, saveFile, "Save as", "---", "Exit"]],
            ["Tools", ["Word counter", "Run code", "Compare files"]],
            ["Configuration", ["Read the content"]],
            ["Help", ["About"]]
        ]

        layout = [
            [smp.Menu(layoutMenu)],
            [smp.Text("New file", font=("Consolas", 10), size=(WIN_W, 1), key="_INFO_")],
            [smp.Multiline(font=("Consolas", 12), size=(WIN_W-30, WIN_H-10), key="_BODY_")],
            [smp.Output(font=('Consolas', 10), size=(WIN_W,WIN_H-25), key="_CONSOLE_")]
            ]

        self.window = smp.Window("Modelo Conceitual", layout=layout, margins=(0,0), resizable=True, return_keyboard_events=True, finalize=True)
        self.window.read(timeout=1)
        self.window["_BODY_"].expand(expand_x=True, expand_y=True)
        self.window["_CONSOLE_"].expand(expand_x=True, expand_y=True)
    

    def getWindow(self):
        return self.window
    
    def getFileName(self):
        return self.fileName
    
    def new_file(self):
        self.window["_BODY_"].update(value='')
        self.window["_INFO_"].update(value="New file")
        filename = None
        return filename

    def open_file(self):
        try:
            self.fileName = smp.popup_get_file("Open file", no_window=True)
        except:
            return
        
        if self.fileName not in (None, '') and not isinstance(self.fileName, tuple):
            with open(self.fileName, 'r') as f:
                self.window["_BODY_"].update(value=f.read())
                self.window["_INFO_"].update(value=self.fileName.split('/')[-1])
        return self.fileName

    def compare(self) -> None:
        try:
            self.fileNames = smp.popup_get_file("Open files", no_window=True, multiple_files=True)
        except:
            return
        
        try:
            if self.fileNames not in (None, ''):
                file1 = self.fileNames[0]
                file2 = self.fileNames[1]
                print(f'Similarity: {tg.teste_arquivos(file1, file2)}')
        except:
            print('Invalid files!')
            

    def save_file(self, fileName, values):
        if fileName not in (None, ''):
            with open(fileName, 'w') as f:
                f.write(values.get("_BODY_"))
            self.window['_INFO_'].update(value=fileName.split('/')[-1])
        else:
            self.saveFileAs(values)

    def saveFileAs(self, values):
        try:
            fileName = smp.popup_get_file('Save file', save_as=True, no_window=True)
        except:
            return
        if fileName not in (None, '') and not isinstance(fileName, tuple):
            with open(fileName,'w') as f:
                f.write(values.get('_BODY_'))
            self.window['_INFO_'].update(value=fileName.split('/')[-1])
        return fileName

    def wordCounter(self, values):
        words = [w for w in values['_BODY_'].split(' ') if w!='\n']
        word_count = len(words)
        smp.PopupQuick('Counter: {:,d}'.format(word_count), auto_close=False)

        
    def aboutMe(self):
        smp.PopupQuick('Author: Pedro Leonel, Computação, UFSM\n Models: PlantUML distributed by LGPL.', auto_close=False)

    def readContent(self, values):
        words = [w for w in values['_BODY_'].split('\n') if w!=' ' and w!='']
        return words
    
    def updateConsole(self):
       self.window['_CONSOLE_'].update(value='')




    
    
    

    