import sys

from shopping_cart.calculator import CartCalculator
from shopping_cart.parser import InputParser


def main() -> None:
    text = sys.stdin.read()
    cart = InputParser.parse(text)
    result = CartCalculator.calculate(cart)
    print(f"{result:.2f}")


if __name__ == "__main__":
    main()
