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
converter.convert(number)
```

By default the language is Russian.
```bash
from num_to_str_repr.number_converter import NumberConverter

converter = NumberConverter("UA")
converter.convert(number)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
