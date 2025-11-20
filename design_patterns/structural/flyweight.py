import json
from typing import Dict, List


class Flyweight:
    """
    The Flyweight stores a common portion of the state (also called intrinsic
    state) that belongs to multiple real business entities. The Flyweight
    accepts the rest of the state (extrinsic state, unique for each entity) via
    its method parameters.
    """

    def __init__(self, shared_state: List[str]) -> None:
        self._shared_state = shared_state

    def operation(self, unique_state: List[str]) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f"Flyweight: Displaying shared ({s}) and unique ({u}) state.")


class FlyweightFactory:
    """
    The Flyweight Factory creates and manages the Flyweight objects. It ensures
    that flyweights are shared correctly. When the client requests a flyweight,
    the factory either returns an existing instance or creates a new one, if it
    doesn't exist yet.
    """

    def __init__(self, initial_flyweights: List[List[str]]) -> None:
        self._flyweights: Dict[str, Flyweight] = {}

        for state in initial_flyweights:
            key = self.get_key(state)
            self._flyweights[key] = Flyweight(state)

    def get_key(self, state: List[str]) -> str:
        # FIX: sort the items to always get the same key
        return "_".join(sorted(state))

    def get_flyweight(self, shared_state: List[str]) -> Flyweight:
        key = self.get_key(shared_state)

        if key not in self._flyweights:
            print("FlyweightFactory: Can't find a flyweight, creating new one.")
            self._flyweights[key] = Flyweight(shared_state)
        else:
            print("FlyweightFactory: Reusing existing flyweight.")

        return self._flyweights[key]

    def list_flyweights(self) -> None:
        count = len(self._flyweights)
        print(f"FlyweightFactory: I have {count} flyweights:")
        print("\n".join(self._flyweights.keys()))


def add_car_to_police_database(
    factory: FlyweightFactory,
    plates: str, owner: str,
    brand: str, model: str, color: str
) -> None:
    print("\nClient: Adding a car to database.")

    flyweight = factory.get_flyweight([brand, model, color])

    flyweight.operation([plates, owner])


if __name__ == "__main__":
    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])

    factory.list_flyweights()

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "M5", "red"
    )

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "X1", "red"
    )

    print()
    factory.list_flyweights()
