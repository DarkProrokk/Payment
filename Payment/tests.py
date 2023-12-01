from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Item, Order, Tax, Discount


# Create your tests here.
class DiscountModelTests(TestCase):

    @staticmethod
    def print_info(message):
        print(message)

    def setUp(self):
        print('-' * 30)
        self.print_info('Start setUp')
        self.discount_1 = Discount.objects.create(percent_off=20, discount_hash='123')
        self.discount_2 = Discount.objects.create(percent_off=30, discount_hash='123')
        self.print_info('Finish setUp')

    def test_discount_creation(self):
        self.print_info('test_discount_creation')

        discount_1 = Discount.objects.get(id=self.discount_1.id)
        discount_2 = Discount.objects.get(id=self.discount_2.id)

        self.assertEqual(discount_1.percent_off, 20)
        self.assertEqual(discount_2.percent_off, 30)
        self.assertEqual(Discount.objects.count(), 2)

        self.print_info('Finish test_discount_creation')

    def test_add_discount_in_order(self):
        self.print_info('test_add_discount_in_order')
        order = Order.objects.create(discount=self.discount_1)
        self.assertEqual(self.discount_1.discount_hash, order.discount.discount_hash)
        self.print_info('Finish test_add_discount_in_order')


class TaxModelTests(TestCase):

    @staticmethod
    def print_info(message):
        print(message)

    def setUp(self):
        print('-' * 30)
        self.print_info('Start setUp')
        self.tax_1 = Tax.objects.create(display_name='tax_1', description='description_1', percentage=10,
                                        tax_hash='123', inclusive=False)
        self.tax_2 = Tax.objects.create(display_name='tax_2', description='description_2', percentage=20,
                                        tax_hash='123', inclusive=True)
        self.print_info('Finish setUp')

    def test_task_creation(self):
        self.print_info('test_task_creation')
        self.assertEqual(self.tax_1.display_name, 'tax_1')
        self.assertEqual(self.tax_2.display_name, 'tax_2')
        self.assertEqual(Tax.objects.count(), 2)
        self.print_info('Finish test_task_creation')

    def test_add_tax_in_order(self):
        self.print_info('test_add_tax_in_order')
        order = Order.objects.create(tax=self.tax_1)
        self.assertEqual(self.tax_1.tax_hash, order.tax.tax_hash)
        self.print_info('Finish test_add_tax_in_order')


class ItemModelTests(TestCase):

    @staticmethod
    def print_info(message):
        print(f"{message}")

    def setUp(self):
        print('-' * 30)
        self.print_info('Start setUp')
        self.item_1 = Item.objects.create(name="item_1", price=100, description='description_1')
        Item.objects.create(name="item_2", price=100, description='description_2')
        Item.objects.create(name="item_3", price=100, description='description_3')
        self.item_4 = Item.objects.create(name="item_4", price=100, description='description_1', currency='eur')
        self.print_info('Finish setUp')

    def test_item_creation(self):
        self.print_info('test_item_creation')
        self.assertEqual(self.item_1.name, 'item_1')
        self.assertEqual(self.item_1.price, 100)
        self.print_info('Finish test_item_creation')

    def test_item_get_all_item(self):
        self.print_info('test_item_get_all_item')
        items = Item.objects.all()
        self.assertEqual(items.count(), 4)
        self.print_info('Finish test_item_get_all_item')

    def test_currency_choices(self):
        self.print_info('test_currency_choices')
        choices = ['usd', 'eur']
        self.assertListEqual([choice[0] for choice in Item.CUR], choices)
        self.print_info('Finish test_currency_choices')

    def test_str_representation(self):
        self.print_info('test_str_representation')
        self.assertEqual(str(self.item_1), 'item_1')
        self.print_info('Finish test_str_representation')

    def test_default_currency(self):
        self.print_info('test_str_representation')
        self.assertEqual(self.item_1.currency, 'usd')
        self.print_info('Finish test_default_currency')

    def test_eur_currency(self):
        self.print_info('test_str_representation')
        self.assertEqual(self.item_4.currency, 'eur')
        self.print_info('Finish test_str_representation')


class OrderModelTest(TestCase):

    @staticmethod
    def print_info(message):
        print(f"{message}")

    def setUp(self):
        print('-' * 30)
        self.print_info("Start setUp")
        self.order = Order.objects.create()
        Item.objects.create(name="item_1", price=100, description='description_1')
        Item.objects.create(name="item_2", price=100, description='description_2', currency='eur')
        Item.objects.create(name="item_3", price=100, description='description_2')
        self.print_info("Finish SetUp")

    def test_order_creation(self):
        self.print_info("test_order_creation")
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        self.print_info("Finish test_order_creation")

    def test_add_item_in_order(self):
        self.print_info("test_add_item_in_order")
        self.order.items.add(Item.objects.get(name="item_1"))
        self.order.items.add(Item.objects.get(name="item_3"))
        self.print_info("Finish test_add_item_in_order")

    def test_add_item_with_different_currency(self):
        self.print_info("test_add_item_with_different_currency")
        self.order.items.add(Item.objects.get(name="item_1"))
        with self.assertRaises(ValidationError):
            self.order.items.add(Item.objects.get(name="item_2"))


class TestView(TestCase):

    @staticmethod
    def print_info(message):
        print(f"{message}")

    def setUp(self):
        print('-' * 30)
        self.print_info('Start setUp')
        Item.objects.create(name="item_1", price=100, description='description_1')
        Item.objects.create(name="item_4", price=100, description='description_1', currency='eur')
        Order.objects.create()
        self.print_info('Finish setUp')

    def test_item_view(self):
        self.print_info('test_item_view')
        item_id = Item.objects.first()
        response = self.client.get(f'/payment/item/{item_id.id}/')
        self.assertEqual(response.status_code, 200)
        self.print_info('Finish test_item_view')

    def test_buy_item(self):
        self.print_info('test_buy_item')
        item_id = Item.objects.first()
        response = self.client.get(f'/payment/buy/{item_id.id}/', follow=True)
        self.assertEqual('session_id' in response.content.decode(), True)
        self.print_info('Finish test_buy_item')

    def test_buy_empty_order(self):
        self.print_info('test_buy_order')
        order = Order.objects.first()
        response = self.client.get(f'/payment/order_buy/{order.id}/', follow=True)
        self.assertEqual(response.content.decode(), 'Order cannot be empty. Add Item')
        self.print_info('Finish test_buy_order')
