"""
    Transform a CSV file with the following format
    category;col1;col2;col3;col4
    cat1;1;1;1;2
    cat2;2;2;2;2
    ...
    catn;n;n;n;n
    into a tikz graph

    Author: Symeon Malengreau
    Version: 0.1.1
"""

import sys
import random

CONSTANT_SIZE_X = 15.0
CONSTANT_SIZE_Y = 10.0

COLORS = ['red', 'green', 'blue', 'cyan','magenta', 'yellow', 'darkgray', 'brown', 'lime', 'olive', 'orange', 'pink', 'purple', 'teal', 'violet']

def readCSV(path) :
    f = open(path, 'r')
    h = f.readline().split(";")
    out = []
    for i in range(len(h)) :
        out.append([])
    for line in f :
        tmp = line.split(';')
        for i in range(len(tmp)):
            if tmp[i] != '' :
                out[i].append(int(tmp[i]))
            else :
                out[i].append(0)
    f.close()
    colors = []
    for i in range(len(out)-1):
        if len(COLORS) > 0 :
            r = random.randint(1,len(COLORS))    
            color = COLORS[r-1]
            COLORS.remove(color)
            colors.append(color)
        else :
            colors.append('black')
    return {'head':h, 'data':out, 'colors':colors}

def writeCategory(f, category) :
    # Print category
    f.write('% Category\n')
    numCategory = len(category)
    f.write('\\node at (0,-0.5) {0};\n')
    f.write('\\draw(0,0) -- (0,-0.1);\n')
    for i in range(numCategory) :
        pos = str((i+1) * CONSTANT_SIZE_X/numCategory)
        f.write('\\draw(' + pos +',0) -- ('+ pos + ',-0.1);\n')
        f.write('\\node at (' + pos + ',-0.5) {' + str(category[i]) + '};\n')

def writeAxis(f, values, minVal, maxVal, color) :
    numCategory = len(values)
    spacing = (abs(minVal) + maxVal)/CONSTANT_SIZE_Y
    f.write('% Axis\n')
    f.write('\\draw[' + color + ',line width=0.25mm] (0,0) -- (' + str(1 * CONSTANT_SIZE_X/numCategory) + ',' + str(values[0]/spacing) + ');\n');
    for i in range(numCategory-1) :
        f.write('\\draw[' + color + ',line width=0.25mm] (' + str((i+1) * CONSTANT_SIZE_X/numCategory) + ',' + str(values[i]/spacing) + ') -- (' + str((i+2) * CONSTANT_SIZE_X/numCategory) + ',' + str(values[i+1]/spacing) + ');\n');

def writeValue(f, minVal, maxVal) :
    spacing = int((abs(minVal) + maxVal)/CONSTANT_SIZE_Y)
    f.write('% Value\n')
    for i in range(int(CONSTANT_SIZE_Y)+1) :
        f.write('\\draw(-0.1,' + str(i) + ') -- (0,' + str(i) + ');\n')
        f.write('\\node at (-0.6, ' +str(i) +') {' + str(minVal+spacing*i) + '};\n')

def writeLegend(f, colors, head) :
    for i in range(len(colors)) :
        f.write('\\draw[' + colors[i] + ', line width=0.25mm](17,' + str(i*0.4+2) + ') -- (18,' + str(i*0.4+2) + ');\n')
        f.write('\\node at (19,' + str(i*0.4+2) + ') {' + head[i+1] + '};\n')    
    

def writeData(f, data) :
    # Write category
    writeCategory(f, data['data'][0])
    minVal = sys.maxint
    maxVal = -sys.maxint - 1
    for i in range(len(data['data'])-1) :
        for val in data['data'][i+1] :
            if val < minVal :
                minVal = val
            if val > maxVal :
                maxVal = val

    # Write Value
    if minVal >= 0 :
        minVal = 0
        
    writeValue(f, minVal, maxVal)
    
    # Write Axis
    for i in range(len(data['data'])-1) :
        writeAxis(f, data['data'][i+1], minVal, maxVal, data['colors'][i])

    writeLegend(f, data['colors'], data['head'])
    
def createTikz(path, data) :
    f = open(path, 'w')
    f.write('\\begin{tikzpicture}[scale=1.0]\n')
    f.write('% NAME TO REPLACE\n')
    f.write('\\node at (-0.2,11.2) {\\textit{Axis y}};\n')
    f.write('\\node at (16.8,0) {\\textit{Axis x}};\n')
    f.write('%\\Large\n%\\node at (10,12) {\\textbf{Main Title}};\n%\\normalsize\n')
    f.write('% GRAPH\n')
    f.write('\\draw[step=0.25,black!8,very thin] (0,0) grid (15.5,10.5);\n')
    f.write('\\draw[->](0,0) -- (15.8, 0);\n')
    f.write('\\draw[->](0,0) -- (0, 10.8);\n')
    writeData(f, data)
    f.write('\\end{tikzpicture}')
    f.close()


inFile = raw_input('Enter input .csv file: ')
outFile = raw_input('Enter output .tex file: ')
out = readCSV(inFile)
createTikz(outFile, out)
      
        
