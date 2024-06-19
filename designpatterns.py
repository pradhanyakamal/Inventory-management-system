from datetime import datetime
# Singleton Pattern for Inventory
class Inventory:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Inventory, cls).__new__(cls)
            cls._instance.stock = []
        return cls._instance 

    def __iter__(self):
        return len(cls._instance.stock)+1

    def add_item(self, item):

        self.stock.append(item)






# Iterator Pattern for Auto-incrementing Item IDs
class ItemIDIterator:
    def __init__(self):
        self.current_id = 6

    def get_next_id(self):
        next_id = self.current_id
        self.current_id += 1
        return next_id



# Strategy Pattern for Discount Calculation
class DiscountStrategy:
    def calculate_discount(self, total_amount):
        pass

class Strategy1(DiscountStrategy):
    def calculate_discount(self, total_amount):
        return total_amount *0.2  #20% discount

class Strategy2(DiscountStrategy):
    def calculate_discount(self, total_amount):
        return total_amount *0.3  #30% discount
        
class Strategy3(DiscountStrategy):
    def calculate_discount(self, total_amount):
        return total_amount *0.3  #30% discount

class Observer:
    def update(self):
        pass

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

class PaymentObserver(Observer):
    def update(self):
        print("Payment successful. Thank you!")

class Invoice(Observable):
    def __init__(self):
        self.items = []
        # Get the current date
        current_date = datetime.now()
        current_month = current_date.month

        if current_month in [1,4,7,10]:
            self.discount_strategy = Strategy1()

        elif current_month in [2,5,8,11]:
            self.discount_strategy = Strategy2()

        else:
            self.discount_strategy = Strategy3()

    def add_item(self, item):
        self.items.append(item)

    def delete_item(self, item):
        self.items.remove(item)

    def calculate_total_amount(self):
        return sum(item['price'] for item in self.items)

    def calculate_discount(self):
        return self.discount_strategy.calculate_discount(self.calculate_total_amount())

    def generate_invoice(self):
        total_amount = self.calculate_total_amount()
        discount = self.calculate_discount()
        final_amount = total_amount - discount
        return {
            'items': self.items,
            'total_amount': total_amount,
            'discount': discount,
            'final_amount': final_amount
        }

       