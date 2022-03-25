rows = int(input("Enter number of rows: "))
number = 1

for i in range(1, rows + 1):
    for j in reversed(range(number, i + number)):
        print(j, end=" ")
        number += 1
    print()

