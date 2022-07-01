
class Employee:
    manager_bonus = 1.0
    position = "Nhân viên"

    def __init__(self, id, name, salary_base, working_days, department, working_performance, bonus, late_coming_days):
        self.id = id
        self.name = name
        self.department = department

        # Make sure input information is in right type
        try:
            self.salary_base = int(salary_base)
            self.working_days = int(working_days)
            self.working_performance = float(working_performance)
            self.bonus = int(bonus)
            self.late_coming_days = int(late_coming_days)
        except ValueError:
            print("Một số dữ liệu phải ở dạng số. Vui lòng kiểm tra lại dữ liệu.")

    def salary(self, dept_list, tax, fine):
        """Tính thu nhập thực nhận của nhân viên
        dept_list: danh sách bộ phận
        tax: danh sách các mức thuế dựa theo thu nhập. i.e. [{"min": 0, "max": 5, "value": 5}]
        fine: danh sách các mức phạt đi trễ dựa theo số ngày đi trễ. i.e. [{"min": 0, "max": 5, "value": 5}]
        """

        # Get department bonus from department id
        for dept in dept_list:
            if dept["Mã bộ phận"] == self.department:
                dept_bonus = int(dept["Thưởng bộ phận"])

        # Base monthly salary
        salary_before_bonus = self.salary_base * self.working_days * self.working_performance

        # Get fine rate
        # If late working day = 0, fine rate = 0
        fine_rate = 0
        if self.late_coming_days > fine[-1]["min"]:
            fine_rate = fine[-1]["value"]
        else:
            for x in fine[0:-1]:
                if x["min"] < self.late_coming_days <= x["max"]:
                    fine_rate = x["value"]

        # Salary before tax, after bonus and fine for late working days
        salary_before_insurance = salary_before_bonus + self.bonus + dept_bonus * self.manager_bonus - self.late_coming_days * fine_rate

        # Salary after insurance
        salary_before_tax = salary_before_insurance * 0.895

        # Get tax rate
        # If salary = 0, tax rate = 0
        tax_rate = 0
        # Check last item of tax rates list because it has no "max" (or can check salary >= x["min"] for x in tax[::-1)
        if salary_before_tax / 1000000 > tax[-1]["min"]:
            tax_rate = tax[-1]["value"]
        # Check where the tax rate is from list
        else:
            for x in tax[0:-1]:
                if x["min"] < salary_before_tax / 1000000 <= x["max"]:
                    tax_rate = x["value"] / 100

        # Total receive after tax
        receive = salary_before_tax * (1 - tax_rate)

        return f"----\nMã số: {self.id}\nThu nhập thực nhận: {int(receive):,} (VND)\n----"

    def __str__(self):
        return f"----\nMã số: {self.id}\nMã bộ phận: {self.department}\nChức vụ: {self.position}\nHọ và tên: {self.name}\nHệ số lương: {self.salary_base:,} (VND)\nSố ngày làm việc: {self.working_days} (ngày)\nHệ số hiệu quả: {self.working_performance}\nThưởng: {self.bonus:,} (VND)\nSố ngày đi muộn: {self.late_coming_days}\n---- "


class Manager(Employee):
    """Kế thừa Employee Class"""

    # Manager gets another 10% from department bonus
    manager_bonus = 1.1
    position = "Quản lý"


class Department:
    def __init__(self, id, bonus_salary):
        self.id = id
        self.bonus_salary = bonus_salary

    def __str__(self):
        return f"----\nMã bộ phận: {self.id}\nThưởng bộ phận: {self.bonus_salary:,} (VND)\n----"


