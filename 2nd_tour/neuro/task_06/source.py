import numpy as np

def get_spectrum(y):
    Fs = 256.0
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

data = np.array([int(s) for s in input().split()])
alphas = []
chunk_size = 256
for start in range(0,len(data)-chunk_size,chunk_size):
    alphas.append(get_alpha(data[start:start+chunk_size]))

for i in range(1,len(alphas)):
    alphas[i] = 0.8 * alphas[i-1] + 0.2 * alphas[i]

level = (max(alphas)+min(alphas))/2
peaks = 0
for i in range(1,len(alphas)):
    if alphas[i-1]<=level and alphas[i]>level:
        chunk = data[i*chunk_size:(i+1)*chunk_size]
        if max(chunk)-min(chunk) < 1300:
            peaks += 1
print(peaks)
