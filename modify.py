from store_data import write_file


def add_new(employee_list: list, department_list: list, employee_file, department_file):
    """
    Tạo mới nhân viên/quản lý (và bộ phận nếu chưa tồn tại)
    employee_list: danh sách nhân viên (danh sách các từ điển thông tin nhân viên/quản lý)
    department_list: danh sách phòng ban (danh sách các từ điển thông tin bộ phận)
    employee_file: file lưu trữ thông tin nhân viên (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    department_file: file lưu trữ thông tin bộ phận (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    """

    employee_info = {}
    required_infor = ["Nhập mã số", "Nhập mã bộ phận", "Nhập chức vụ (NV/QL)", "Nhập họ và tên", "Nhập hệ số lương",
                      "Nhập số ngày làm việc", "Nhập hệ số hiệu quả", "Nhập thưởng", "Nhập số ngày đi muộn"]

    print("----")
    print("Thêm nhân viên mới...")

    for x in required_infor[:4]:
        while True:
            employee_info[x] = input(x + ": ")

            # Cannot input blank
            if len(employee_info[x]) < 1:
                print("Bạn không được bỏ trống thông tin này")
                continue

            if x == "Nhập mã số":
                # If employee ID existed, break the for loop, ask user to input ID again
                maso = [employee_list[y]["Mã số"] for y in range(len(employee_list))]
                if employee_info[x] in maso:
                    print("Mã nhân viên đã tồn tại.")
                    continue
                # If employee ID is new, break while loop and go to next item
                else:
                    break

            # Check if department is new, create and add to department list, store to department file
            elif x == "Nhập mã bộ phận":
                dept_id = [dept["Mã bộ phận"] for dept in department_list]

                if employee_info[x] not in dept_id:
                    print("Mã bộ phận chưa tồn tại, tạo mới...")
                    while True:
                        try:
                            new_dept_bonus = int(input("Nhập thưởng bộ phận:\n"))
                            break
                        except ValueError:
                            print("Bạn phải nhập một số dương.")

                    department_list.append({"Mã bộ phận": employee_info[x], "Thưởng bộ phận": new_dept_bonus})
                    print("Đã tạo bộ phận mới...")
                    department_list.sort(key=lambda d: d['Mã bộ phận'])
                    write_file(department_file, department_list)

            break

    # Check if user enter negative number
    for a in required_infor[4:]:
        while True:
            employee_info[a] = input(a + ": ")

            # Cannot input blank
            if len(employee_info[a]) < 1:
                print("Bạn không được bỏ trống thông tin này")
                continue

            # Input must be number
            try:
                employee_info[a] = float(employee_info[a])
            except ValueError:
                print("Bạn phải nhập thông tin ở dạng số")
                continue

            # Input number must be positive
            if employee_info[a] < 0:
                print("Bạn phải nhập một số dương.")
                continue
            break

    # Get employee position
    if employee_info["Nhập chức vụ (NV/QL)"].lower() == "nv":
        position = "Nhân viên"
    else:
        position = "Quản lý"

    # Create a dict of employee data to append to employee list
    emp_dict = {
        "Mã số": employee_info["Nhập mã số"],
        "Mã bộ phận": employee_info["Nhập mã bộ phận"],
        "Chức vụ": position,
        "Họ và tên": employee_info["Nhập họ và tên"],
        "Hệ số lương": int(employee_info["Nhập hệ số lương"]),
        "Số ngày làm việc": int(employee_info["Nhập số ngày làm việc"]),
        "Hệ số hiệu quả": employee_info["Nhập hệ số hiệu quả"],
        "Thưởng": int(employee_info["Nhập thưởng"]),
        "Số ngày đi muộn": int(employee_info["Nhập số ngày đi muộn"])
    }

    employee_list.append(emp_dict)
    employee_list.sort(key=lambda e: e["Mã số"])
    write_file(employee_file, employee_list)
    print("Đã thêm nhân viên mới...")
    print("----")


def remove_employee(employee_list, employee_file):
    """
    Xóa nhân viên khỏi hệ thống theo ID
    employee_list: danh sách nhân viên (danh sách các từ điển thông tin nhân viên/quản lý)
    employee_file: file lưu trữ thông tin nhân viên (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    """

    emp_id_list = [emp["Mã số"] for emp in employee_list]
    print("----")

    while True:
        remove_id = input("Nhập mã nhân viên muốn xóa: ")
        if len(remove_id) < 1:
            print("Bạn không được bỏ trống thông tin này.")

        elif remove_id not in emp_id_list:
            stay = input("Mã nhân viên không tồn tại. Bạn có muốn nhập lại mã nhân viên không? (Y/N)\n")
            if stay[0].lower() == "y":
                continue
            else:
                return False

        else:
            for x in range(len(employee_list)):
                if employee_list[x]["Mã số"] == remove_id:
                    employee_list.pop(x)
                    break
            break

    write_file(employee_file, employee_list)
    print("Đã xóa thành công")
    print("----")


