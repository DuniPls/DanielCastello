'''
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20×20 grid?

'''
x = []

totalRows = 22

for i in range(totalRows):
    y=[]
    for j in range(totalRows):
        y.append(0)
    x.append(y)
    
x[totalRows - 2][totalRows - 2] = 1

for i in range(totalRows - 2, -1, -1):
    for j in range(totalRows - 2, -1, -1):
        x[i][j] = x[i + 1][j] + x[i][j + 1] + x[i][j]


print(x)
