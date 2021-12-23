# -*- coding: utf-8 -*-
''' Convert number to string '''
import re

from constant import (
    NUMBER_SYSTEM_NAME,
    NUMBER_DICTS,
    END_OF_STRING,
    ZEROS
)


class NumberConverter:

    def __init__(self, language="RU"):
        if language not in ("RU", "UA"):
            raise TypeError(f"The language is not supported: {language}")
        self.number_system_name = NUMBER_SYSTEM_NAME[language]
        self.number_dict = NUMBER_DICTS[language]
        self.thousand_end  = END_OF_STRING["thousand"][language]
        self.million_end  = END_OF_STRING["million"][language]
        self.end_of_string = END_OF_STRING["end_of_string"][language]


    def __get_simple_number(self, n):
        return self.number_dict[int(n)][0]

    def __get_from_ten_to_twenty(self, n):
        n = str(int(n))
        first, second = map(int, n)
        return self.number_dict[first][1][second]

    def __get_dozen_dict(self, n):
        n = str(int(n))
        first, second = map(int, n)
        if first and second != 0:
            result = self.number_dict[first][1]
            result += f" {self.number_dict[second][0]}"
            return result
        return self.number_dict[first][1]

    def __get_dozen_number(self, n):
        num_range = {
          self.__get_simple_number: [1, 10],
          self.__get_from_ten_to_twenty: [10, 20],
          self.__get_dozen_dict: [20, 100]
        }
        for key, value in num_range.items():
            if int(n) in range(value[0], value[1]):
                return key(n)
        return ""

    def __get_hundread_dict(self, n):
        result = self.number_dict[int(n[0])][2]
        result += f" {self.__get_dozen_number(n[1:])}"
        return result

    def __get_hundred_number(self, n):
        num_range = {
            self.__get_simple_number: [1, 10],
            self.__get_dozen_number: [10, 100],
            self.__get_hundread_dict: [100, 1000]
        }
        for key, value in num_range.items():
            if int(n) in range(value[0], value[1]):
                return key(n)
        return ZEROS

    def __split_number(self, number: int) -> list:
        """ Split number to simple, dozen and hundred """
        res = []
        n_without_zero = str(int(number))
        convert_function = (
          (self.__get_hundred_number, 3),
          (self.__get_simple_number, 1),
          (self.__get_dozen_number, 2)
        )
        while n_without_zero:
            x = int(len(n_without_zero)) % 3
            slice_num = convert_function[x][1]
            res.append(convert_function[x][0](n_without_zero[0: slice_num]))
            n_without_zero = n_without_zero[slice_num:]
        return res

    def convert(self, number):
        try:
            int(number)
        except ValueError:
            raise ValueError(f"The {number} is not number")
        numbers = self.__split_number(number)
        length = int(len(numbers))
        if length > 34:
            raise ValueError(f"The number {number} is too big")
        output = ""
        for i in numbers:
            if i == ZEROS:
                length -= 1
                continue
            output += self.__add_clarification(i, length)
            length -= 1
        return output.replace('  ', ' ')

    def __add_clarification(self, n, length):
        if length == 2:
            return f"{self.__check_end_of_thousand(n, length)} "
        elif length > 2:
            return f"{n} {self.__check_end_of_string(n, length)} "
        return str(n)

    def __check_end_of_thousand(self, n, length):
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        for k in self.thousand_end:
            if re.fullmatch(k, simple_number[index]):
                result = re.sub(k, self.thousand_end[k][1], n) + ' '
                result += self.number_system_name[length] + self.thousand_end[k][0]
                return result
        return f"{n} {self.number_system_name[length]}"

    def __check_end_of_string(self, n, length):
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        for k in self.million_end:
            if re.fullmatch(k, simple_number[index]):
                return self.number_system_name[length] + self.million_end[k]
        
        return f'{self.number_system_name[length]}{self.end_of_string}'
