from abc import ABC, abstractmethod

class FlowParser(ABC):
    """Abstract class for parsing flow message data from a given text file.
    
    This abstract class acts as a template for subclasses that parse different
    kinds of flow messages; In this case we have created one subclass
    MeterReadingParser.
    """
    
    @abstractmethod
    def __init__(self, filename):
        """Initialises FlowParser object based on the given filename.

        Args:
            filename (str): text file containing flow message data.
        """
        self.filename = filename

    @abstractmethod
    def parse_file(self):
        pass