import mysql.connector  # library koneksi python ke mysql

# mengkoneksikan ke mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbmasker",
    # auth_plugin="mysql_native_password"
)
#print(mydb)
# kursor untuk akses di database mysql
my_cursor = mydb.cursor()

# membuat database di mysql
#my_cursor.execute("CREATE DATABASE dbmasker")

# membuat tabel pada database di mysql
my_cursor.execute(
    "CREATE TABLE data_masker (No INTEGER(255), Tanggal VARCHAR(255), Jam VARCHAR(255), Suhu VARCHAR(255), Ket_Masker VARCHAR(255), id INTEGER AUTO_INCREMENT PRIMARY KEY)"
)

# menambahkan data ke database
#sqlstuff = "INSERT INTO cobadb (No, Tanggal, Jam, Suhu, Ket_Masker) VALUES (%s, %s, %s, %s, %s)"
#record1 = (1, "18/01/2023", "13:03:17", 28.37, "No Mask")
#my_cursor.execute(sqlstuff, record1)
# mydb.commit()

# menampilkan data dari database
'''query = "SELECT * FROM data_masker"
my_cursor.execute(query)
records = my_cursor.fetchall()
for x in records:
    print(x)'''
