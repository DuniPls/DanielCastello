'''
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.

'''
digs = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digits =["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
teens=["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens=["twenty", "thrity", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
hundred ="hundred"
thousand ="thousand"
connector = "and"

total = 0

#1-9

for d in digits:
    total += len(d)
    print(d + " = " + str(len(d)))
    
#10-19
for d in teens:
    total += len(d)
    print(d + " = " + str(len(d)))
    
#20-99
for t in tens:
    for d in digits:
        total += len(t+d)
        print(t+d + " = " + str(len(t+d)))
        
        
#100, 200, 300, 400, 500, 600, 700, 800, 900
for d in digs:
    total += len(d + hundred)
    print(d + " " + hundred + " = " + str(len(d + hundred)))
    
for d in digs:
    for i in digs:
        total += len(d + hundred + connector + i)
        print(d + " " + hundred + " " + connector + " " + i + " = " + str(len(d + hundred + connector + i)))
    for i in teens:
        total += len(d + hundred + connector + i)
        print(d + " " + hundred + " " + connector + " " + i + " = " + str(len(d + hundred + connector + i)))
    for i in tens:
        for j in digits:
            total += len(d + hundred + connector + i + j)
            print(d + " " + hundred + " " + connector + " " + i + j + " = " + str(len(d + hundred + connector + i + j)))
            
total += len(digs[0] + thousand)
print(digs[0] + " " + thousand + " = " + str(len(digs[0] + thousand)))
print(total)
