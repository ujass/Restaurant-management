from itertools import combinations
import csv

new_order = ["paneer", "buttermilk", "roti"]

food_com = combinations(new_order, 2)

food_com = list(food_com)
print(food_com)
print(food_com[0][0])

# Fake old orders
all_order = [["paneer", "buttermilk", "papad"], ["dabeli", "vadapau", "buttermilk"], ["roti", "paneer"], ["paneer", "roti", "papad"], ["vadapau", "buttermilk"], ["buttermilk", "papad"],
             ["vadapau", "dabeli"], ["paneer", "roti"], ["paneer", "roti", "buttermilk"]]


total_order = len(all_order) + 1
result = []

for i in food_com:
    count = 0
    for j, value in enumerate(all_order):
        if i[0] in value and i[1] in value:
            count += 1

    result.append(count)

new_result = []
for i in result:
    new_result.append(i / total_order)

print(new_result)
# print(food_com[0][0]) // accces food_com


"""
    1) Read csv file
    2) Update data
    3) Write file
"""

with open('FOODSS.csv', 'r') as r:
    r = csv.reader(open('FOODSS.csv')) 
    lines = list(r)
    print(lines)

for i, food_pair in enumerate(food_com):
    for j in range(2):
        
        col_index1 = lines[0].index(food_com[i][0].upper())  # paneer index
        row_index1 = lines[0].index(food_com[i][1].upper())  # buttermilk index
       
        lines[row_index1][col_index1] = new_result[i]  # Mean = lines[paneer][buttermilk]
        lines[col_index1][row_index1] = new_result[i]  # Mean = lines[buttermilk][paneer]
        print(lines[row_index1][col_index1])
        print( lines[col_index1][row_index1])


with open('FOODSS.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(lines)