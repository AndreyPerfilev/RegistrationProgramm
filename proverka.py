import re


s_two = input()
reg = r'[\W\s]'
result = re.findall(reg, s_two)

if len(result) == 0:
    print("l")
else:
    print("У вас есть недопустимые символы или пробелы")

print(s_two if len(result) == 0 else "У вас есть недопустимые символы или пробелы")

