import pyodbc
try:
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=localhost\\SQLEXPRESS;'
        'Database=my_HMS_db;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    print("Successfully connected!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)