def remove_department(employee_list, department_list, department_file):
    """
    Xóa bộ phận khỏi hệ thống theo ID
    employee_list: danh sách nhân viên (danh sách các từ điển thông tin nhân viên/quản lý)
    department_list: danh sách phòng ban (danh sách các từ điển thông tin bộ phận)
    department_file: file lưu trữ thông tin bộ phận (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    """

    depts_have_employee = [emp["Mã bộ phận"] for emp in employee_list]
    dept_id_list = [dept["Mã bộ phận"] for dept in department_list]
    print("----")
    stay = 0

    while True:
        remove_dept_id = input("Nhập mã bộ phận muốn xóa: ")
        if len(remove_dept_id) < 1:
            print("Bạn không được bỏ trống thông tin này.")
            stay = 1

        elif remove_dept_id not in dept_id_list:
            print("Mã bộ phận không tồn tại.")
            stay = 1

        elif remove_dept_id in depts_have_employee:
            print("Bạn không thể xóa bộ phận đang có nhân viên.")
            stay = 1

        else:
            for y in range(len(department_list)):
                if department_list[y]["Mã bộ phận"] == remove_dept_id:
                    department_list.pop(y)
                    break
            stay = 0
            break

        if stay:
            again = input("Bạn có muốn nhập lại mã bộ phận không? (Y/N)\n")
            if again[0].lower() == "y":
                continue
            else:
                return False

    write_file(department_file, department_list)
    print("Đã xóa thành công")
    print("----")


def modify_employee(employee_list, department_list, employee_file, department_file):
    """
    Thay đổi thông tin nhân viên
    employee_list: danh sách nhân viên (danh sách các từ điển thông tin nhân viên/quản lý)
    department_list: danh sách phòng ban (danh sách các từ điển thông tin bộ phận)
    employee_file: file lưu trữ thông tin nhân viên (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    department_file: file lưu trữ thông tin bộ phận (bao gồm đường dẫn file nếu file nằm khác thư mục chương trình)
    """

    emp_id_list = [emp["Mã số"] for emp in employee_list]
    dept_id_list = [dept["Mã bộ phận"] for dept in department_list]

    required_infor = ["Nhập họ và tên", "Nhập mã bộ phận", "Nhập chức vụ (NV/QL)"]
    data_list = ["Họ và tên", "Mã bộ phận", "Chức vụ"]

    required_number = ["Nhập hệ số lương", "Nhập số ngày làm việc", "Nhập hệ số hiệu quả", "Nhập thưởng",
                       "Nhập số ngày đi muộn"]
    data_number = ["Hệ số lương", "Số ngày làm việc", "Hệ số hiệu quả", "Thưởng", "Số ngày đi muộn"]

    print("----")
    print("Chỉnh sửa nhân viên")
    modified = {}

    # Input and check if employee ID is valid
    while True:
        modify_id = input("Nhập mã nhân viên: ")

        if len(modify_id) < 1:
            print("Vui lòng nhập mã nhân viên.")

        elif modify_id not in emp_id_list:
            print()
            stay = input("Nhân viên không tồn tại. Bạn có muốn nhập lại? (Y/N)\n")
            if stay.lower() == "y":
                continue
            elif stay.lower() == "n":
                return False

        else:
            break

    # Get updated for first 3 data
    for x in range(len(required_infor)):
        modified[data_list[x]] = input(required_infor[x] + ": ")

        # Check if department ID is new
        if data_list[x] == "Mã bộ phận":
            if modified[data_list[x]] != "" and modified[data_list[x]] not in dept_id_list:
                print("Mã bộ phận chưa tồn tại.")
                print("Thêm bộ phận mới...")
                # If new, ask for department bonus and save to file
                while True:
                    try:
                        bon = int(input("Nhập thưởng bộ phận: "))
                        if bon < 0:
                            print("Vui lòng nhập một số dương")
                            continue
                    except ValueError:
                        print("Vui lòng nhập một số dương.")
                        continue
                    else:
                        department_list.append({"Mã bộ phận": modified[data_list[x]], "Thưởng bộ phận": bon})
                        print("Đã tạo bộ phận mới.")
                        department_list.sort(key=lambda d: d["Mã bộ phận"])
                        write_file(department_file, department_list)
                        break

    if modified["Chức vụ"].lower() == "nv":
        modified["Chức vụ"] = "Nhân viên"
    elif modified["Chức vụ"].lower() == "ql":
        modified["Chức vụ"] = "Quản lý"

        # Get updated information of number required data
    for y in range(len(required_number)):
        while True:
            change = input(required_number[y] + ": ")

            # If user leave blank input, add to modified dictionary
            if change == "":
                modified[data_number[y]] = change
                break
            else:
                # Check if input is a number
                try:
                    float(change)
                except ValueError:
                    print("Bạn cần nhập đúng định dạng (Số dương).")
                    continue

                # Check if input is a positive number
                if float(change) < 0:
                    print("Bạn cần nhập đúng đinh dang (Số dương).")
                else:
                    if required_number[y] == "Nhập hệ số hiệu quả":
                        modified[data_number[y]] = float(change)
                    else:
                        modified[data_number[y]] = int(change)
                    break

    # Go through every employee in employee list
    for emp in employee_list:
        # Pick employee whose ID is input
        if emp["Mã số"] == modify_id:
            for i in list(modified.keys()):
                # If modify input is blank, do nothing
                if modified[i] == "":
                    pass
                # Modify data
                else:
                    emp[i] = modified[i]

            print("----")
            employee_list.sort(key=lambda e: e["Mã số"])
            write_file(employee_file, employee_list)
            print("Đã hoàn tất chỉnh sửa")
            print("----")

            # Print edited employee
            for k, v in emp.items():
                print(f"{k}: {v}")
            print("----")

