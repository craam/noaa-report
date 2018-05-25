import pandas as pd


def main():
    """
    Reads the noaa report.
    """
    with open("20020102events.txt") as _file:
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
            print(event)

    particulars = []
    for i in data:
        try:
            particulars.append(i[8])
        except IndexError:
            particulars.append("None")

    reg = []
    for i in data:
        try:
            reg.append(i[9])
        except IndexError:
            reg.append("None")

    final_data = {
        "event": [i[0] for i in data],
        "begin": [i[1] for i in data],
        "max": [i[2] for i in data],
        "end": [i[3] for i in data],
        "obs": [i[4] for i in data],
        "Q": [i[5] for i in data],
        "type": [i[6] for i in data],
        "loc/freq": [i[7] for i in data],
        "particulars": particulars,
        "reg": reg
    }
    df = pd.DataFrame(final_data)
    print(df)


if __name__ == "__main__":
    main()
