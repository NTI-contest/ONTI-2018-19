

```python
import sqlite3
```


```python
conn = sqlite3.connect('database.db')
cur = conn.cursor()
```


```python
cur.execute("""SELECT * FROM customers WHERE name = "customer71";""")
res = cur.fetchall()
print(res)
```


```python
cur.execute("""SELECT balance FROM balances WHERE id = 778764;""")
res = cur.fetchall()
print(res)
```


```python
cur.execute("""
SELECT ((SELECT SUM(amount) FROM transactions WHERE ("to" = 778764)) - 
        (SELECT SUM(amount) FROM transactions WHERE ("from" = 778764)));
""")
res = cur.fetchall()
print(res)
```


```python
97750+(-86362)
```


```python
cur.execute("""
SELECT *
FROM transactions
WHERE ("from" = 778764)""")
res = cur.fetchall()
print(len(res))
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT *
FROM transactions
WHERE ("from" = 778764)""")
res = cur.fetchall()
print(len(res))
for i in res:
    print(i)
    cur.execute("""SELECT name FROM shops WHERE (id = {});""".format(i[2]))
    name = cur.fetchall()
    print(name)
```


```python
cur.execute("""
SELECT *
FROM transactions
JOIN shops ON transactions.[to] = shops.id
WHERE ("from" = 778764)""")
res = cur.fetchall()
print(len(res))
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT COUNT(*)
FROM transactions
JOIN shops ON transactions.[to] = shops.id
WHERE ("from" = 778764)
GROUP BY [from], [to]
""")
res = cur.fetchall()
print(len(res))
for i in res:
    print(i)
```


```python
cur.execute("""
SELECT COUNT(*)
FROM transactions
JOIN shops ON transactions.[to] = shops.id
WHERE ("from" = 778764)
GROUP BY [from], [to]
""")
res = cur.fetchall()
n = 0
for i in res:
    if i[0] >= 6:
        n = n + 1

print(n)
```


```python

```
