import pandas as pd

df = pd.read_csv('input.csv', index_col=0)
ans_bool = df.turns.apply(lambda x: 'white' if x % 2 else 'black')
answer = pd.DataFrame({'winner' : ans_bool})
answer.to_csv('answer.csv', index=False)