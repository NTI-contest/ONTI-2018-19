with open('distances.txt','r') as file:
    dists = [(l.split()[0],
              float(l.split()[1])) for l in file.readlines()]
    dists = dict(dists)

with open('samples.txt','r') as file:
    samples = file.readline().split()

max_name, max_val  = samples[0], dists[samples[0]]
min_name, min_val  = samples[0], dists[samples[0]]

for sample in samples:
    if max_val < dists[sample]:
        max_val = dists[sample]
        max_name = sample
    if min_val > dists[sample]:
        min_val = dists[sample]
        min_name = sample
        
print(max_name, min_name)
