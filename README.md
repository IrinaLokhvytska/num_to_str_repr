# NUM_TO_STR_REPR 

Simple package that converts numbers (int and float)
to the Russian and Ukrainian string representation.

The supported number in range [-googol, googol].

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install num-to-str-repr.

```bash
pip install num-to-str-repr
```

## Example

By default the language is Russian.
```bash
from num_to_str_repr.number_converter import NumberConverter

converter = NumberConverter()

# Int number
converter.convert(789_567_361_890_000_321)
"семьсот восемьдесят девять квадриллионов пятьсот шестьдесят семь триллионов триста шестьдесят один миллиард восемьсот девяносто миллионов триста двадцать один"

# Float number
converter.convert(534.321)
"пятьсот тридцать четыре целых триста двадцать одна тысячная"
```

```bash
from num_to_str_repr.number_converter import NumberConverter

converter = NumberConverter("UA")

# Int number
converter.convert(789_567_361_890_000_321)
"сімсот вісімдесят дев'ять квадрильйонів п'ятсот шістдесят сім трильйонів триста шістдесят один мільярд вісімсот дев'яносто мільйонів триста двадцять один"

# Float number
converter.convert(132.41)
"сто тридцять дві цілих сорок одна сота"
```

## Run tests
```bash
python3 -m unittest tests.num_to_str_repr
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
