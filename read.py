import sys

import pandas as pd

class NoaaReport:

    def set_observatories(self, data):
        observatories = []
        for i in data:
            if i[4].isalpha() and len(i[4]) == 3:
                observatories.append(i[4])
            else:
                observatories.append("None")
        return observatories

    def set_Qs(self, data):
        Qs = []
        for i in data:
            if len(i[5]) == 1:
                Qs.append(i[5])
            else:
                Qs.append("None")

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
                del event[1]

    observatories = []
    for i in data:
        if i[4].isalpha() and len(i[4]) == 3:
            observatories.append(i[4])
        else:
            observatories.append("None")

    Qs = []
    for i in data:
        if len(i[5]) == 1:
            Qs.append(i[5])
        else:
            Qs.append("None")

    particulars = []
    for i in data:
        try:
            last_index = len(i) - 1
            if not i[last_index].isdigit() and len(i[last_index]) != 4:
                particula = i[8] + " " + i[9]
            else:
                particula = i[8]
            particulars.append(particula)
        except IndexError:
            particulars.append("None")

    reg = []
    for i in data:
        try:
            last_index = len(i) - 1
            if i[last_index].isdigit() and len(i[last_index]) == 4:
                reg.append(i[last_index])
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
        "Q": Qs,
        "type": [i[6] for i in data],
        "loc/freq": [i[7] for i in data],
        "particulars": particulars,
        "reg": reg
    }
    df = pd.DataFrame(final_data)
    print(df)


if __name__ == "__main__":
    main()
