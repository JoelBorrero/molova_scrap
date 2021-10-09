import pandas as pd

from Database import Database


writer = pd.ExcelWriter('./Files/Report.xlsx', engine='xlsxwriter')
general = [0,0,0,0,0,0,0,0,0,0]
category_names = ["Camisas y Camisetas", "Pantalones y Jeans", "Vestidos y Enterizos", "Faldas y Shorts", "Abrigos y Blazers", "Ropa deportiva", "Zapatos", "Bolsos", "Accesorios", "Otros"]
df = pd.DataFrame({'Categoría':category_names})
df.to_excel(writer,'Report', index=False)
brands = [{'name': 'Bershka', 'data': {}}, {'name': 'Mango', 'data': {}}, {'name': 'Mercedes Campuzano', 'data': {}}, {'name': 'Pull & Bear', 'data': {}}, {'name': 'Stradivarius', 'data': {}}, {'name': 'Zara', 'data': {}}]
for i, brand in enumerate(brands):
    db = Database(brand['name'])
    categories = [0,0,0,0,0,0,0,0,0,0]
    for item in db.getAllItems():
        index = category_names.index(item['category'])
        categories[index] += 1
        general[index] += 1
    df = pd.DataFrame({brand['name']:categories})
    df.to_excel(writer,sheet_name='Report',startcol=i+2, index=False)
worksheet = writer.sheets['Report']
worksheet.set_column('A:H',16)
worksheet.conditional_format('B2:B11', {'type': '3_color_scale'})
df = pd.DataFrame({'General':general})
df.to_excel(writer, sheet_name='Report', startcol=1 , index=False)
catcher = pd.read_excel('./Files/Catcher.xlsx', sheet_name=None,engine='openpyxl')
columns = ['Hora', 'Cambió', 'Nuevos', 'Actualizados']
for brand in brands:
    for _, key in enumerate(catcher):
        if brand['name'].replace(' & ', 'And') in key:
            records = catcher[key]
            for i in range(1, len(records['Hora'])):
                row = []
                for col in columns:
                    row.append(records[col][i])
                hour = row[0][:row[0].index(':')]
                if hour in brand['data']:
                    brand['data'][hour]['Nuevos'] += row[2]
                    brand['data'][hour]['Actualizados'] += row[3]
                    brand['data'][hour]['Visitados'] += 1
                else:
                    brand['data'][hour] = {'Nuevos': row[2], 'Actualizados': row[3], 'Visitados': 1}
columns = ['Hora', 'Nuevos', 'Actualizados', 'Visitados', 'Frecuencia']
conditional = ['E', 'K', 'W', 'AC', 'AI']
for brand in brands:
    cols = [[],[],[],[],[]]
    for _, key in enumerate(brand['data']):
        data = [int(key), brand['data'][key]['Nuevos'], brand['data'][key]['Actualizados'], brand['data'][key]['Visitados']]
        index = 0
        for c in cols[0]:
            if data[0] > c:
                index = cols[0].index(c) + 1
        cols[0].insert(index, data[0])
        cols[1].insert(index, data[1])
        cols[2].insert(index, data[2])
        cols[3].insert(index, data[3])
        cols[4].insert(index, (data[1] + data[2]) / data[3] if data[3] else 0)
        pd.DataFrame({brand['name']:[]}).to_excel(writer,sheet_name='Updates',startcol=6*brands.index(brand),startrow=0, index=False)
        for i in range(5):
            # worksheet.set_column('D:E',len(cols[i])+2)
            df = pd.DataFrame({columns[i]:cols[i]}) 
            df.to_excel(writer,sheet_name='Updates',startcol=6*brands.index(brand)+i,startrow=1, index=False)
    worksheet = writer.sheets['Updates']
    for i in range(5):
        worksheet.conditional_format(f'{conditional[i]}3:{conditional[i]}{_+3}', {'type': '3_color_scale'})
writer.save()