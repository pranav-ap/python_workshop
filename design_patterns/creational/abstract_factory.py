from abc import ABC, abstractmethod


class AbstractProductA(ABC):
    @abstractmethod
    def business_logic(self) -> str:
        pass


class ConcreteProductA1(AbstractProductA):
    def business_logic(self) -> str:
        return "The result of the product A1."


class ConcreteProductA2(AbstractProductA):
    def business_logic(self) -> str:
        return "The result of the product A2."


class AbstractProductB(ABC):
    @abstractmethod
    def business_logic(self) -> None:
        pass

    @abstractmethod
    def another_business_logic(self, collaborator: AbstractProductA) -> None:
        pass


class ConcreteProductB1(AbstractProductB):
    def business_logic(self) -> str:
        return "The result of the product B1."

    def another_business_logic(self, collaborator: ConcreteProductA1) -> str:
        result = collaborator.business_logic()
        return f"The result of the B1 collaborating with the ({result})"


class ConcreteProductB2(AbstractProductB):
    def business_logic(self) -> str:
        return "The result of the product B2."

    def another_business_logic(self, collaborator: ConcreteProductB1):
        result = collaborator.business_logic()
        return f"The result of the B2 collaborating with the ({result})"


class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


def client_code(factory: AbstractFactory) -> None:
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f"{product_b.business_logic()}")
    print(f"{product_b.another_business_logic(product_a)}", end="")


if __name__ == "__main__":
    print("Client: Testing client code with the first factory type:")
    client_code(ConcreteFactory1())

    print("\n")

    print("Client: Testing the same client code with the second factory type:")
    client_code(ConcreteFactory2())
