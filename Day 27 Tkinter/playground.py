def add(*args):
    sum = 0
    for n in args: # args is a python tuple
        sum += n
    return sum

# print(add(3,2,41,1))


def calculate(n, **kwargs):
    print(kwargs) # kwargs is a python dictionary
    n += kwargs["add"]
    n *= kwargs["multiply"]
    return n

# print(calculate(12, add=10, multiply=2))


class Car:
    def __init__(self, **kw) -> None:
        self.maker = kw.get("maker")
        self.model = kw.get("model")
        self.color = kw.get("color")

    def __repr__(self) -> str:
        return f"""Car maker: {self.maker}.\nCar model: {self.model}"""

car = Car(maker="Nissan")
print(car)
