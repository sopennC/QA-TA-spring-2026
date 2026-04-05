from faker import Faker

fake = Faker()


def random_seller_id() -> int:
    return fake.random_int(min=111111, max=999999)


def random_item_name(prefix: str = "Item") -> str:
    return f"{prefix}_{fake.pystr(min_chars=4, max_chars=8)}"


def random_price(min_val: int = 1, max_val: int = 10000) -> int:
    return fake.random_int(min=min_val, max=max_val)
