letters = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]
word = 'QUEEN'
idx = max(letters.index(i) for i in word)

max_value = 10 ** 8

for base in range(31, 100):
    s = 0
    for digit in word:
        s *= base
        s += letters.index(digit)
    if s < 10 ** 9:
        max_value = s
        
print(max_value)