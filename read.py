import sys

from functools import wraps

import pandas as pd

class NoaaReport:

    def __init__(self):
        self.filename = sys.argv[1]
        self.data = []

    def check_data(self):
        """Checks if the data has already been saved. """
        if len(self.data) == 0:
            self.read_data()

        return True

    def read_data(self):
        """
        Reads the noaa report.
        """

        with open(self.filename) as _file:
            for line in _file.readlines():
                sep = line.split()

                try:
                    if not sep[0].startswith(":") and not sep[0].startswith("#"):
                        self.data.append(sep)
                except IndexError:
                    pass

            for event in self.data:
                if event[1] == "+":
                    event[0] += " +"
                    del event[1]

    def set_Qs(self):
        Qs = []
        for info in self.data:
            if len(info[5]) == 1:
                Qs.append(info[5])
            else:
                Qs.append("None")
        
        return Qs

    def set_observatories(self):
        index = 0
        observatories = []
        while index < len(self.data):
            if len(self.data[index][4]) == 3:
                observatories.append(self.data[index][4])
                index += 1
            else:
                del self.data[index]

        return observatories

    def set_particulares(self):
        particulars = []
        for info in self.data:
            try:
                last_index = len(info) - 1
                if not info[last_index].isdigit() or len(info[last_index]) != 4:
                    if len(info) > 9:
                        particula = info[last_index - 1] + " " + info[last_index]
                    else:
                        particula = info[last_index]
                else:
                    particula = info[last_index - 1]

                particulars.append(particula)
            except IndexError:
                particulars.append("None")
        
        return particulars

    def set_regions(self):
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

def main():
    """
    Reads the noaa report.
    """
    with open(sys.argv[1]) as _file:
        data = []
        for line in _file.readlines():
            sep = line.split()

            try:
                if not sep[0].startswith(":") and not sep[0].startswith("#"):
                    data.append(sep)
            except IndexError:
                pass

        for event in data:
            if event[1] == "+":
                event[0] += " +"
                del event[1]

    index = 0
    observatories = []
    while index < len(data):
        if len(data[index][4]) == 3:
            observatories.append(data[index][4])
            index += 1
        else:
            del data[index]

    qs = []
    for info in data:
        if len(info[5]) == 1:
            qs.append(info[5])
        else:
            qs.append("None")

    particulars = []
    for info in data:
        try:
            last_index = len(info) - 1
            if not info[last_index].isdigit() or len(info[last_index]) != 4:
                if len(info) > 9:
                    particula = info[last_index - 1] + " " + info[last_index]
                else:
                    particula = info[last_index]
            else:
                particula = info[last_index - 1]

            particulars.append(particula)
        except IndexError:
            particulars.append("None")

    reg = []
    for info in data:
        try:
            last_index = len(info) - 1
            if info[last_index].isdigit() and len(info[last_index]) == 4:
                reg.append(info[last_index])
            else:
                reg.append("None")
        except IndexError:
            reg.append("None")

    final_data = {
        "event": [i[0] for i in data],
        "begin": [i[1] for i in data],
        "max": [i[2] for i in data],
        "end": [i[3] for i in data],
        "obs": observatories,
        "Q": qs,
        "type": [i[6] for i in data],
        "loc/freq": [i[7] for i in data],
        "particulars": particulars,
        "reg": reg
    }

    columns = ["event", "begin", "max",
               "end", "obs", "Q", "type",
               "loc/freq", "particulars", "reg"]
    df = pd.DataFrame(final_data, columns=columns)
    print(df)


if __name__ == "__main__":
    main()
