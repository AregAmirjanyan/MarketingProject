# Logger Documentation

This documentation provides an overview of the `CustomFormatter` class, its attributes, methods, and an example of how to use it for logging.



## CustomFormatter Class

The `CustomFormatter` class provides a custom formatter for informative logging.

#### Attributes

- `grey`: ANSI escape sequence for grey color.
- `violet`: ANSI escape sequence for violet color.
- `yellow`: ANSI escape sequence for yellow color.
- `red`: ANSI escape sequence for red color.
- `bold_red`: ANSI escape sequence for bold red color.
- `reset`: ANSI escape sequence to reset text color.
- `format`: Default log format string.
- `FORMATS`: Dictionary mapping log levels to colored format strings.

#### Methods

#### `format(record)`

Formats the log record and returns the formatted (colored) output.

