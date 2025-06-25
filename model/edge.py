from dataclasses import dataclass

from model.product import Product


@dataclass
class Edge:
    p1: Product
    p2: Product
    peso: int

    def __str__(self):
        return f"Arco da {self.p1.Product_number} a {self.p2.Product_number}, peso={self.peso}"

    def __lt__(self, other):
        return self.peso < other.peso
