import pytest

from src.receipt import Receipt
from src.model_objects import Product, SpecialOfferType, ProductUnit
from src.shopping_cart import ShoppingCart
from src.teller import Teller
from tests.fake_catalog import FakeCatalog

catalog: FakeCatalog = FakeCatalog()
toothbrush: Product = Product("toothbrush", ProductUnit.EACH)
catalog.add_product(toothbrush, 0.99)
apples: Product = Product("apples", ProductUnit.KILO)
catalog.add_product(apples, 1.99)
teller: Teller = Teller(catalog)

def test_ten_percent_discount():
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart: ShoppingCart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)
    
    original_toothbrush_price = 2 * 0.99
    toothbrush_price = 2 * 0.99 * 0.9
    toothbrush_discount = 2 * 0.99 * 0.1
    apples_price = 2.5 * 1.99

    assert (apples_price + toothbrush_price) == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 2 == len(receipt.items)

    # Apples
    receipt_item: Receipt = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity
    
    # Toothbrush
    receipt_item_2 = receipt.items[1]
    assert toothbrush == receipt_item_2.product
    assert 0.99 == receipt_item_2.price
    assert original_toothbrush_price == pytest.approx(receipt_item_2.total_price, 0.01)
    assert 2 == receipt_item_2.quantity
    assert -toothbrush_discount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)

def test_three_for_two_offer():
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 3 * 0.99
    discounted_price = 2 * 0.99
    discount_amount = 0.99
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 3 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_three_for_two_offer_with_extra_item():
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 4)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 4 * 0.99
    discounted_price = (2 * 0.99) + 0.99
    discount_amount = original_price - discounted_price
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 4 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_five_for_amount_offer():
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.50)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 5)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 5 * 0.99
    discounted_price = 4.50
    discount_amount = original_price - discounted_price
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 5 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_five_for_amount_offer_with_extra_items():
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.50)
    
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 7)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 7 * 0.99
    discounted_price = 4.50 + (2 * 0.99)
    discount_amount = original_price - discounted_price
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 7 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_two_for_amount_offer():
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.50)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 2 * 0.99
    discounted_price = 1.50
    discount_amount = original_price - discounted_price
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 2 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_two_for_amount_offer_with_extra_item():
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.50)
    
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 3 * 0.99
    discounted_price = 1.50 + 0.99
    discount_amount = original_price - discounted_price
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 3 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)
def test_three_for_two_offer():
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 3 * 0.99
    discounted_price = 2 * 0.99
    discount_amount = 0.99
    
    assert discounted_price == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 3 == receipt_item.quantity
    assert -discount_amount == pytest.approx(receipt.discounts[0].discount_amount, 0.01)

def test_apples_no_discount():
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 2.5 * 1.99
    
    assert original_price == pytest.approx(receipt.total_price(), 0.01)
    assert 0 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity

def test_toothbrush_no_discount():
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = 1 * 0.99
    
    assert original_price == pytest.approx(receipt.total_price(), 0.01)
    assert 0 == len(receipt.discounts)
    assert 1 == len(receipt.items)
    
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert original_price == pytest.approx(receipt_item.total_price, 0.01)
    assert 1 == receipt_item.quantity

def test_apples_and_toothbrush_no_discount():
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 1.75)
    cart.add_item_quantity(toothbrush, 2)
    
    receipt = teller.checks_out_articles_from(cart)
    
    original_price = (1.75 * 1.99) + (2 * 0.99)
    
    assert original_price == pytest.approx(receipt.total_price(), 0.01)
    assert 0 == len(receipt.discounts)
    assert 2 == len(receipt.items)
    
    receipt_item_1 = receipt.items[0]
    assert apples == receipt_item_1.product
    assert 1.99 == receipt_item_1.price
    assert (1.75 * 1.99) == pytest.approx(receipt_item_1.total_price, 0.01)
    assert 1.75 == receipt_item_1.quantity
    
    receipt_item_2 = receipt.items[1]
    assert toothbrush == receipt_item_2.product
    assert 0.99 == receipt_item_2.price
    assert (2 * 0.99) == pytest.approx(receipt_item_2.total_price, 0.01)
    assert 2 == receipt_item_2.quantity
