from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id

    @abstractmethod
    def calculate_pay(self):
        pass

class SalariedEmployee(Employee):
    def __init__(self, name, emp_id, weekly_salary):
        super().__init__(name, emp_id)
        self.weekly_salary = weekly_salary

    def calculate_pay(self):
        return float(self.weekly_salary)

class HourlyEmployee(Employee):
    def __init__(self, name, emp_id, hourly_rate, hours_worked):
        super().__init__(name, emp_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        if self.hours_worked <= 40:
            return self.hours_worked * self.hourly_rate
        regular_pay = 40 * self.hourly_rate
        overtime_pay = (self.hours_worked - 40) * (self.hourly_rate * 1.5)
        return regular_pay + overtime_pay

class CommissionEmployee(Employee):
    def __init__(self, name, emp_id, base_salary, sales, commission_rate):
        super().__init__(name, emp_id)
        self.base_salary = base_salary
        self.sales = sales
        self.commission_rate = commission_rate

    def calculate_pay(self):
        return self.base_salary + (self.sales * self.commission_rate)

def generate_payroll_summary(employees):
    return [{"id": e.emp_id, "name": e.name, "pay": e.calculate_pay()} for e in employees]

if __name__ == "__main__":
    h = HourlyEmployee("Alice", "H1", 20, 45)
    c = CommissionEmployee("Bob", "C1", 500, 4000, 0.10)
    print(generate_payroll_summary([h, c]))