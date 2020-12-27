# Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

# For example, suppose your expense report contained the following:

# 1721
# 979
# 366
# 299
# 675
# 1456
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.


def find_nums_for_sum_2020():

    f = open("day_1.txt", "r")

    numbers_list = f.read().splitlines()

    f.close()

    for element in numbers_list:
        num_in_list = int(element)
        for comp_num in range(0, len(numbers_list)):
            comp_num_in_list = int(numbers_list[comp_num])
            if (num_in_list + comp_num_in_list) == 2020:
                return num_in_list, comp_num_in_list


print(find_nums_for_sum_2020())

def find_three_nums_for_sum_2020():

    f = open("day_1.txt", "r")

    numbers_list = f.read().splitlines()

    f.close()

    for element in numbers_list:
        num_in_list = int(element)
        for comp_num in range(0, len(numbers_list)):
            comp_num_in_list = int(numbers_list[comp_num])
            for third_num in range(0, len(numbers_list)):
                third_num_in_list = int(numbers_list[third_num])

            
                if (num_in_list + comp_num_in_list + third_num_in_list) == 2020:
                    return num_in_list, comp_num_in_list, third_num_in_list


print(find_three_nums_for_sum_2020())