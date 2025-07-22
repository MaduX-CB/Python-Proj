import re
# Used for the digits
digits = {
    "0":"",
    "1":"one",
    "2":"two",
    "3":"three",
    "4":"four",
    "5":"five",
    "6":"six",
    "7":"seven",
    "8":"eight",
    "9":"nine"}

# Used for numbers in between 10 to 20
after_ten = {
    "0":"ten",
    "1":"eleven",
    "2":"twelve",
    "3":"thirteen",
    "4":"fourteen",
    "5":"fifteen",
    "6":"sixteen",
    "7":"seventeen",
    "8":"eighteen",
    "9":"nineteen"}

# Used for the ten digits
tens = {"0":"",
        "2":"twenty",
        "3":"thirty",
        "4":"fourty",
        "5":"fifty",
        "6":"sixty",
        "7":"seventy",
        "8":"eighty",
        "9":"ninety"}

# Used for determing what type the group of number is
three_digit = ["","Thousand", "Million", "Billion","Trillion"]

final=""
number = input("Enter a number")
number = number[::-1]

# splits the number into groups of three
numb = re.findall(r"\d{1,3}", number)

# Loop to perform the number check for each group of three
for i in range(5):
    try:
        num = numb[i]
    except IndexError:
        break
    else:
        # For identifying the units
        unit = digits[num[0]]
        
        # For identifying the ten digit
        try:
            ten_digit = num[1]
        # Used
        except IndexError:
            ten_word = unit
        else:
            if ten_digit == "1":
                ten_word = after_ten[num[0]]
            else:
                ten_word = f"{tens[ten_digit]} {unit}" 
        
        try:
            hundred_digit = num[2]
        except IndexError:
            hundred = ""
        else:
            if hundred_digit == "0":
                hundred = ""
            else:
                hundred = f"{digits[hundred_digit]} hundred"
        result = f",{hundred} {ten_word} {three_digit[i]}"
        if int(num) == 0:
            result = ""
        final = f"{result} {final}"
print(final.title().strip(",").strip())