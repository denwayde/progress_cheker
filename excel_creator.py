from openpyxl import Workbook
from db_func import select_data


# wb = Workbook()
# ws = wb.active

data = select_data("SELECT * FROM points")
print(data)
