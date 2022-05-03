import PySimpleGUI as sg
import PIL
from PIL import Image
import io
import base64
import shutil

class Visuazador:
    def __init__(self) -> None:
        self.THUMBNAIL_SIZE = (500,200)
        self.THUMBNAIL_PAD = (1,1)
        self.ROOT_FOLDER = r'content/'
        self.screen_size = sg.Window.get_screen_size()
        self.IMAGE_SIZE = (self.screen_size[0]-800,self.screen_size[1]-800)
        self.file_types = [("PNG (*.png)", "*.png"), ("All files (*.*)", "*.*")]
        self.tmp_file = "content/text_file.png"
        

    def make_square(self, im, min_size=256, fill_color=(0, 0, 0, 0)):
        x, y = im.size
        size = max(min_size, x, y)
        new_im = Image.new('RGBA', (size, size), fill_color)
        new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
        return new_im


    def convert_to_bytes(self, file_or_bytes, resize=None, fill=False):
        if isinstance(file_or_bytes, str):
            img = PIL.Image.open(file_or_bytes)
        else:
            try:
                img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            except Exception as e:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = PIL.Image.open(dataBytesIO)

        cur_width, cur_height = img.size
        if resize:
            new_width, new_height = resize
            scale = min(new_height / cur_height, new_width / cur_width)
            img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
        if fill:
            img = self.make_square(img, self.THUMBNAIL_SIZE[0])
        with io.BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()





    def display_image_window(self, filename):
        try:
            layout = [

            [sg.Button("Save", enable_events=True, size=(10, 1), font='Any 14')],
            [sg.Image(data=self.convert_to_bytes(filename, self.IMAGE_SIZE))],
            ]

            return layout
        except Exception as e:
            print(f'** Display image error **', e)
            return 


    
    def save_image(self):
        try:
            save_filename = sg.popup_get_file("File", file_types=self.file_types, save_as=True, no_window=True)
            shutil.copy(self.tmp_file, save_filename)
            sg.popup(f"Saved!")
        except:
            print("Error saving!")



    def getWindow(self):
        return sg.Window(title="Vizualizer" ,layout = self.display_image_window("content/text_file.png"), modal=True, element_padding=(0,0), resizable=False, finalize=True)
    