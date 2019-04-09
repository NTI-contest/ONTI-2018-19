

```python
import sqlite3
```


```python
conn = sqlite3.connect('database.db')
cur = conn.cursor()
```


```python
cur.execute("""
SELECT name
FROM sqlite_master 
WHERE (type ='table')
""")
res = cur.fetchall()
```


```python
res
```


```python
cur.execute("""
SELECT sql 
FROM sqlite_master 
WHERE name = 'shops';
""")
res = cur.fetchall()
```


```python
print(res[0][0])
```


```python
cur.execute("""SELECT * FROM shops;""")
res = cur.fetchall()[:5]
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT sql 
FROM sqlite_master 
WHERE name = 'customers';
""")
res = cur.fetchall()
```


```python
print(res[0][0])
```


```python
cur.execute("""SELECT * FROM customers;""")
res = cur.fetchall()[:5]
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT sql 
FROM sqlite_master 
WHERE name = 'balances';
""")
res = cur.fetchall()
```


```python
print(res[0][0])
```


```python
cur.execute("""SELECT * FROM balances;""")
res = cur.fetchall()[:5]
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT sql 
FROM sqlite_master 
WHERE name = 'ids';
""")
res = cur.fetchall()
```


```python
print(res[0][0])
```


```python
cur.execute("""SELECT * FROM ids;""")
res = cur.fetchall()[:5]
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT sql 
FROM sqlite_master 
WHERE name = 'transactions';
""")
res = cur.fetchall()
```


```python
print(res[0][0])
```


```python
cur.execute("""SELECT * FROM transactions;""")
res = cur.fetchall()[:5]
for i in res:
    print(i)
```


```python

```
