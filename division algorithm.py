def FindDigitNumber(number):
    digit_number = 0
    magnitude = 1
    while True:
        magnitude *= 10
        digit_number += 1
        if number - magnitude < 0:
            break
    return digit_number


def SeparateDigit(number):
    digit_number = FindDigitNumber(number)
    digit_array = []
    for i in reversed(range(digit_number)):
        leading_digit = number // (10 ** i)
        digit_array.append(leading_digit)
        number -= leading_digit * (10 ** i)
    return digit_array


"""
def Division(dividend, divisor):
    dividend_digits = SeparateDigit(dividend)
    remainder = 0
    quotient = 0
    for i in dividend_digits:
        current_dividend = remainder * 10 + i
        quotient *= 10
        quotient += current_dividend // divisor
        remainder = current_dividend % divisor
    return quotient, remainder
"""


def Division(dividend, divisor):
    if dividend < divisor:
        quotient = 0
        remainder = dividend
        return quotient, remainder
    quotient, remainder = Division(dividend // 10, divisor)
    dividend = remainder * 10 + dividend % 10
    quotient = quotient * 10 + dividend // divisor
    remainder = dividend % divisor
    return quotient, remainder

dividend = 155
divisor = 3
quotient, remainder = Division(dividend, divisor)
print(quotient, "...", remainder)