import argparse
from src.meter_reading_parser import MeterReadingParser

class MeterReadingsProcessor():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='processes flow message meter readings data')
        self.parser.add_argument('filepath', type=str, help='path to input file')
        self.args = self.parser.parse_args()

    def run(self):
        meter_reading_parser = MeterReadingParser(self.args.filepath)
        processed_meter_readings = meter_reading_parser.parse_file()
        print(processed_meter_readings)