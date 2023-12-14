import subprocess
import os
from time import sleep


for file in os.listdir('.\\minimized'):
    command = "obabel -i pdb minimized\\"+file+" -o pdbqt -O ligands\\"+file[:-4]+".pdbqt"
    p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    

        
