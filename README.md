# Reading Meter Parser command-line utility

This programme analyses the content of flow messages contatining meter reading
data and extracts and outputs the relevant data points in a readable format.

## Usage

To use the command-line utility, run the following command:

    python main.py flows/filename

where 'filename' is the text file you want to input.

### Options

- '-h, --help': Display help message
- 'v, --verbose': Display output in more readable format

### Examples

    python main.py -h
    python main.py --help

    python main.py flows/filename -v
    python main.py flows/filename --verbose