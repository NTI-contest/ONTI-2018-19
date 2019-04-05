import numpy as np

def get_spectrum(y):
    Fs = 160.0
    Ts = 1.0/Fs
    n = len(y)
    k = np.arange(n)
    T = n/Fs
    frq = k/T
    frq = frq[range(n//2)]
    Y = np.fft.fft(y)/n
    Y = Y[range(n//2)]
    return frq, abs(Y)

def get_alpha(y):
    frq, Y = get_spectrum(y)
    alpha = 0
    for freq, ampl in zip(frq, Y):
        if freq > 8 and freq < 13:
            alpha += ampl
    return alpha

st = [s.split(',') for s in input().split()]
sig1, sig2 = zip(*st)
sig1 = [int(s) for s in sig1]
sig2 = [int(s) for s in sig2]
alpha1 = get_alpha(sig1)
alpha2 = get_alpha(sig2)
print('1' if alpha1 > alpha2 else '2')