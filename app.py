'''Author : Pradhanya K
Roll no : 3122225002701'''

'''Online Store Management System'''


from flask import Flask, render_template, request, redirect

from designpatterns import Inventory, ItemIDIterator
from designpatterns import DiscountStrategy, Strategy1, Strategy2, Strategy3
from designpatterns import Observer, Observable, PaymentObserver, Invoice

from abc import ABC, abstractmethod
from datetime import datetime
import json
import re

app = Flask(__name__)


#instatiation 
inventory1 = Inventory()
inventory2 = Inventory()

class Product:
    def __init__(self, pid, name, quantity, price):
        self.id = pid
        self.name = name
        self.quantity = quantity
        self.price = price

    def add_item(self):
        inventory1.stock.append({'id': self.id, 'name': self.name, 'quantity': self.quantity, 'price': self.price})

# Read data from JSON file
with open('products.json', 'r') as file:
    products_data = json.load(file)

# Create Product objects and add them to inventory
for product_data in products_data:
    product = Product(product_data['id'], product_data['name'], product_data['quantity'], product_data['price'])
    product.add_item()

item_id_iterator = ItemIDIterator()

# Command Pattern: Command Interface
class Command:
    def execute(self):
        pass

# Concrete Command: AddItemCommand
class AddItemCommand(Command):
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def execute(self):
        new_item = {'id': self.item_id, 'name': self.name, 'quantity': self.quantity, 'price': self.price}
        inventory1.stock.append(new_item)

# Invoker: CommandInvoker
class CommandInvoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()
        self.commands = []  # Clear the executed commands



observable = Observable()
payment_observer = PaymentObserver()
observable.add_observer(payment_observer)




invoice = Invoice()





# Create a CommandInvoker instance
command_invoker = CommandInvoker()



#cart class
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items

# Instantiate the Cart
cart = Cart()

# Template Method Pattern: Abstract Class for Report Generation
class ReportGenerationTemplate(ABC):
    def generate_report(self,inventory1):
        self.display_header()
        self.collect_data()
        data = self.format_data()
        return data

    def display_header(self):
        print("Generating Report...")

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def format_data(self):
        pass

    def display_footer(self):
        print("Report generation complete.")

# Concrete Template: AvailableItemsReport
class AvailableItemsReport(ReportGenerationTemplate):
    def collect_data(self):
        self.items = inventory1.stock

    def format_data(self):
        report_data = []
        print("Available Items Report:")
        for item in self.items:
            report_data.append(item)
        return report_data

# payment_observer.update()

# Flask Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    pattern = "^[a-zA-Z0-9#\$@\%\*&]{8,20}$"
    match = re.search(pattern, password)

    if username == 'admin' and match:
        return render_template('admin_dashboard.html')
    elif username == 'storemanager' and match:
        return render_template('store_manager_dashboard.html')
    else:
        return render_template('login.html', error='Invalid credentials')



@app.route('/admin/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_id = item_id_iterator.get_next_id()
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        # Create a command for adding the item
        add_item_command = AddItemCommand(item_id, name, quantity, price)

        command_invoker.add_command(add_item_command)
        command_invoker.execute_commands()
        

        return render_template('admin_dashboard.html', message='Item added successfully')

    return render_template('add_item.html')

@app.route('/admin/delete_item', methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        for item in inventory1.stock:
            if item['id'] == item_id:
                inventory1.stock.remove(item)
                return render_template('admin_dashboard.html', message='Item deleted successfully')

        return render_template('admin_dashboard.html', error='Item not found')

    return render_template('delete_item.html')

@app.route('/admin/show_available_items')
def show_available_items():
    return render_template('available_items.html', items=inventory2.stock)

# Flask Route for Admin Generate Page
@app.route('/admin/generate', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        report_type = request.form.get('report_type')

        # Assuming 'inventory' is an instance of the Inventory class
        inventory_instance = Inventory()

        if report_type == 'available_items':
            report_generator = AvailableItemsReport()
            report_result = report_generator.generate_report(inventory_instance)

            return render_template('display_records.html',records = report_result)

    return render_template('generate_report.html')



@app.route('/store_manager/show_available_items')
def show_available_items_store():
    return render_template('available_items.html', items=inventory1.stock)

@app.route('/store_manager/add_item_to_cart', methods=['GET','POST'])
def add_item_to_cart():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantity = int(request.form['quantity'])

        for item in inventory1.stock:
            if item['id'] == item_id:
                price = item['price']
                new_price = quantity * price
                name = item['name']
                cart.add_item({'item_id':item_id,'name':name,'quantity':quantity,'price':new_price})
                invoice.add_item({'item_id':item_id,'name':name,'quantity':quantity,'price':new_price})
                
        return render_template('store_manager_dashboard.html', message='Item added to cart successfully')

    return render_template('add_item_to_cart.html')

@app.route('/store_manager/delete_item', methods=['GET', 'POST'])
def delete_item_store():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        
        # Check if the item with the given ID exists in the inventory
        for item in cart.get_items():
            if item['item_id'] == item_id:
                cart.remove_item(item)
                invoice.delete_item(item)
                
        return render_template('store_manager_dashboard.html')


    return render_template('delete_item_store.html')

@app.route('/store_manager/show_cart',methods=['GET','POST'])
def show_cart():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantity = int(request.form['quantity'])

        for item in inventory1.stock:
            if item['id'] == item_id:
                price = item['price']
                new_price = quantity * price
                name = item['name']
                cart.add_item({'item_id':item_id,'name':name,'quantity':quantity,'price':new_price})
                invoice.add_item({'item_id':item_id,'name':name,'quantity':quantity,'price':new_price})   

        return render_template('store_manager_dashboard.html', message='Item added to cart successfully')
    
    return render_template('cart.html', items=cart.get_items())

@app.route('/store_manager/pay')
def pay():
        invoice_data = invoice.generate_invoice()

        # Reduce the quantity of purchased items in the inventory
        for item in invoice_data['items']:
            item_id = item['item_id']
            quantity_purchased = item['quantity']

            # Find the corresponding item in the inventory and update its quantity
            for available_item in inventory1.stock:
                if available_item['id'] == item_id:
                    available_item['quantity'] -= quantity_purchased

        # Delete items with quantity <= 0 from the inventory
        inventory1.stock = [item for item in inventory1.stock if item['quantity'] > 0]

        payment_observer.update()  # Notify observer (simple print statement here)
        
        return render_template('payment.html', total=invoice_data['total_amount'], discount=invoice_data['discount'])

if __name__ == '__main__':
    app.run(debug=True)

