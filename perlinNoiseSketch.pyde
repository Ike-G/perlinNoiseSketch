
from random import uniform, randint
import math as m 

def genGrid(s) : 
    grid = [[(0,0) for i in range(s)] for j in range(s)]
    grid[0][0] = (uniform(-16,16), uniform(-16,16))
    angle = m.atan2(*grid[0][0])%(2*m.pi)
    mod = m.sqrt(grid[0][0][0]**2+grid[0][0][1]**2)
    last = (angle, mod)
    redist = lambda x : 2*m.exp(-(x/8)**2)
    for i in range(s**2) : 
        delA = uniform(-m.pi/4, m.pi/4)
        delM = uniform(-0.6, 0.6)*last[1]
        last = (delA+last[0], redist(delM+last[1])*(delM+last[1]))
        c = hilbertCurve(s, i)
        grid[c[0]][c[1]] = (last[1]*m.cos(last[0]), last[1]*m.sin(last[0]))
    return grid

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


class Projectile : 
    # Assume a mass of 1, so F = a 
    def __init__(self, grid, start, vDens) : 
        self.res = ((len(grid)+1)*vDens, (len(grid)+1)*vDens) # Image is scaled up by 8
        self.vDens = vDens
        self.G = grid 
        self.x = start[0]
        self.y = start[1]
        self.vx, self.vy = 0, 0 
        self.ax, self.ay = 0, 0
        self.xH, self.yH = [self.x], [self.y]
    
    def update(self) :
        fx, fy = 0, 0 
        for i in range(len(self.G)) : 
            for j in range(len(self.G)) :  
                pF = m.exp(-self.proximity(i*self.vDens,j*self.vDens)/(m.log(self.vDens)*4))
                fx += pF*self.G[i][j][0]/self.vDens
                fy += pF*self.G[i][j][1]/self.vDens
        self.uA(fx, fy)
        self.uV()
        self.uP()

    def rollout(self) : 
        while self.res[0] >= self.x >= 0 and self.res[1] >= self.y >= 0 : 
            self.update()
            #line(self.xH[-1], self.yH[-1], self.x, self.y)
            self.xH.append(self.x)
            self.yH.append(self.y)
            #print("Pos: ",self.x, self.y)
            #print("Vel: ", self.vx, self.vy)
            #print("Acc: ", self.ax, self.ay, "\n")

    def uA(self, fx, fy) : 
        self.ax += fx 
        self.ay += fy
        self.ax, self.ay = self.ax*0.95, self.ay*0.95
    
    def uV(self) : 
        self.vx += self.ax 
        self.vy += self.ay 
    
    def uP(self) : 
        self.x += self.vx 
        self.y += self.vy 

    def proximity(self, cx, cy) : 
        return m.sqrt((self.x-cx)**2+(self.y-cy)**2)

    def grad(self) : 
        il = self.xH[0]
        jl = self.yH[0]
        g = []
        for i,j in zip(self.xH[1:], self.yH[1:]) : 
            g.append((j-jl)/(i-il))
        return g

    def gradTwo(self, grad) : 
        try : 
            il = self.xH[0]
            jl = grad[0]
            gTwo = []
            for i,j in zip(self.xH[1:], grad[1:]) : 
                gTwo.append((j-jl)/(i-il))
            return gTwo
        except : 
            return 0 

def clockwiseRotation(s,v) : 
    grid = [[[] for i in range(int(s/v))] for j in range(int(s/v))]
    for i in range(int(s/v)) : 
        for j in range(int(s/v)) : 
            angle = m.atan((j+1)/(i+1))-m.pi/2
            mag = 16/m.sqrt((j+1)**2+(i+1)**2)
            grid[i][j] = (mag*m.cos(angle), mag*m.sin(angle))
    return grid

def counterClockwise(s,v) : 
    grid = [[[] for i in range(int(s/v))] for j in range(int(s/v))]
    for i in range(int(s/v)) : 
        for j in range(int(s/v)) : 
            angle = m.atan((j+1)/(i+1))+m.pi/2
            mag = 16/m.sqrt((j+1)**2+(i+1)**2)
            grid[i][j] = (mag*m.cos(angle), mag*m.sin(angle))
    return grid

def fullCircle(s,v) : 
    grid = [[[] for i in range(int(s/v))] for j in range(int(s/v))]
    for i in range(int(s/v)) : 
        for j in range(int(s/v)) : 
            angle = m.atan((j-3.5)/(i-3.5))+m.pi/2
            angle *= abs(angle)
            mag = 2/(3.5-i)
            grid[i][j] = (mag*m.cos(angle), mag*m.sin(angle))
    return grid

def main(side, pNum, vDens, *cs) : 
    #G = counterClockwise(side,vDens)
    G = genGrid(side/vDens)
    #G = fullCircle(side,vDens)
    print("Finished grid")
    noFill()
    stroke(cs[0], 255, 255, 100)
    for i in range(pNum/4) : 
        P = Projectile(G, (side*(i+1)/(pNum/4), side), vDens) 
        P.rollout()
        beginShape()
        for i in range(len(P.xH)) : 
            curveVertex(P.xH[i], P.yH[i])
        endShape()
    print("25% complete")
    stroke(cs[-1], 255, 255, 100)
    for i in range(pNum/4) : 
        P = Projectile(G, (side*(i+1)/(pNum/4), 0), vDens)
        P.rollout()
        beginShape()
        for i in range(len(P.xH)) : 
            curveVertex(P.xH[i], P.yH[i])
        endShape()
    print("50% complete")
    stroke(cs[0], 255, 255, 100)
    for i in range(pNum/4) : 
        P = Projectile(G, (0, side*(i+1)/(pNum/4)), vDens)
        P.rollout()
        beginShape()
        for i in range(len(P.xH)) : 
            curveVertex(P.xH[i], P.yH[i])
        endShape()
    print("75% complete")
    stroke(cs[-1], 255, 255, 100)
    for i in range(pNum/4) : 
        P = Projectile(G, (side, side*(i+1)/(pNum/4)), vDens)
        P.rollout()
        beginShape()
        for i in range(len(P.xH)) : 
            curveVertex(P.xH[i], P.yH[i])
        endShape()
    out = createWriter("lastField.txt")
    for i in G : 
        out.print(str(i)+",")
    out.flush()
    out.close()
    print("99% complete")
    
    
sideLength = 1024
projectileNumber = 1024
vectorDensity = 128 
size(1024, 1024)
colorMode(HSB)

cs = [0, 51, 130, 212, 225]
for i in cs :
    #for j in cs : 
    clear()
    background(0,0,0)
    main(sideLength, projectileNumber, vectorDensity, i)
    fn = str(i)+"-v6.png"
    save(fn)


print("100% complete")

# Colours to check 
# - 130 255 255 100 - Blue 
# - 85 255 255 100 - Green
# - 212 255 255 100 - Magenta
# - 0 255 255 100 - Red
# - 51 255 255 100 - Yellow
# - 225 255 255 100 - Pink
# - 21 255 255 50 - Orange
