import re
text = 'CHARGE: THE SUM OF THE\nCANCELLATION FEES OF ALL CANCELLED FARE\nCOMPONENTS.'
number = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
print(len(number))
print(number)