from collections import defaultdict

N, M = [int(v) for v in input().split()]

mkb = defaultdict(lambda: defaultdict(int))

for _ in range(N):
    C, k_raw = input().split()
    for _ in range(int(k_raw)):
        S, p_raw = input().split()
        mkb[C][S] = float(p_raw)

H = input().split()

rating = {}
for disease, symptoms in mkb.items():
    K = 0.0
    for symptom, score in symptoms.items():
        K += score if symptom in H else -score
    rating[disease] = K

rating_max = max(rating.values())
rating_to_display = [k for (k, v) in rating.items() if v == rating_max]
rating_to_display.sort()

for disease in rating_to_display:
    print(disease)