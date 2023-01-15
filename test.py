class A:
    def __init__(self):
        self.a = 0


InsA = A()
for _ in range(200):
    print(InsA.a)
