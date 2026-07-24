from backend.app import get_price_for_customer


def test_retail_price_is_used_for_minoristas():
  product = {"retail_price": 100.0, "wholesale_price": 80.0}
  assert get_price_for_customer(product, "retail") == 100.0


def test_wholesale_price_is_used_for_mayoristas():
  product = {"retail_price": 100.0, "wholesale_price": 80.0}
  assert get_price_for_customer(product, "wholesale") == 80.0
