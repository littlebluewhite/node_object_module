class A:
    def __init__(self, a):
        self.a = a

    def aa(self):
        return self.a


class B:
    def __init__(self, b):
        self.b = b

    def bb(self):
        return self.b


class C(A, B):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        A.__init__(self, a)
        B.__init__(self, b)

    def ca(self):
        return A.aa(self)

    def cb(self):
        return B.bb(self)


if __name__ == "__main__":
    i = C(1, 2)
    r = A(5)
    print(i.ca())
    print(i.cb())
