"""
import os
from alive_progress import alive_bar
import glob
import re
import subprocess
import time
from tqdm import tqdm
bestscore=0

good_files=[] #Array of file names that meet RoF and/or bioavailability
file_count=len(glob.glob1('.\sdfs',"*"))

#Writing out the explicitly good files
with open("Rule_of_Five.txt", 'w') as ofile:
    for out_line in good_files:
        ofile.write(out_line+',')
    ofile.close()
print (len((good_files)))

for file in tqdm(good_files):
    bar()
    stri=""
    current_ligand=file.removeprefix('structures_')
    current_ligand=current_ligand[:-4]+'.pdb'
    if os.path.exists('minimized2/'+current_ligand) == True:
        continue
    #first need to create the script
   
    time.sleep(0.2)

time.sleep(10)
for file in good_files:
    file=file.removeprefix("structures_")
    file=file[:-4]+'.pdb'
    command = "obabel -i pdb minimized2\\"+file+" -o pdbqt -O converted2\\"+file[:-4]+".pdbqt"
    #obabel -i pdb minimized/structures_44.pdb -o pdbqt -O converted/structures_44.pdbqt
    #p=subprocess.run(command)
    p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
"""

import concurrent.futures
import math
import os
from alive_progress import alive_bar
import glob
import re
import subprocess
import time
from time import sleep, perf_counter
import random
from tqdm import tqdm

good_files=[] #Array of file names that meet RoF and/or bioavailability
file_count=len(glob.glob1('.',"*.sdf"))#here
if(os.path.exists('./minimized') == 0):
        os.makedirs('./minimized')
if(os.path.exists('./scratch') == 0):
        os.makedirs('./scratch')
def total_files():
    with alive_bar(file_count, stats=True, calibrate=10, title='Reading Files') as bar:
        for file in os.listdir('.'):#here
            if file.endswith('.sdf'):
                good_files.append(file)
            bar()

def dock(current_ligand):
    filename='.\\scratch\\'+current_ligand+'.py'
    with open(filename, "w") as ofile:
        ofile.write('import pymol\n')
        ofile.write('cmd.load("'+current_ligand+'")\n')#here
        ofile.write('cmd.remove("hydrogens")\n')
        ofile.write('cmd.h_add()\n')
        ofile.write('cmd.clean(\"all\")\n')
        ofile.write('cmd.select(\"all\")\n')
        ofile.write('x=cmd.get_coords(\"all\")[0][0]\n')
        ofile.write('y=cmd.get_coords(\"all\")[0][1]\n')
        ofile.write('z=cmd.get_coords(\"all\")[0][2]\n')
        ofile.write('mvec=[-float(x), -float(y), -float(z)]\n')
        ofile.write('cmd.translate(mvec)\n')
        file2=current_ligand.removeprefix('structures_')
        stri='minimized\\\\'+file2[:-4]+'.pdb'#here
        ofile.write('cmd.save(\"'+stri+'\")\n')
    command ="C:\ProgramData\pymol\PyMOLWin.exe -qc "+filename
   # print (command)
    p=subprocess.run(command)
    sleep(1)

def total_files():
    for file in os.listdir('.'):
        if file.endswith('.sdf'):
            good_files.append(file)

def clean_scratch():
    for file in os.listdir('.\scratch'):
        os.remove('./scratch/'+file)

def main():
    #First find out which files need to be run still
    total_files()
    start_time = perf_counter()
    with alive_bar(file_count, stats=True, calibrate=10, title='Energy Minimizing') as bar2:
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            for file in zip(good_files, executor.map(dock, good_files)):
                bar2()
    end_time = perf_counter()
    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
    clean_scratch()


if __name__ == '__main__':
    main()
