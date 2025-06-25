from database.DAO import DAO

mydao = DAO()
colori = mydao.getAllColors()
for color in colori:
    print(color)