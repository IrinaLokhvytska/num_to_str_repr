# -*- coding: utf-8 -*-
""" Convert number to the string representation """
import re

from num_to_str_repr.constant import (
    NUMBER_SYSTEM_NAME,
    NUMBER_DICTS,
    END_OF_NUMBER,
    ZEROS
)


class NumberConverter:
    """ Convert number to the string representation """

    def __init__(self, language: str="RU") -> None:
        """ Init NumberConverter class """
        if language not in ("RU", "UA"):
            raise TypeError(f"The language is not supported: {language}")
        self.number_system_name = NUMBER_SYSTEM_NAME[language]
        self.number_dict = NUMBER_DICTS[language]
        self.end_of_number = END_OF_NUMBER[language]

    def convert(self, number: float) -> str:
        """ Convert number to the string representation """
        self.__validate_if_number_is_valid(number)
        if "." not in str(number):
            return self.__return_string_representation(int(number))
        start_n, end_n = map(int, str(number).split("."))
        if not end_n:
            # For example 2.00 is the same as 2
            return self.__return_string_representation(start_n)
        int_end = self.__return_string_representation(start_n)
        float_end = self.__return_string_representation(end_n, max_length=1)
        real_output = self.__check_end_of_string_for_float_number(int_end, start_n)
        float_output = self.__check_end_of_string_for_float_number(float_end, end_n, False)
        return f"{real_output} {float_output}".replace('  ', ' ')
    
    def __check_end_of_string_for_float_number(self, float_str:str, number:int, real:bool=True) -> str:
        """ Check the end of string for the real and float number """
        if real:
            str_end = self.end_of_number["float_end"]["int"]
        else:
            str_end = self.end_of_number["float_end"]["float"][len(str(number))-1]
        str_end = str_end[0] if float_str.endswith("один") else str_end[1]
        thousand_end = self.end_of_number["thousand"]
        for k in thousand_end:
            if float_str.endswith(k):
                float_str = re.sub(k, thousand_end[k][1], float_str)
        output = f'{float_str} {str_end}'
        return output

    def __return_string_representation(self, number: float, max_length: int=34) -> str:
        """ Return string representation """
        numbers = self.__split_number(abs(number))
        length = int(len(numbers))
        self.__validate_if_number_is_supported(number, length, max_length)
        output = "" if number >= 0 else f"{self.end_of_number['start_of_string']} "
        for i in numbers:
            if i == ZEROS:
                length -= 1
                continue
            output += self.__add_number_system_name(i, length)
            length -= 1
        return output.replace('  ', ' ')

    def __validate_if_number_is_valid(self, number: float) -> None:
        """ Validate if number is int or float, otherwise raise exception """
        try:
            float(number)
        except ValueError:
            raise ValueError(f"The {number} is not number")

    def __validate_if_number_is_supported(self, number: float, length: int, max_length:int) -> None:
        """ The supported number for int is in range [-googol, googol] """
        if length > max_length:
            raise ValueError(f"The number {number} is too big")

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

    def __get_simple_number(self, n: str) -> str:
        """ Return the string representation for the sipmle number [0, 9] """
        return self.number_dict[int(n)][0]

    def __get_dozen_number(self, n: str) -> str:
        """ Return the string representation for the sipmle number [10, 99] """
        num_range = {
          self.__get_simple_number: [1, 10],
          self.__get_from_ten_to_twenty: [10, 20],
          self.__get_dozen_dict: [20, 100]
        }
        for key, value in num_range.items():
            if int(n) in range(value[0], value[1]):
                return key(str(n))
        return ""

    def __get_from_ten_to_twenty(self, n: str) -> str:
        """ Return the string representation for the sipmle number [10, 19] """
        first, second = int(n[0]), int(n[1])
        return self.number_dict[first][1][second]

    def __get_dozen_dict(self, n: str) -> str:
        """ Return the string representation for the sipmle number [20, 99] """
        first, second = int(n[0]), int(n[1])
        if first and second != 0:
            result = self.number_dict[first][1]
            result += f" {self.number_dict[second][0]}"
            return result
        return self.number_dict[first][1]

    def __get_hundred_number(self, n: str) -> str:
        """ Return the string representation for the sipmle number [100, 999] """
        num_range = {
            self.__get_simple_number: [1, 10],
            self.__get_dozen_number: [10, 100],
            self.__get_hundread_dict: [100, 1000]
        }
        for key, value in num_range.items():
            if int(n) in range(value[0], value[1]):
                return key(str(n))
        return ZEROS

    def __get_hundread_dict(self, n: str) -> str:
        """ Return the string representation for the sipmle number [100, 999] """
        result = self.number_dict[int(n[0])][2]
        result += f" {self.__get_dozen_number(n[1:])}"
        return result

    def __add_number_system_name(self, n: str, length: int) -> str:
        """ Add number system name """
        if length == 2:
            return f"{self.__check_end_of_thousand(n, length)} "
        elif length > 2:
            return f"{n} {self.__check_end_of_string(n, length)} "
        return str(n)

    def __check_end_of_thousand(self, n: str, length: int) -> str:
        """ Add end of the string for the thousand """
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        thousand_end = self.end_of_number["thousand"]
        for k in thousand_end:
            if re.fullmatch(k, simple_number[index]):
                result = re.sub(k, thousand_end[k][1], n) + ' '
                result += self.number_system_name[length] + thousand_end[k][0]
                return result
        return f"{n} {self.number_system_name[length]}"

    def __check_end_of_string(self, n: str, length: int) -> str:
        """ Add end of the string for the million and more """
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        million_end = self.end_of_number["million"]
        for k in million_end:
            if re.fullmatch(k, simple_number[index]):
                return self.number_system_name[length] + million_end[k]
        return f'{self.number_system_name[length]}{self.end_of_number["end_of_string"]}'
