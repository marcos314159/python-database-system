import re
import sys
import json


class Client():
    # Class-level list to store all registered client instances
    client_instances = []

    def __init__(self, email, name, address, city, country, id=None, active=True, register=True):
        """
        Initialize a Client object.

        If register=True, the instance is stored.
        If id is not provided, it is generated from JSON data.
        """

        # Only store instance if explicitly intended
        if register:
            Client.client_instances.append(self)

        self.id = id
        if not self.id:
            self.set_id()

        # Attribute assignments (email uses validation)
        self.email = email
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        self.active = active

    @classmethod
    def get_all_instances(cls):
        """Return all registered Client instances."""
        return cls.client_instances

    def __str__(self):
        """Readable string representation of a Client."""
        return (
            f"ID: {self.id};"
            f"\nE-mail: {self.email};"
            f"\nName: {self.name};"
            f"\nAddress: {self.address};"
            f"\nCity: {self.city};"
            f"\nCountry: {self.country};"
            f"\nActive: {self.activity_status()}"
        )

    def set_id(self):
        """Generate a new ID based on the last client in the JSON file."""
        with open("data.json", "r") as file:
            data = json.load(file)
            last_client = data["Clients"][-1]
            self.id = last_client["id"] + 1

    def activity_status(self):
        """Return human-readable activity status."""
        return "yes" if self.active else "no"

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        """Validate email format before assignment."""
        if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            sys.exit("Invalid email")
        self._email = email


class Product():
    # Class-level list to store all registered product instances
    product_instances = []

    def __init__(self, name, category, price, cost_price, weight, dimensions, brand,
                 color=None, stock=0, sales=0, id=None, active=True, register=True):
        """
        Initialize a Product object.

        If register=True, the instance is stored.
        If id is not provided, it is generated from JSON data.
        """

        if register:
            Product.product_instances.append(self)

        self.id = id
        if not self.id:
            self.set_id()

        # Attribute assignments (some validated through setters)
        self.name = name
        self.category = category
        self.price = price
        self.cost_price = cost_price
        self.weight = weight
        self.dimensions = dimensions
        self.brand = brand
        self.color = color
        self.stock = stock
        self.sales = sales
        self.active = active

    @classmethod
    def get_all_instances(cls):
        """Return all registered Product instances."""
        return cls.product_instances

    def __str__(self):
        """Readable string representation of a Product."""
        return (
            f"ID: {self.id};"
            f"\nName: {self.name};"
            f"\nCategory: {self.category};"
            f"\nPrice: {self.price};"
            f"\nCost price: {self.cost_price};"
            f"\nWeight: {self.weight};"
            f"\nDimensions: {self.dimensions};"
            f"\nBrand: {self.brand};"
            f"\nStock: {self.stock};"
            f"\nSales: {self.sales};"
            f"\nActive: {self.activity_status()}"
        )

    def set_id(self):
        """Generate a new ID based on the last product in the JSON file."""
        with open("data.json", "r") as file:
            data = json.load(file)
            last_product = data["Products"][-1]
            self.id = last_product["id"] + 1

    def activity_status(self):
        """Return human-readable activity status."""
        return "yes" if self.active else "no"

    # --- Update methods (used in input handling) ---

    def update_price(self, new_price):
        self.price += new_price

    def update_cost_price(self, new_cost_price):
        self.cost_price += new_cost_price

    def update_stock(self, new_stock):
        self.stock += new_stock

    def update_sales(self, new_sales):
        self.sales += new_sales

    # --- Validation using property setters ---

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        """Ensure category is within allowed values."""
        if category not in [
            "Electronics", "Clothing", "Home & Kitchen", "Furniture",
            "Tools & Hardware", "Beauty & Personal Care",
            "Health & Wellness", "Sports & Outdoors", "Toys & Games"
        ]:
            sys.exit("Category not found")
        self._category = category

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        """Ensure price is numeric."""
        if not isinstance(price, (int, float)):
            sys.exit("Invalid price")
        self._price = price

    @property
    def cost_price(self):
        return self._cost_price

    @cost_price.setter
    def cost_price(self, cost_price):
        """Ensure cost price is numeric."""
        if not isinstance(cost_price, (int, float)):
            sys.exit("Invalid cost price")
        self._cost_price = cost_price
