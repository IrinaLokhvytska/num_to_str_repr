# -*- coding: utf-8 -*-
''' Convert number to string '''
import re


class NumberConverter:
    def __init__(self, number):
        self.number = number
        self.dict_numbers = {}
        self.__complete_dictionary()

    simple_number = (
        'ноль',
        'один',
        'два',
        'три',
        'четыре',
        'пять',
        'шесть',
        'семь',
        'восемь',
        'девять'
    )

    number_clarification = {
        2: 'тысяч',
        3: 'миллион',
        4: 'миллиард',
        5: 'триллион',
        6: 'квадриллион',
        7: 'квинтиллион',
        8: 'секстиллион',
        9: 'септиллион',
        10: 'октиллион',
        11: 'нониллион',
        12: 'дециллион',
        13: 'ундециллион',
        14: 'додециллион',
        15: 'тредециллион',
        16: 'кваттуордециллион',
        17: 'квиндециллион',
        18: 'cедециллион',
        19: 'септдециллион',
        20: 'дуодевигинтиллион',
        21: 'ундевигинтиллион',
        22: 'вигинтиллион',
        23: 'анвигинтиллион',
        24: 'дуовигинтиллион',
        25: 'тревигинтиллион',
        26: 'кватторвигинтиллион',
        27: 'квинвигинтиллион',
        28: 'сексвигинтиллион',
        29: 'септемвигинтиллион',
        30: 'октовигинтиллион',
        31: 'новемвигинтиллион',
        32: 'тригинтиллион',
        33: 'антригинтиллион',
        34: 'гугол'
    }

    def __complete_dictionary(self):
        for i in range(10):
            self.dict_numbers[i] = []
            self.dict_numbers[i].append(self.simple_number[i])
            if i == 0:
                continue
            else:
                self.__complete_dozen(i)
                self.__complete_hundred(i)

    def __complete_dozen_for_one(self, i):
        end = 'надцать'
        dozens = []
        helper = {
            0: 'десять',
            1: '{0}{1}'.format(self.simple_number[1], end),
            2: '{0}{1}{2}'.format(self.simple_number[2][:-1], 'е', end),
            3: '{0}{1}'.format(self.simple_number[3], end),
        }
        for y in range(10):
            if y in helper:
                dozens.append(helper[y])
            else:
                dozens.append('{0}{1}'.format(self.simple_number[y][:-1], end))
        self.dict_numbers[i].append(dozens)

    def __complete_dozen(self, i):
        helper = {
            2: '{0}{1}'.format(self.simple_number[2], 'дцать'),
            3: '{0}{1}'.format(self.simple_number[3], 'дцать'),
            4: 'сорок',
            9: '{0}{1}'.format(self.simple_number[9][:-2], 'носто'),
        }
        if i in helper:
            self.dict_numbers[i].append(helper[i])
        elif i == 1:
            self.__complete_dozen_for_one(i)
        else:
            self.dict_numbers[i].append('{0}{1}'.format(self.simple_number[i], 'десят'))

    def __complete_hundred(self, i):
        helper = {
          1: 'сто',
          2: '{0}{1}'.format(self.simple_number[2][:-1], 'ести'),
          3: '{0}{1}'.format(self.simple_number[3], 'ста'),
          4: '{0}{1}'.format(self.simple_number[4], 'ста')
        }
        if i in helper:
            self.dict_numbers[i].append(helper[i])
        else:
            self.dict_numbers[i].append('{0}{1}'.format(self.simple_number[i], 'сот'))

    def __get_simple_number(self, n):
        return self.dict_numbers[int(n)][0]

    def __get_from_ten_to_twenty(self, n):
        n = str(int(n))
        first, second = map(int, n)
        return self.dict_numbers[first][1][second]

    def __get_dozen_dict(self, n):
        n = str(int(n))
        first, second = map(int, n)
        if first and second != 0:
            result = self.dict_numbers[first][1]
            result += ' ' + self.dict_numbers[second][0]
            return result
        else:
            return self.dict_numbers[first][1]

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
        result = self.dict_numbers[int(n[0])][2]
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

    def __split_number(self):
        res = []
        n_without_zero = str(int(self.number))
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

    def convert(self):
        numbers = self.__split_number()
        length = int(len(numbers))
        if length > 34:
            return 'The number {} too big'.format(self.number)
        output = ''
        for i in numbers:
            if i == '000':
                length -= 1
                continue
            else:
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
                result += self.number_clarification[length] + ends[k][0]
                return result
        return n + ' ' + self.number_clarification[length]

    def __check_end_of_string(self, n, length):
        ends = {'один': '', 'два': 'а', 'три': 'а', 'четыре': 'а'}
        simple_number = n.split(' ')
        index = len(simple_number) - 1
        for k in ends:
            if re.fullmatch(k, simple_number[index]):
                return self.number_clarification[length] + ends[k]
        return '{0}{1}'.format(self.number_clarification[length], 'ов')
