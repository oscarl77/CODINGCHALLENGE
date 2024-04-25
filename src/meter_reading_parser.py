import re
from src.flow_parser import FlowParser
from datetime import datetime


class MeterReadingParser(FlowParser):
    """Class for parsing meter reading data from a flow message text file.

    Attributes:
        filename (str): text file containing meter reading data.
        parsed_meter_readings (dictionary (str: str)): dictionary that will store processed 
        meter reading data.
    
    Methods:
        __init__()
        parse_file()
        
    """

    def __init__(self, filename):
        """Initialises the instance based on the meter reading file and
        an empty dictionary along with it.

        Args:
            filename (str): text file containing flow message data.
        """
        super().__init__(filename)
        self.parsed_meter_readings = {}

    def parse_file(self):
        """Parses raw meter reading data into desired dictionary format.

        Returns:
            dictionary (dict of str: str): Contains key-value pairs for desired metrics
            e.g highest meter reading.
        """
        
        with open(self.filename, 'r') as file:
            meter_reading_contents = file.read().splitlines()

        meter_total = self._get_count_of_meters(meter_reading_contents)

        valid_readings_sum = self._get_readings_sum(meter_reading_contents, 'V')
        invalid_readings_sum = self._get_readings_sum(meter_reading_contents, 'F')
        highest_valid_reading = self._get_highest_valid_reading(meter_reading_contents)
        lowest_valid_reading = self._get_lowest_valid_reading(meter_reading_contents)
        oldest_reading = self._get_oldest_meter_reading(meter_reading_contents)
        newest_reading = self._get_newest_meter_reading(meter_reading_contents)

        self.parsed_meter_readings['Meter count'] = meter_total
        self.parsed_meter_readings['Sum of valid meter readings'] = valid_readings_sum
        self.parsed_meter_readings['Sum of invalid meter readings'] = invalid_readings_sum
        self.parsed_meter_readings['Highest valid meter reading'] = highest_valid_reading
        self.parsed_meter_readings['Lowest valid meter reading'] = lowest_valid_reading
        self.parsed_meter_readings['Oldest meter reading'] = oldest_reading
        self.parsed_meter_readings['Most recent meter reading'] = newest_reading

        return self.parsed_meter_readings


    def _get_count_of_meters(self, file_contents):
        """Sums up the number of meters in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            int: total number of meters in the file.
        """
        meter_count = 0
        for line in file_contents:
            if 'METER|' in line:
                meter_count += 1
        return meter_count


    def _get_readings_sum(self, file_contents, validity):
        """Sums up all the valid or invalid meter readings in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.
            validity (str): can take one of two string values, 
            'V' = valid, 'F' = invalid.

        Returns:
            float: Total of the valid or invalid meter readings.
        """
        meter_readings_sum = 0
        valid_readings_pattern = r'(\d+\.\d+)\|(\d+)\|' + validity 
        # check each line for match corresponding to VALUE|DATE|STATUS
        # regular expression
        for line in file_contents:
            match = re.search(valid_readings_pattern, line)
            if match: 
                meter_readings_sum += float(match.group(1)) # i.e VALUE
        return meter_readings_sum
    

    def _get_highest_valid_reading(self, file_contents):
        """Returns the highest valid meter reading in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            float: highest valid reading in text file if it exists, otherwise
            returns str.
        """
        global_max = 0
        valid_readings_pattern = r'(\d+\.\d+)\|(\d+)\|V'
        # check each line for a match corresponding to the VALUE|DATE|STATUS(V)
        # regular expression
        for line in file_contents:
            match = re.search(valid_readings_pattern, line)
            if match:
                local_max = float(match.group(1)) # i.e VALUE
                if local_max > global_max:
                    global_max = local_max
        if global_max == 0:
            return 'N/A'
        return global_max
    

    def _get_lowest_valid_reading(self, file_contents):
        """Returns the lowest valid meter reading in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            float: lowest valid reading in text file if it exists, otherwise
            returns str.
        """
        global_min = float('inf')
        valid_readings_pattern = r'(\d+\.\d+)\|(\d+)\|V'
        # check each line for a match corresponding to the VALUE|DATE|STATUS(F)
        # regular expression
        for line in file_contents:
            match = re.search(valid_readings_pattern, line)
            if match:
                local_min = float(match.group(1)) # i.e VALUE
                if local_min < global_min:
                    global_min = local_min
        if global_min == float('inf'):
            return 'N/A'
        return global_min
    

    def _get_oldest_meter_reading(self, file_contents):
        """Returns the oldest meter reading in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            float: oldest meter reading in the file if it exists, 
            otherwise returns str.
        """
        oldest_date = self._get_oldest_date(file_contents)
        if oldest_date is None:
            return 'N/A'
        oldest_date_pattern = r'(\d+\.\d+)\|' + oldest_date
        # check each line for VALUE|DATE regular expression
        for line in file_contents:
            match = re.search(oldest_date_pattern, line)
            if match:
                oldest_reading = match.group(1) # i.e VALUE
        return float(oldest_reading)

    def _get_oldest_date(self, file_contents):
        """Returns the oldest date in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            str: oldest date in the file.
        """
        date_pattern = r'(\d+)\|(V|F)'
        global_oldest = datetime.now().date()
        date_found = False
        # check each line for a match to the DATE|STATUS regular expression
        for line in file_contents:
            match = re.search(date_pattern, line)
            if match:
                date_found = True
                date_string = match.group(1)
                local_oldest = datetime.strptime(date_string, '%Y%m%d').date()
                if local_oldest < global_oldest:
                    global_oldest = local_oldest
        if not date_found:
            return None
        return global_oldest.strftime('%Y%m%d')
    

    def _get_newest_meter_reading(self, file_contents):
        """Returns the most meter reading in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            float: most recent meter reading in the file if it exists,
            otherwise returns str.
        """
        newest_date = self._get_newest_date(file_contents)
        if newest_date is None:
            return 'N/A'
        newest_date_pattern = r'(\d+\.\d+)\|' + newest_date
        # check each line for a match to the VALUE|DATE regular expression
        for line in file_contents:
            match = re.search(newest_date_pattern, line)
            if match:
                newest_reading = match.group(1) # i.e VALUE
        return float(newest_reading)

    def _get_newest_date(self, file_contents):
        """Returns the most recent date in the file.

        Args:
            file_contents (list[str]): list of each line from the meter
            readings text file.

        Returns:
            str: Most recent date in the file.
        """
        date_pattern = r'(\d+)\|(V|F)'
        global_newest = datetime.strptime('00010101', '%Y%m%d').date()
        date_found = False
        # check each line for a match to the DATE|STATUS regular expression
        for line in file_contents:
            match = re.search(date_pattern, line)
            if match:
                date_found = True
                date_string = match.group(1)
                local_newest = datetime.strptime(date_string, '%Y%m%d').date()
                if local_newest > global_newest:
                    global_newest = local_newest
        if not date_found:
            return None
        return global_newest.strftime('%Y%m%d')