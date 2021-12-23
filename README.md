# NUM_TO_STR_REPR 

Simple module that convert the number to the Russian and Ukrainian string representation.

Start number - 0, end number -googol.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install num-to-str-repr.

```bash
pip install num-to-str-repr
```

## Example

```bash
from num_to_str_repr.number_converter import NumberConverter

converter = NumberConverter()
converter.convert(789_567_361_890_000_321)
семьсот восемьдесят девять квадриллионов пятьсот шестьдесят семь триллионов триста шестьдесят один миллиард восемьсот девяносто миллионов триста двадцать один
```

By default the language is Russian.
```bash
from num_to_str_repr.number_converter import NumberConverter

converter = NumberConverter("UA")
converter.convert(789_567_361_890_000_321)
сімсот вісімдесят дев'ять квадрильйонів п'ятсот шістдесят сім трильйонів триста шістдесят один мільярд вісімсот дев'яносто мільйонів триста двадцять один
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
