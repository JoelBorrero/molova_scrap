import pandas as pd

from Database import Database


writer = pd.ExcelWriter('./Files/Report.xlsx', engine='xlsxwriter')
general = [0,0,0,0,0,0,0,0,0,0]
category_names = ["Camisas y Camisetas", "Pantalones y Jeans", "Vestidos y Enterizos", "Faldas y Shorts", "Abrigos y Blazers", "Ropa deportiva", "Zapatos", "Bolsos", "Accesorios", "Otros"]
df = pd.DataFrame({'Categoría':category_names})
df.to_excel(writer,'Report', index=False)
for i, brand in enumerate(['Bershka', 'Mango', 'Mercedes Campuzano', 'Pull & Bear', 'Stradivarius', 'Zara']):
    db = Database(brand)
    categories = [0,0,0,0,0,0,0,0,0,0]
    for item in db.getAllItems():
        index = category_names.index(item['category'])
        categories[index] += 1
        general[index] += 1
    df = pd.DataFrame({brand:categories})
    df.to_excel(writer,sheet_name='Report',startcol=i+2, index=False)
worksheet = writer.sheets['Report']
worksheet.set_column('A:H',16)
worksheet.conditional_format('B2:B11', {'type': '3_color_scale'})
df = pd.DataFrame({'General':general})
df.to_excel(writer, sheet_name='Report', startcol=1 , index=False)
writer.save()