import sys

import pandas as pd

class NoaaReport:
    """Read noaa report.
    """

    def __init__(self):
        self.filename = sys.argv[1]
        self.data = []

    def _check_data(self):
        """Checks if the data has already been saved. """
        if len(self.data):
            return True

        self._read_data()

    def _read_data(self):
        """Reads the noaa report.
        """
        with open(self.filename) as _file:
            for line in _file.readlines():
                sep = line.split()

                try:
                    if (not sep[0].startswith(":") and
                            not sep[0].startswith("#")):

                        self.data.append(sep)
                except IndexError:
                    pass

            for event in self.data:
                if event[1] == "+":
                    event[0] += " +"
                    del event[1]

    def set_Qs(self):
        """TODO """
        self._check_data()
        Qs = []
        for info in self.data:
            if len(info[5]) == 1:
                Qs.append(info[5])
            else:
                Qs.append("None")
        return Qs

    def set_observatories(self):
        """TODO """
        self._check_data()
        index = 0
        observatories = []
        while index < len(self.data):
            if len(self.data[index][4]) == 3:
                observatories.append(self.data[index][4])
                index += 1
            else:
                del self.data[index]

        return observatories

    def set_particulars(self):
        """TODO """
        self._check_data()
        particulars = []
        for info in self.data:
            try:
                last_index = len(info) - 1
                if info[last_index].isdigit() and len(info[last_index]) == 4:
                    if len(info) > 10:
                        particula = (info[last_index - 2] + " " +
                                     info[last_index - 1])
                    else:
                        particula = info[last_index - 1]
                else:
                    if len(info) > 9:
                        particula = (info[last_index - 1] + " " +
                                     info[last_index])
                    else:
                        particula = info[last_index]

                particulars.append(particula)
            except IndexError:
                particulars.append("None")

        return particulars

    def set_regions(self):
        """TODO """
        self._check_data()
        reg = []
        for info in self.data:
            try:
                last_index = len(info) - 1
                if info[last_index].isdigit() and len(info[last_index]) == 4:
                    reg.append(info[last_index])
                else:
                    reg.append("None")
            except IndexError:
                reg.append("None")
        
        return reg

    def set_event(self):
        """TODO """
        self._check_data()
        return [i[0] for i in self.data]

    def set_begin(self):
        """TODO """
        self._check_data()
        return [i[1] for i in self.data]

    def set_max(self):
        """TODO """
        self._check_data()
        return [i[2] for i in self.data]

    def set_end(self):
        """TODO """
        self._check_data()
        return [i[3] for i in self.data]

    def set_type(self):
        """TODO """
        self._check_data()
        return [i[6] for i in self.data]

    def set_freq(self):
        """TODO """
        self._check_data()
        return [i[7] for i in self.data]

    def set_final_data(self):
        """TODO """
        self._check_data()

        # observatories must be declared first, because it changes the
        # data list.
        final_data = {
            "obs": self.set_observatories(),
            "event": self.set_event(),
            "begin": self.set_begin(),
            "max": self.set_max(),
            "end": self.set_end(),
            "Q": self.set_Qs(),
            "type": self.set_type(),
            "loc/freq": self.set_freq(),
            "particulars": self.set_particulars(),
            "reg": self.set_regions()
        }

        columns = ["event", "begin", "max",
                   "end", "obs", "Q", "type",
                   "loc/freq", "particulars", "reg"]

        df = pd.DataFrame(final_data, columns=columns)
        print(df)
        return df


if __name__ == "__main__":
    report = NoaaReport()
    report.set_final_data()
