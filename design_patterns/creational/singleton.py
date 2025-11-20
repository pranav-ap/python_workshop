class SingletonMeta(type):
    # It stores the one and only instance per class.
    _instances = {}

    # called when you do :
    # obj = MyClass()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

    def some_business_logic(self):
        pass


if __name__ == "__main__":
    s1 = Singleton(25)
    s2 = Singleton(30)

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
        print(f"s1 value: {s1.value}")  # 25
        print(f"s2 value: {s2.value}")  # 25
    else:
        print("Singleton failed, variables contain different instances.")
