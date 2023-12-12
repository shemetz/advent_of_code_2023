with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]
numsum = 0
for line in input_lines:
    digits = [c for c in line if c.isdigit()]
    first_digit = digits[0]
    last_digit = digits[-1]
    numsum += int(f"{first_digit}{last_digit}")

print(numsum)  # 54953

numsum = 0
digit_list = list(enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]))
digit_list.extend(list(enumerate(str(i) for i in range(10))))
for line in input_lines:
    first_d = "error"
    first_d_index = len(line)
    last_d = "error2"
    last_d_index = -2
    for d, digit in digit_list:
        index = line.find(digit)
        rindex = line.rfind(digit)
        if index != -1 and index < first_d_index:
            first_d = d
            first_d_index = index
        if rindex != -1 and rindex > last_d_index:
            last_d = d
            last_d_index = rindex
    numsum += int(f"{first_d}{last_d}")

print(numsum)  # 53868
