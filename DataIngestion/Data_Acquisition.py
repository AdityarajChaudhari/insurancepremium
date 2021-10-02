import pandas as pd
from InsurancePremium.Logging.Logs import log_class
import os


class LoadingRaw:
    """Class for loading raw data from local source
    """

    def __init__(self):
        self.folder = '../LogFiles/'
        self.filename = 'DataAcquisition_log.txt'

        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        self.log_object = log_class(self.folder, self.filename)

    def get_data(self):
        try:
            self.log_object.create_log_file("""Loading training data set from the local source into pandas DataFrame""")
            df = pd.read_csv('../Dataset/insurance_dataset.csv')
            return df
        except Exception as e:
            self.log_object.create_log_file("The error is :- " + str(e))
            raise e



















