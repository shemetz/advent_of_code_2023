def main():
    with open("day1.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    print(input_lines)


if __name__ == '__main__':
    main()
