from itertools import combinations

a = ["paneer", "buttermilk", "roti"]

food_com = combinations(a, 2)

# for i in list(food_com):
#     print(i)

food_com = list(food_com)
print(food_com)

print(food_com[0][0])

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

print(result)
new_result = []
for i in result:
    new_result.append(i / total_order)

print(new_result)