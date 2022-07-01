from modify import add_new, remove_employee, remove_department, modify_employee
from classes import Employee, Manager, Department
from store_data import read_file
from taxes_and_fines import tax_rates, fine_rates

def menu(tax, fine, employee_file, department_file):
    """
    employee_list: danh sách nhân viên (danh sách các từ điển thông tin nhân viên/quản lý)
    department_list: danh sách phòng ban (danh sách các từ điển thông tin bộ phận)
    tax: danh sách mức thuế (danh sách các từ điển về các mức thuế theo các mức thu nhập)
    fine: danh sách mức phạt đi trễ (danh sách các từ điển về các mức phạt do đi trễ theo số ngày đi trễ)
    employee_file: file lưu trữ thông tin nhân viên (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    department_file: file lưu trữ thông tin bộ phận (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    """

    while True:

        employee_list = read_file(employee_file)
        department_list = read_file(department_file)

        print("==============  HỆ THỐNG QUẢN LÝ  ==============")
        print()
        print("1. Hiển thị danh sách nhân viên.")
        print("2. Hiển thị danh sách bộ phận.")
        print("3. Thêm nhân viên mới.")
        print("4. Xóa nhân viên theo ID.")
        print("5. Xóa bộ phận theo ID.")
        print("6. Hiển thị bảng lương.")
        print("7. Chỉnh sửa nhân viên.")
        print("8. Thoát.")

        while True:
            try:
                select = int(input("Nhập số thứ tự của chức năng bạn muốn chọn:\n"))
            except ValueError:
                print("Vui lòng nhập số thứ tự hiển thị trên Menu.")
                continue
            else:
                break

        # Create a list of objects from Employee and Manager
        emp_list_oop = []
        for x in employee_list:
            if x["Chức vụ"] == "Nhân viên":
                emp_list_oop.append(Employee(x["Mã số"], x["Họ và tên"], x["Hệ số lương"], x["Số ngày làm việc"],
                                             x["Mã bộ phận"], x["Hệ số hiệu quả"], x["Thưởng"], x["Số ngày đi muộn"]))
            else:
                emp_list_oop.append(Manager(x["Mã số"], x["Họ và tên"], x["Hệ số lương"], x["Số ngày làm việc"],
                                            x["Mã bộ phận"], x["Hệ số hiệu quả"], x["Thưởng"], x["Số ngày đi muộn"]))

        # Create a list of objects from Department
        dept_list_oop = []
        for y in department_list:
            dept_list_oop.append(Department(y["Mã bộ phận"], y["Thưởng bộ phận"]))

        # Show all employee data
        if select == 1:
            for emp in emp_list_oop:
                print(emp)

        # Show all department data
        elif select == 2:
            for dept in dept_list_oop:
                print(dept)

        # Add new employee
        elif select == 3:
            add_new(employee_list, department_list, employee_file, department_file)

        # Remove employee
        elif select == 4:
            remove = remove_employee(employee_list, employee_file)
            if not remove:
                continue

        # Remove department
        elif select == 5:
            remove_dept = remove_department(employee_list, department_list, department_file)
            if not remove_dept:
                continue

        # Show Payroll
        elif select == 6:
            for emp in emp_list_oop:
                print(emp.salary(department_list, tax, fine))

        # Edit employee data
        elif select == 7:
            modify = modify_employee(employee_list, department_list, employee_file, department_file)
            if not modify:
                continue

        # Exit program
        elif select == 8:
            print("Hẹn gặp lại.")
            break

        back = input("Bạn có muốn trở lại Menu không? (Y/N)\n")
        if back[0].lower() == "y":
            continue
        else:
            print("Hẹn gặp lại.")
            break


if __name__ == "__main__":

    TAX_URL = "https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien" \
              "%2FPYB101x_1.1%2FASM_Resources%2Ftax.xml?alt=media&token=f7a6f73d-9e6d-4807-bb14-efc6875442c7 "
    FINES_URL = "https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien" \
                "%2FPYB101x_1.1%2FASM_Resources%2Flate_coming.json?alt=media&token=55246ee9-44fa-4642-aca2-dde101d705de "

    taxes = tax_rates(TAX_URL)
    fines = fine_rates(FINES_URL)

    employee_file = "NV.json"
    department_file = "BP.json"

    menu(taxes, fines, employee_file, department_file)