import sqlite3

customer = input()
min_balance = int(input())
min_buys = int(input())

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# получаем начальный баланс пользователя
cur.execute('''
SELECT balance
FROM balances
JOIN customers ON balances.id = customers.id
WHERE customers.name = '{}';
'''.format(customer))
balance = cur.fetchall()[0][0]

# находим количество денежных едениц, полученных пользователем
cur.execute('''
SELECT SUM(amount) as recieved
FROM transactions
JOIN customers ON transactions.[to] = customers.id
WHERE customers.name = '{}';
'''.format(customer))
received = cur.fetchall()[0][0]

# находим количество денежных едениц, потраченных пользователем
cur.execute('''
SELECT SUM(amount) as spent
FROM transactions
JOIN customers ON transactions.[from] = customers.id
WHERE customers.name = '{}';
'''.format(customer))
spent = cur.fetchall()[0][0]

# balance + received - spent = конечный баланс пользователя
if (balance + received - spent) < min_balance:
    print(0)
else:
    # получаем выборку магазинов, 
    # в которых пользователь customer совершал покупки не менее min_buys раз
    cur.execute('''
    SELECT shops.name, COUNT(*) AS n_buys
    FROM transactions
    JOIN customers ON transactions.[from] = customers.id
    JOIN shops ON transactions.[to] = shops.id
    WHERE customers.name = '{}'
    GROUP BY [from], [to]
    HAVING n_buys >= {};
    '''.format(customer, min_buys))
    # находим количество строк в выборке,
    # что и является искомым числом магазинов
    n_buys = len(cur.fetchall())
    print(n_buys)