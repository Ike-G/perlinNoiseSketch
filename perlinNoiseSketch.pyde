
from random import uniform, randint
import math as m 

def genGrid(size) : 
    grid = [[(0,0) for i in range(size)] for j in range(size)]
    grid[0][0] = (uniform(-16,16), uniform(-16,16))
    angle = m.atan2(*grid[0][0])%(2*m.pi)
    mod = m.sqrt(grid[0][0][0]**2+grid[0][0][1]**2)
    last = (angle, mod)
    redist = lambda x : 2*m.exp(-(x/8)**2)
    for i in range(size**2) : 
        delA = uniform(-m.pi/6, m.pi/6)
        delM = uniform(-0.4, 0.4)*last[1]
        last = (delA+last[0], redist(delM+last[1])*(delM+last[1]))
        c = hilbertCurve(size, i)
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
        # Velocity ranges between (x,y) s.t. -m.pi/6 < arctan(-x/y) < m.pi/6
        angle = 0
        mod = 0
        self.vx = mod*m.cos(angle)/100
        self.vy = mod*m.sin(angle)/100
        self.ax, self.ay = 0, 0
        self.xH, self.yH = [self.x], [self.y]
    
    def update(self) :
        fx, fy = 0, 0 
        for i in range(len(self.G)) : 
            for j in range(len(self.G)) :  
                pF = m.exp(-self.proximity(i*self.vDens,j*self.vDens)/8)
                # pF = m.exp(-self.proximity(i,j))
                fx += pF*self.G[i][j][0]/self.vDens
                fy += pF*self.G[i][j][1]/self.vDens
        self.uA(fx, fy)
        self.uV()
        self.uP()

    def rollout(self) : 
        while self.res[0] >= self.x >= 0 and self.res[1] >= self.y >= 0 : 
            self.update()
            line(self.xH[-1], self.yH[-1], self.x, self.y)
            self.xH.append(self.x)
            self.yH.append(self.y)
            #print("Pos: ",self.x, self.y)
            #print("Vel: ", self.vx, self.vy)
            #print("Acc: ", self.ax, self.ay, "\n")

    def uA(self, fx, fy) : 
        self.ax += fx 
        self.ay += fy
    
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


def main(side, pNum, vDens) : 
    G = genGrid(side/vDens)
    for i in range(pNum/4) : 
        P = Projectile(G, (side*(i+1)/(pNum/4), side), vDens) 
        P.rollout()
    print("25% complete")
    for i in range(pNum/4) : 
        P = Projectile(G, (side*(i+1)/(pNum/4), 0), vDens)
        P.rollout()
    print("50% complete")
    for i in range(pNum/4) : 
        P = Projectile(G, (0, side*(i+1)/(pNum/4)), vDens)
        P.rollout()
    print("75% complete")
    for i in range(pNum/4) : 
        P = Projectile(G, (side, side*(i+1)/(pNum/4)), vDens)
        P.rollout()
    print("99% complete")
    
size(1024, 1024)
colorMode(HSB)
background(0, 0, 0)
stroke(130, 255, 255, 100)
#square = createShape(RECT, 0, 0, 50, 50)
#square.setFill(color(0,255,255, 128))
#square.setStroke(False)
#shape(square, 25, 25)
main(1024, 1024, 16)
print("100% complete")
