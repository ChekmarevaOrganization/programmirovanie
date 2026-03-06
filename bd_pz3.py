import mysql.connector

class SQLTable:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_table(self, columns):
        cols = ', '.join(f"`{name}` {dtype}" for name, dtype in columns.items())
        query = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            {cols}
        )
        """
        self.cursor.execute(query)
        self.connection.commit()
        print(f"Table '{self.table_name}' created")

    def insert(self, data):
        columns = ', '.join(f"`{k}`" for k in data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO `{self.table_name}` ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"Row inserted, ID: {self.cursor.lastrowid}")
        return self.cursor.lastrowid

    def update(self, data, filters):
        set_clause = ', '.join(f"`{k}` = %s" for k in data.keys())
        where_clause = ' AND '.join(f"`{k}` = %s" for k in filters.keys())
        values = tuple(data.values()) + tuple(filters.values())

        query = f"UPDATE `{self.table_name}` SET {set_clause} WHERE {where_clause}"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"Updated {self.cursor.rowcount} rows")
        return self.cursor.rowcount

    def delete(self, filters):
        where_clause = ' AND '.join(f"`{k}` = %s" for k in filters.keys())
        values = tuple(filters.values())

        query = f"DELETE FROM `{self.table_name}` WHERE {where_clause}"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"Deleted {self.cursor.rowcount} rows")
        return self.cursor.rowcount

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS `{self.table_name}`"
        self.cursor.execute(query)
        self.connection.commit()
        print(f"Table '{self.table_name}' dropped")

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    db_config = {
        'user': 'j30084097_137',
        'password': 'Gruppa137',
        'host': 'srv221-h-st.jino.ru',
        'database': 'j30084097_137'
    }

    table = SQLTable(db_config, 'school')

    columns = {
        'name': 'text',
        'surname': 'text',
        'class_level': 'INT'
    }
    table.create_table(columns)

    table.insert({
        'name': 'Varvara',
        'surname': 'Chekmareva',
        'class_level': 11
    })

    table.update(

        data={'class_level': 10},
        filters={'name': 'Varvara'}
    )

    table.delete(filters={'name': 'Varvara'})

    table.drop_table()

    table.close()
