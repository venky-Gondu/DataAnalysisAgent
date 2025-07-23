import sqlite3

conn=sqlite3.connect('ecommerce_data.db')
cursor=conn.cursor()
result=cursor.execute('''select * from product_total_sales ''')
for row in result:
    print(row)
