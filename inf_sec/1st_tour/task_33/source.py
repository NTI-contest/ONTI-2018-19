import base64

def decrypt(x, n):
    key = 'qwertyuioplkjhgfdsazlfmh'

    if n < 0:
        return "".join([chr(c) for c in x])

    x.insert((n + 3) % len(x), x.pop(0))

    for i in range(n, len(x)):
        x[i] = x[i] ^ ord(key[i - n])    
    
    return decrypt(x, n - 1)

enc_flag = "TWEGaEc9C0NIeSYhD08YP1BkIDUFQzJ9"
tmp = base64.b64decode(enc_flag)
dec_flag = decrypt(list(tmp), len(tmp) - 1)
print(dec_flag)