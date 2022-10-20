
import subprocess





fileLocation = 'content/text_file.txt'







def inicialization():
    # worker2()
    proc1 = subprocess.Popen("java -jar plantuml.jar -picoweb")
    proc2 = subprocess.Popen(f"python -m plantuml -s http://127.0.0.1:8080/plantuml/png/ {fileLocation}")

        









        
    

            
