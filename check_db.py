import sqlite3

conn = sqlite3.connect('claims.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [row[0] for row in tables])

# Check claim_list data
cursor.execute("SELECT COUNT(*) FROM claim_list")
claim_list_count = cursor.fetchone()[0]
print('Claim list count:', claim_list_count)

# Check claim_detail data
cursor.execute("SELECT COUNT(*) FROM claim_detail")
claim_detail_count = cursor.fetchone()[0]
print('Claim detail count:', claim_detail_count)

# Show sample data
if claim_list_count > 0:
    cursor.execute("SELECT * FROM claim_list LIMIT 3")
    print('Claim list sample:')
    for row in cursor.fetchall():
        print(row)

if claim_detail_count > 0:
    cursor.execute("SELECT * FROM claim_detail LIMIT 3")
    print('Claim detail sample:')
    for row in cursor.fetchall():
        print(row)

conn.close()
