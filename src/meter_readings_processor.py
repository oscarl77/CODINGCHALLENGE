import argparse
import pprint
from src.meter_reading_parser import MeterReadingParser

class MeterReadingsProcessor():
    """Command-line utility for processing meter readings text file

    Attributes:
        parser (argparse.ArgumentParser):  argument parser for command-line arguments.
        args (argparse.Namespace): parsed command-line arguments.

    Methods:
        __init__()
        run()
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='processes flow message meter readings data')
        self.parser.add_argument('filepath', type=str, help='path to input file')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Display output in more readable format')
        self.args = self.parser.parse_args()

    def run(self):
        meter_reading_parser = MeterReadingParser(self.args.filepath)
        processed_meter_readings = meter_reading_parser.parse_file()
        if self.args.verbose:
            print(pprint.pformat(processed_meter_readings))
        else:
            print(processed_meter_readings)