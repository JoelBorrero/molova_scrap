import psycopg2


class SQLDatabase:
    """Creates a SQL Database"""

    def __init__(self):
        """Starts the connection to the database"""
        self.con = psycopg2.connect(
            host="localhost", database="Molova", user="postgres", password="admin"
        )
        print("Conectado con éxito")
        self.cursor = self.con.cursor()

    def createItemsTable(self):
        """Create a new Table. If table exists will be deleted and created as new"""
        self.cursor.execute("drop table if exists items")
        sql = """create table items(
            brand varchar(30) not null,
            name varchar(50) not null,
            description varchar,
            priceBefore char(15) not null,
            allPricesNow char(15) not null,
            discount char(5),
            allImages varchar,
            url char(100) not null,
            allSizes varchar(100),
            colors varchar,
            category char(20) not null,
            originalCategory varchar(30),
            subcategory char(10) not null,
            originalSubcategory varchar(30),
            sale bool not null,
            gender char(6) not null,
            data json,
            PRIMARY KEY (url)
            )"""
        self.cursor.execute(sql)

    def insert(self, item):
        sql = f"""INSERT INTO items VALUES(
            '{item['brand']}',
            '{item['name']}',
            '{item['description']}',
            '{str(item['priceBefore']).replace("'",'"')}',
            '{str(item['allPricesNow']).replace("'",'"')}',
            '{item['discount']}',
            '{str(item['allImages']).replace("'",'"')}',
            '{item['url']}',
            '{str(item['allSizes']).replace("'",'"')}',
            '{str(item['colors']).replace("'",'"')}',
            '{item['category']}',
            '{item['originalCategory']}',
            '{item['subcategory']}',
            '{item['originalSubcategory']}',
            '{item['sale']}',
            '{item['gender']}'
            );"""
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except:
            print("Error executing sql")

    def close(self):
        """This functions must be called to save"""
        self.con.commit()
        self.con.close()