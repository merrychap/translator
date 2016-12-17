# Translator

### Description
This script translates source code (for instance, python, c++) into highlighted html.
First of all, you have to specify structure of your language. It means, that you
tell what colors should be used for words, digits, background and so on.

### Requirements
- Python 3.*

### Arguments of launching
Argument | Description
-------- | -----------
--ext | Key for extension of file with source code
--file | File with source code
--descr | Language description

### Supported languages
- Python
- C++

### How to launch application?
```sh
$ python3 translator.py [--keys]
```

### Structure
Structure represents following json file:
```json
{
    "basic_colors": {
        "digits": "#digits_color",
        "comments": "#comments_color",
        "background": "#bacground_color",
        "strings": "#strings_color",
        "text": "#text_color"
    },
    "reserved": [
        ["#color1", ["list", "of", "words", "with", "that", "color"]],
        ["#color2", ["another", "list", "with", "different", "colors"]]
    ]
}
```
