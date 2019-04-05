from scipy.signal import butter, lfilter

data = list(map(float, input().split()))

nyq = 0.5 * 500
low = 3 / 250
high = 60 / 250
b, a = butter(4, [low, high], btype='band')
data = lfilter(b, a, data)

i = 0
beats = 0

while i < len(data) - 20:
    chunk = data[i:i+20]
    if max(chunk) - min(chunk) > 0.5:
        beats += 1
        i += 150
    i += 1

print(beats)
