from dataclasses import dataclass

from shopping_cart.domain.category import Category


@dataclass(frozen=True)
class Product:
    name: str
    category: Category


CATALOG: dict[str, Product] = {
    # Electronics
    "ipad":        Product("ipad",        Category.ELECTRONICS),
    "iphone":      Product("iphone",      Category.ELECTRONICS),
    "monitor":     Product("monitor",     Category.ELECTRONICS),
    "laptop":      Product("laptop",      Category.ELECTRONICS),
    "keyboard":    Product("keyboard",    Category.ELECTRONICS),
    # Food
    "bread":       Product("bread",       Category.FOOD),
    "biscuit":     Product("biscuit",     Category.FOOD),
    "cake":        Product("cake",        Category.FOOD),
    "beef":        Product("beef",        Category.FOOD),
    "fish":        Product("fish",        Category.FOOD),
    "vegetable":   Product("vegetable",   Category.FOOD),
    # Daily
    "napkin":      Product("napkin",      Category.DAILY),
    "storage-box": Product("storage-box", Category.DAILY),
    "coffee-cup":  Product("coffee-cup",  Category.DAILY),
    "umbrella":    Product("umbrella",    Category.DAILY),
    # Alcohol
    "beer":        Product("beer",        Category.ALCOHOL),
    "baijiu":      Product("baijiu",      Category.ALCOHOL),
    "vodka":       Product("vodka",       Category.ALCOHOL),
}

# Maps Chinese input tokens (from stdin) to CATALOG keys.
# Chinese string literals here represent the external input format specification.
INPUT_NAME_MAP: dict[str, str] = {
    "ipad":    "ipad",
    "iphone":  "iphone",
    "顯示器":   "monitor",
    "筆記型電腦": "laptop",
    "鍵盤":    "keyboard",
    "麵包":    "bread",
    "餅乾":    "biscuit",
    "蛋糕":    "cake",
    "牛肉":    "beef",
    "魚":      "fish",
    "蔬菜":    "vegetable",
    "餐巾紙":  "napkin",
    "收納箱":  "storage-box",
    "咖啡杯":  "coffee-cup",
    "雨傘":    "umbrella",
    "啤酒":    "beer",
    "白酒":    "baijiu",
    "伏特加":  "vodka",
}

# Maps Chinese category tokens (from promotion lines) to Category enum.
INPUT_CATEGORY_MAP: dict[str, Category] = {
    "電子":   Category.ELECTRONICS,
    "食品":   Category.FOOD,
    "日用品": Category.DAILY,
    "酒類":   Category.ALCOHOL,
}
