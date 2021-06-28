import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
#import niceplots
import csv
fontSize=20
lineWidth=2
plt.rc('font',family='Times New Roman',size=fontSize) 
plt.rc('axes',linewidth=lineWidth-1,edgecolor='k')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'
CFDCp = []
CFDXC = []
with open('data0.csv', 'rb') as csvfile:
    counter = 0
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        cols = [x.strip() for x in row[0].split(',')]
        if counter ==0:
            for idxI,col in enumerate(cols):
                if 'Cp' in col:
                    cpCol = idxI
                if 'X/C' in col:
                    xcCol = idxI
            print cpCol,xcCol
        else:
            CFDCp.append(-float(cols[cpCol]))
            CFDXC.append(float(cols[xcCol]))
        counter +=1

f=open('adflow.dat','r')
lines=f.readlines()
f.close()

ADflowCp=[]
ADflowXC=[]
for idxI,line in enumerate(lines):
    if idxI>4:
        cols = line.split()
        ADflowCp.append(-float(cols[9]))
        ADflowXC.append(float(cols[3]))

EXPCp = []
EXPXC = []
f1 = open('exp.txt','r')
lines = f1.readlines()
for line in lines: 
    cols  = line.split()
    EXPXC.append( float(cols[0]))
    EXPCp.append( float(cols[1]))
f1.close()


plt.plot(EXPXC,EXPCp,'ko',label='Experiment')
plt.plot(CFDXC,CFDCp,'-r',      label="OpenFOAM, $C_D$: 0.01324, $C_L$: 0.6647")
plt.plot(ADflowXC,ADflowCp,'-b',label='ADflow,        $C_D$: 0.01275, $C_L$: 0.6770')
plt.tight_layout()
plt.xlim([-0.01,1.01])
plt.xlabel("$x/c$",fontsize=fontSize)
plt.ylabel("$C_p$",fontsize=fontSize)
plt.legend(frameon=False,prop={'size':16},loc=0,numpoints=1)
plt.savefig('fig',bbox_inches='tight')   # save the figure to file
