"""End-to-end integration tests using raw input text, verifying final output."""
import subprocess
import sys
from decimal import Decimal

from shopping_cart.calculator import CartCalculator
from shopping_cart.parser import InputParser

CASE_A_INPUT = """\
2015.11.11|0.7|電子 //promotion info
\n\
1*ipad:2399.00
1*顯示器:1799.00
12*啤酒:25.00
5*麵包:9.00
\n\
2015.11.11
2016.3.2 1000 200
"""

CASE_B_INPUT = """\
\n\
3*蔬菜:5.98
8*餐巾紙:3.20
\n\
2015.01.01
"""


def _run(text: str) -> Decimal:
    cart = InputParser.parse(text)
    return CartCalculator.calculate(cart)


def test_case_a_produces_3083_60():
    assert _run(CASE_A_INPUT) == Decimal("3083.60")


def test_case_b_produces_43_54():
    assert _run(CASE_B_INPUT) == Decimal("43.54")


def test_case_a_via_main_stdout():
    result = subprocess.run(
        [sys.executable, "-m", "shopping_cart.main"],
        input=CASE_A_INPUT,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "3083.60"


def test_case_b_via_main_stdout():
    result = subprocess.run(
        [sys.executable, "-m", "shopping_cart.main"],
        input=CASE_B_INPUT,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "43.54"
