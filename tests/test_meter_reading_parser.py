import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
from src.meter_reading_parser import MeterReadingParser

class TestMeterReadingParser(unittest.TestCase):

    def setUp(self):
        """Creates temporary files to be used in the unit tests.
        """
        self.temp_files = []
        temp_file_content_0 = ("HEADER|\n"
        "METER|001|\nREADING|002|520.6|20221108|V|\n"
        "METER|003|\nREADING|004|1865.2|20220302|V|\n"
        "METER|005|\nREADING|006|944.0|20220711|F|\n"
        "METER|007|\nREADING|008|284.1|20221111|V|\n"
        "METER|009|\nREADING|010|765.9|20220122|F|\n"
        "FOOTER|")
        temp_file_content_1 = ("HEADER|\n"
        "METER|011|\nREADING|012|1130.0|20221213|V|\n"
        "METER|013|\nREADING|014|875.5|20220425|V|\n"
        "METER|015|\nREADING|016|112.2|20220112|V|\n"
        "METER|017|\nREADING|018|50.8|20221108|V|\n"
        "METER|019|\nREADING|020|343.0|20221010|V|\n"
        "METER|021|\nREADING|022|465.9|20220901|V|\n"
        "FOOTER|")
        temp_file_content_2 = ("HEADER|\n"
        "METER|023|\nREADING|024|818.0|20221223|F|\n"
        "METER|025|\nREADING|026|593.5|20220511|F|\n"
        "METER|027|\nREADING|028|4373.2|20220828|F|\n"
        "METER|029|\nREADING|030|9476.8|20221105|F|\n"
        "METER|031|\nREADING|032|634.0|20221108|F|\n"
        "METER|033|\nREADING|034|1205.9|20221103|F|\n"
        "FOOTER|")  
        temp_file_content_3 = ("HEADER|\n"
        "METER|039|\nREADING|040|987.4|20220417|V|\n"
        "FOOTER|")
        temp_file_content_4 = ("HEADER|\n"
        "FOOTER|")
        temp_file_content_5 = ("")
        self.temp_file_contents = [temp_file_content_0,
                              temp_file_content_1, 
                              temp_file_content_2,
                              temp_file_content_3,
                              temp_file_content_4,
                              temp_file_content_5]
        for contents in self.temp_file_contents:
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.write(contents)
            temp_file.close()
            # We store the temp_file name and its contents in a tuple within
            # this a list of files
            self.temp_files.append((temp_file, contents))
    
    def test_meter_reading_parser_default(self):
        expected_output_0 = {'Meter count': 5,
                             'Sum of valid meter readings': 2669.9,
                             'Sum of invalid meter readings': 1709.9,
                             'Highest valid meter reading': 1865.2,
                             'Lowest valid meter reading': 284.1,
                             'Oldest meter reading': 765.9,
                             'Most recent meter reading': 284.1}
        temp_file = self.temp_files[0][0]
        temp_file_content = self.temp_files[0][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_0)
        os.remove(temp_file_path)
        
    def test_meter_reading_parser_all_valid(self):
        expected_output_1 = {'Meter count': 6,
                             'Sum of valid meter readings': 2977.4,
                             'Sum of invalid meter readings': 0,
                             'Highest valid meter reading': 1130.0,
                             'Lowest valid meter reading': 50.8,
                             'Oldest meter reading': 112.2,
                             'Most recent meter reading': 1130.0}
        temp_file = self.temp_files[1][0]
        temp_file_content = self.temp_files[1][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_1)
        os.remove(temp_file_path)

    def test_meter_reading_parser_all_invalid(self):
        expected_output_2 = {'Meter count': 6,
                             'Sum of valid meter readings': 0,
                             'Sum of invalid meter readings': 17101.4,
                             'Highest valid meter reading': 'N/A',
                             'Lowest valid meter reading': 'N/A',
                             'Oldest meter reading': 593.5,
                             'Most recent meter reading': 818.0}
        temp_file = self.temp_files[2][0]
        temp_file_content = self.temp_files[2][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_2)
        os.remove(temp_file_path)

    def test_meter_reading_parser_one_reading(self):
        expected_output_3 = {'Meter count': 1,
                             'Sum of valid meter readings': 987.4,
                             'Sum of invalid meter readings': 0,
                             'Highest valid meter reading': 987.4,
                             'Lowest valid meter reading': 987.4,
                             'Oldest meter reading': 987.4,
                             'Most recent meter reading': 987.4}
        temp_file = self.temp_files[3][0]
        temp_file_content = self.temp_files[3][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_3)
        os.remove(temp_file_path)
    
    def test_meter_reading_parser_no_meter(self):
        expected_output_4 = {'Meter count': 0,
                            'Sum of valid meter readings': 0,
                            'Sum of invalid meter readings': 0,
                            'Highest valid meter reading': 'N/A',
                            'Lowest valid meter reading': 'N/A',
                            'Oldest meter reading': 'N/A',
                            'Most recent meter reading': 'N/A'}
        temp_file = self.temp_files[4][0]
        temp_file_content = self.temp_files[4][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_4)
        os.remove(temp_file_path)

    def test_meter_reading_parser_empty_flow(self):
        expected_output_5 = {'Meter count': 0,
                           'Sum of valid meter readings': 0,
                           'Sum of invalid meter readings': 0,
                           'Highest valid meter reading': 'N/A',
                           'Lowest valid meter reading': 'N/A',
                           'Oldest meter reading': 'N/A',
                           'Most recent meter reading': 'N/A'}
        temp_file = self.temp_files[5][0]
        temp_file_content = self.temp_files[5][1]
        temp_file_path = temp_file.name
        with patch("builtins.open", mock_open(read_data=temp_file_content)):
            meter_reading_parser = MeterReadingParser(temp_file_path)
            result = meter_reading_parser.parse_file()
            self.assertEqual(result, expected_output_5)
        os.remove(temp_file_path)