import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def tax_rates(tax_url):
    """Trích xuất dữ liệu tính toán chỉ số thuế"""

    # Access https using ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Access website, get data, create a list of dictionaries from output data
    tax_connection = urllib.request.urlopen(tax_url, context=ctx).read()
    tax_data = ET.fromstring(tax_connection)
    t_rate = []

    # Check if input is in right data type
    for tax in tax_data:
        try:
            di = {"min": float(tax[0].text),
                  "max": float(tax[1].text),
                  "value": float(tax[2].text)}
        except IndexError:
            di = {"min": float(tax[0].text),
                  "value": float(tax[1].text)}
        except ValueError:
            print("Các dữ liệu về thuế phải là số. Vui lòng kiểm tra dữ liệu.")
        except TypeError:
            print("Các dữ liệu thuế trích xuất được phải là danh sách hoặc từ điển với các giá trị là số. Vui lòng "
                  "kiểm tra lại dữ liệu trích xuất")
        t_rate.append(di)

    return t_rate


def fine_rates(fines_url):
    """Trích xuất dữ liệu phạt do đi trễ"""

    # Access https using ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Access website and get data as json format (list of dictionary)
    fines_connection = urllib.request.urlopen(fines_url, context=ctx)
    fines_read = fines_connection.read().decode("UTF-8")
    fines_data = json.loads(fines_read)

    # Ensure information from fine list is in correct type
    try:
        fines_data[-1]["min"] = float(fines_data[-1]["min"])
        fines_data[-1]["value"] = float(fines_data[-1]["value"])
        for x in fines_data[0:-1]:
            for k, v in x.items():
                x[k] = float(v)
    except ValueError:
        print("Các dữ liệu về mức phạt phải là số. Vui lòng kiểm tra dữ liệu.")
    except TypeError:
        print("Các dữ liệu về mức phạt trích xuất được phải là danh sách hoặc từ điển với các giá trị là số. Vui lòng "
              "kiểm tra lại dữ liệu trích xuất")

    return fines_data
