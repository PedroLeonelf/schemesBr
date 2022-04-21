import os
import multiprocessing
import time



NUMBER_OF_SESSIONS = 2
fileLocation = 'content/text_file.txt'
 
def worker():
    os.system("java -jar plantuml.jar -picoweb")


def worker2():
    os.system(f"python -m plantuml -s http://127.0.0.1:8080/plantuml/png/ {fileLocation}")






def inicialization():
    jobs = []
    for i in range( NUMBER_OF_SESSIONS ):
        p = multiprocessing.Process(target=worker)
        
        g = multiprocessing.Process(target=worker2)
    
        jobs.append(p)
        p.start()
        g.start()
        time.sleep(1)
        g.kill()
        p.kill()

        









        
    

            
