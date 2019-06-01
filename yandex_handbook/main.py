"""
Суть данного пакета в том что бы подготовить файл в формате XLS для загрузки на яндекс
Файл будет содержать актуальные цены на лома.
"""

# import xlrd  # Чтение
#
# # rb = xlrd.open_workbook('price-list-template.xls', formatting_info=True)
# # sheet = rb.sheet_by_index(0)
# #
# # for rownum in range(sheet.nrows):
# #     row = sheet.row_values(rownum)
# #     for c_el in row:
# #         print(c_el)
#
#
# import xlwt  # Запись
#
# """
# 0 = Категория |1 = Название |2 = Описание |3 = Цена|4 = Фото |
#
# Словарь со списокм значений, ключ словаря это номер строки, индес списка = столбцу
# data = {0 : [Цветной лом, Медь, лбая медная деталь, 330р кг, vk.com/sdf23d.jpg
# """
#
# wb = xlwt.Workbook()
# ws = wb.add_sheet('A Test Sheet')
#
#
#
#
# ws.write(0, 0, 'Test')
# ws.write(0, 1, 'Test')
# ws.write(0, 2, 'Test')
# # ws.write(1, 0, datetime.now(), style1)
# # ws.write(2, 0, 1)
# # ws.write(2, 1, 1)
# # ws.write(2, 2, xlwt.Formula("A3+B3"))
#
#
# wb.save('example.xls', )

try:
    1 / 0

except Exception as error:
    print(type(error))