import matplotlib.pyplot as plt
import math as m 

def visualise(side, vDens, raw) : 
    vField = raw
    plt.plot([0,side],[0,side], 'w')
    maxX = vField[0][0][0]
    maxY = vField[0][0][1]
    for i in range(int(side/vDens)) : 
        for j in range(int(side/vDens)) : 
            plt.arrow(i*vDens, j*vDens, 8*vField[i][j][0], 8*vField[i][j][1], color='red', head_width=8)
            maxX = vField[i][j][0] if abs(vField[i][j][0])>abs(maxX) else maxX
            maxY = vField[i][j][1] if abs(vField[i][j][1])>abs(maxY) else maxY
            print(vField[i][j])
            print(i,j)
            print("\n")
    print(maxX, maxY)
    plt.show()

def hilbertCurve(n, d) : 
    s = 1 
    x, y = 0, 0 
    while s < n :
        rx = 1&(d>>1) 
        ry = 1&(d^rx)
        if not ry : 
            if rx : 
                x, y = s-1-x, s-1-y
            temp = x
            x = y 
            y = temp
        x += s*rx
        y += s*ry 
        d >>= 2
        s <<= 1
    return (x, y)

def clockwiseRotation() : 
    grid = [[[] for i in range(8)] for j in range(8)]
    for i in range(8) : 
        for j in range(8) : 
            angle = m.atan((j+1)/(i+1))-m.pi/2
            mag = 7/m.sqrt((j+1)**2+(i+1)**2)
            grid[i][j] = (mag*m.cos(angle), mag*m.sin(angle))
    return grid

def fullCircle(s,v) : 
    grid = [[[] for i in range(int(s/v))] for j in range(int(s/v))]
    for i in range(int(s/v)) : 
        for j in range(int(s/v)) : 
            angle = m.atan((j-3.5)/(i-3.5))+m.pi/2
            angle *= abs(angle)
            mag = 8/(3.5-i)
            grid[i][j] = (mag*m.cos(angle), mag*m.sin(angle))
    return grid


