from mysql.connector import MySQLConnection, Error
import mysql.connector
from config import HOST, PORT, PSWD, USER, DBNAME
from   pprint import pprint

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PSWD,
            database=DBNAME
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection



def get_category_list():
    sql = 'SELECT p.product_id, pd.name, pc.category_id FROM oc_product p INNER JOIN oc_product_description pd ON (pd.product_id=p.product_id) INNER JOIN oc_product_to_category pc ON(p.product_id = pc.product_id) GROUP BY pc.category_id'
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    category_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return category_list


def get_products_from_category(product_id:int, category_id:int)->list:
    sql = f"SELECT product_id from oc_product_to_category WHERE category_id = {category_id} AND product_id<>{product_id};"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    products = cursor.fetchall()
    p = []
    values = f"({product_id},{product_id}, 0, '', 0)"
    for prod in products:
        values +=","
        values += f"({product_id},{prod[0]}, 0, '', 0)"
    sql = f"INSERT INTO oc_hpmodel_links (parent_id, product_id, sort, image, type_id) VALUES {values}"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    category_list = get_category_list()
    for cat in category_list:
        get_products_from_category(cat[0], cat[2])
