letters = [chr(i) for i in range(1072, 1104)]
letters.insert(6, 'ё')
len(letters)

number = int(input())
word = ''
while(number):
    word = letters[number % 34 - 1] + word
    number //= 34

print(word)