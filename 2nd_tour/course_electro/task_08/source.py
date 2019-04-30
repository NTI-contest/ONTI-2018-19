R1 = 4.7
R2 = 5.6
R_Int = 10.0

def find_value(A, D1, D2):
  # A0 - OUTPUT, полностью определяет результат
  if A == '0':
    return 0
  elif A == '1':
    return 1023

  if (D1 in '1U') and (D2 in '1U'):  # оба HIGH or PULLUP
    return 1023

  if D1 == '0' and D2 == '0':  # R1,R2 параллельно на GND
    if A == 'I':
      return 0  #  GND независимо от R1/R2
    Else:   #  R1, R2 параллельно, R_int сверху делителя
      r_dn = 1 / (1/R1 + 1/R2)
      r_up = R_Int
      return int(1023 * r_dn / (r_up + r_dn) )
    
  # Считаем верх делителя: начать с бесконечности, учитывать все
  # резисторы, идущие параллельно
  r_up = math.inf
  if A == 'U':
    r_up = 1 / (1/R_Int + 1/r_up)
  if D1 == '1':
    r_up = 1 / (1/R1 + 1/r_up)
  elif D1 == 'U':  # R_Int встает последов. c R1
    r_up = 1 / (1/(R1+R_Int) + 1/r_up)

  if D2 == '1':
    r_up = 1 / (1/R2 + 1/r_up)
  elif D2 == 'U':
    r_up = 1 / (1/(R2+R_Int) + 1/r_up)


  # Аналогично с "нижними" резисторами, но тут только могут быть R1 и R2
  r_dn = math.inf
  if D1 == '0':
    r_dn = 1 / (1/R1 + 1/r_dn)
  if D2 == '0':
    r_dn = 1 / (1/R2 + 1/r_dn)


  # Все 3 пина поставлены на INPUT, неопределенное напряжение.
  if r_up == math.inf and r_dn == math.inf:
    return None

  if r_dn == math.inf:
    return 1023
  if r_up == math.inf:
    return 0

  return int(1023 * r_dn / (r_up + r_dn) )


# Полный перебор состояний пинов 
results = []
for A0 in "IU01":
  for D1 in "IU01":
      for D2 in "IU01":
        v = find_value(A0, D1, D2)
        if not (v is None):
          results.append(v)


# Печатаем все уникальные решения, с сортировкой по возрастанию.
arr = [str(v) for v in sorted(set(results))]
print(len(arr))
print(' '.join(arr))