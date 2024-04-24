import argparse
from src.learning import FlowParser


def main():
    filename = 'flows/meter_readings'
    flow_parser = FlowParser()

    flow_parser.parse_meter_readings(filename)

if __name__ == "__main__":
    main()