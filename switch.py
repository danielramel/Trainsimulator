class Switch:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.state = self.b

    def change(self, rails):
        self.state = self.c if self.state == self.b else self.b
        if rails[self.a].next == self.b:
            rails[self.a].next = self.c
            rails[self.c].previous = self.a

        elif rails[self.a].next == self.c:
            rails[self.a].next = self.b
            rails[self.b].previous = self.a

        elif rails[self.a].previous == self.b:
            rails[self.a].previous = self.c
            rails[self.c].next = self.a

        elif rails[self.a].previous == self.c:
            rails[self.a].previous = self.b
            rails[self.b].next = self.a

        else:
            raise ValueError("The Switch is not connected to the Rail it is supposed to change!")
        
    def __repr__(self):
        return f"Switch(a={repr(self.a)}, b={repr(self.b)}, c={repr(self.c)})"