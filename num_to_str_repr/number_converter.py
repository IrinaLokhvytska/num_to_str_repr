# -*- coding: utf-8 -*-
''' Convert number to string '''
import re

from constant import NUMBER_CLARIFICATION, NUMBER_DICTS


class NumberConverter:

    def __get_simple_number(self, n):
        return NUMBER_DICTS[int(n)][0]

    def __get_from_ten_to_twenty(self, n):
        n = str(int(n))
        first, second = map(int, n)
        return NUMBER_DICTS[first][1][second]

    def __get_dozen_dict(self, n):
        n = str(int(n))
        first, second = map(int, n)
        if first and second != 0:
            result = NUMBER_DICTS[first][1]
            result += ' ' + NUMBER_DICTS[second][0]
            return result
        else:
            return NUMBER_DICTS[first][1]

    def __get_dozen_number(self, n):
        num_range = {
          self.__get_simple_number: [1, 10],
          self.__get_from_ten_to_twenty: [10, 20],
          self.__get_dozen_dict: [20, 100]
        }
        for key, value in num_range.items():
            if int(n) in range(value[0], value[1]):
                return key(n)
        return ''

    def __get_hundread_dict(self, n):
        result = NUMBER_DICTS[int(n[0])][2]
        result += ' {}'.format(self.__get_dozen_number(n[1:]))
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
        return '000'

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
        numbers = self.__split_number(number)
        length = int(len(numbers))
        if length > 34:
            return 'The number {} too big'.format(number)
        output = ''
        for i in numbers:
            if i == '000':
                length -= 1
                continue
            output += self.__add_clarification(i, length)
            length -= 1
        return output.replace('  ', ' ')

    def __add_clarification(self, n, length):
        output = ''
        if length == 2:
            output += self.__check_end_of_thousand(n, length) + ' '
        elif length > 2:
            output += n + ' ' + self.__check_end_of_string(n, length) + ' '
        else:
            output += n
        return output

    def __check_end_of_thousand(self, n, length):
        ends = {
          'один': ('а', 'одна'),
          'два': ('и', 'две'),
          'три': ('и', 'три'),
          'четыре': ('и', 'четыре')
        }
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        for k in ends:
            if re.fullmatch(k, simple_number[index]):
                result = re.sub(k, ends[k][1], n) + ' '
                result += NUMBER_CLARIFICATION[length] + ends[k][0]
                return result
        return n + ' ' + NUMBER_CLARIFICATION[length]

    def __check_end_of_string(self, n, length):
        ends = {'один': '', 'два': 'а', 'три': 'а', 'четыре': 'а'}
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        for k in ends:
            if re.fullmatch(k, simple_number[index]):
                return NUMBER_CLARIFICATION[length] + ends[k]
        return '{0}{1}'.format(NUMBER_CLARIFICATION[length], 'ов')
