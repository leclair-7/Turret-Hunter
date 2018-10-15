

class Person():
	def __init__(self):
		self.name=""
	def report(self):
		print("Report for:", self.name)

class Employee(Person):
	def __init__(self):
		super().__init__()
		self.job_title = ""
	def report(self):
		print("Employee report for:", self.name)

class Customer(Person):
	"""odcstring for Customer"""
	def __init__(self):
		super().__init__()
		self.email = ""
	def report(self):
		super().report()
		print("Customer e-mail:",self.email)

lucas_hagel = Person()
lucas_hagel.name = "Lucas Hagel"

jane_employee = Employee()
jane_employee.name = "Jane Employee"
jane_employee.job_title = "Fur Brusher"

bob_customer = Customer()
bob_customer.name = "Bob"
bob_customer.email = "bob@bob.com"

lucas_hagel.report()
jane_employee.report()
bob_customer.report()
		