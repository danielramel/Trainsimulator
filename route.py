import pygame

class Route:
    def __init__(self, sp, ep, rails):
        self.sp = sp
        self.ep = ep

        self.direction = sp._x < ep._x

        self.path = self.dfs(sp, ep, rails)

        if len(self.path) == 0:
            self.path = None        

    def dfs(self, sp, ep, rails, route=None):
        if route is None:
            route = []

        if sp == ep:
            return route

        for rail in rails.values():
            if self.direction and rail.a == sp:
                route.append(rail)

                r = self.dfs(rail.b, ep, rails, route)
                if r[-1].b == ep:
                    return r
                else:
                    route.pop()

            elif not self.direction and rail.b == sp:
                route.append(rail)

                r = self.dfs(rail.a, ep, rails, route)
                if r[-1].a == ep:
                    return r
                else:
                    route.pop()
        return route
        
    def set(self, rails, semaphores, switches):
        for i in range(len(self.path)):
            if self.path[i].isLocked:
                for j in range(i-1, -1, -1):
                    rails[self.path[j].name].isLocked = False
                raise ValueError("The route cannot be set, because one of the rails is locked!")
            
            rails[self.path[i].name].isLocked = True

            for switch in switches.values():
                if switch.a == self.path[i].name:

                    if (i < len(self.path)-1 and switch.state != self.path[i+1].name):
                        switch.change(rails)

                        #if change didn't help, it means that the switch is already in the right position, so let's change it back
                        if switch.state != self.path[i+1].name:
                            switch.change(rails)
                        else:
                            continue

                    if (i > 0 and switch.state != self.path[i-1].name):
                        switch.change(rails)

                        #if change didn't help, it means that the switch is already in the right position, so let's change it back
                        if switch.state != self.path[i-1].name:
                            switch.change(rails)
                        continue

    
        if self.direction:
            semaphores[self.path[0].a.name+"R"].set(self.path)
        else:
            semaphores[self.path[0].b.name+"L"].set(self.path)
            
    def __str__(self) -> str:
        for e in self.path:
            s += f"{e.name} -> "

        return s

    def __repr__(self):
        return str(self)