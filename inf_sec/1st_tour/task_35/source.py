from Crypto.PublicKey import RSA

class BroadcastAttack:
    t = []
    messsage = 0

    def __init__(self, e, N, C):
        self.e = e
        self.N = N
        self.C = C

    def calculate_partials(self):
        for i in range(self.e):
            mod_product = 1
            for j in range(self.e):
                if i != j:
                    mod_product *= self.N[j]
            t_i = self.C[i] * mod_product * ModUtil.modinv(mod_product, self.N[i])
            self.t.append(t_i)

    def solve_congruence(self):
        partial_total = 0
        mod_product = 1
        for i in range(self.e):
            partial_total += self.t[i]
            mod_product *= self.N[i]

        self.message = ModUtil.isqrt(partial_total % mod_product, self.e)

    def attack(self):
        self.calculate_partials()
        self.solve_congruence()
        return bytes.fromhex(hex(self.message)[2:]).decode()

class ModUtil:
    @staticmethod
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x_old, y_old = ModUtil.egcd(b % a, a)
            return gcd, y_old - (b // a) * x_old, x_old

    @staticmethod
    def modinv(a, m):
        gcd, x, y = ModUtil.egcd(a, m)
        if gcd != 1:
            raise Exception('Mod Inv Undefined')
        else:
            return x % m

    @staticmethod
    def isqrt(n, k):
        u, s = n, n + 1
        while u < s:
            s = u
            t = (k - 1) * s + n // pow(s, k - 1)
            u = t // k
        return s

def main():
    e = 5
    N = []
    C = []

    for i in range(1, 6):
        with open(f'{i}.pub.pem', 'rb') as f:
            N.append(RSA.importKey(f.read()).n)

        with open(f'{i}.enc', 'rb') as f:
            C.append(int(f.read().hex(), 16))

    attack = BroadcastAttack(e, N, C)
    print(attack.attack())

if __name__ == '__main__':
    main()