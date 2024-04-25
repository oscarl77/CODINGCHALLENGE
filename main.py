import argparse
import textwrap
from parsers.meter_reading_parser import MeterReadingParser


def main():
    filename = 'flows/test_readings'
    meter_readings = MeterReadingParser(filename)
    meter_readings.parse_meter_readings()
    

if __name__ == "__main__":
    main()