
class FlowParser():
    """Class for parsing flow message data from a given text file.

    Attributes:
        filename (str): text file containing flow message data.     
    """
    
    def __init__(self, filename):
        """Initialises FlowParser object based on the given filename.

        Args:
            filename (str): text file containing flow message data.
        """
        self.filename = filename
