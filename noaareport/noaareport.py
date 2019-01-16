from __future__ import print_function

import os
import datetime as dt

import pandas as pd


class NoEventReports(Exception):
    """No events reported in this day. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoaaReport(object):
    """Reads noaa report.

    Reads the last active region on the file from the previous day,
    and compares to the first one.

    Attributes
    ----------
    year: str or int
        The report's year.
    month: stro or int
        The report's month.
    day: str ot int
        The report's day.
    path: str
        The path to the report file.
    filename: str
        Filename set for the selected day

    """

    def __init__(self, year, month, day, path):
        self._year = str(year)
        self._month = str(month)
        self._day = str(day)
        self._path = path
        self._filename = self.__set_filename()
        self._data = []
        self.df = None

    def __set_filename(self):
        """Creates the filename, given the year, month and day.

        Returns
        -------
        str
            The filename.

        """

        if len(self._month) == 1:
            self._month = "0" + self._month

        if len(self._day) == 1:
            self._day = "0" + self._day

        filename = self._year + self._month + self._day + "events.txt"
        return filename

    def __check_data(self):
        """Checks if the data has already been saved.

        Returns
        -------
        bool
            True if data has alredy been read.

        Raises
        ------
        NoEventReports
            There are no events in this day.

        """

        if len(self._data):
            return True

        self.read()
        return False

    def read(self):
        """Reads the file.

        Returns
        -------
        _data: list
            The data in a list.

        Raises
        ------
        NoEventReports
            There are no events in this day.

        """
        with open(os.path.join(self._path, self._filename)) as _file:
            for line in _file.readlines():
                if len(line.strip()) == 0:
                    continue

                if line.startswith(":") or line.startswith("#"):
                    continue
                elif line.startswith("NO"):
                    raise NoEventReports("No events reported")
                
                
                event = line[:8].strip()
                event_begin = line[8:16].strip()
                event_max = line[16:25].strip()
                event_end = line[25:32].strip()
                obs = line[32:37].strip()
                quality = line[37:40].strip()
                event_type = line[40:46].strip()
                loc = line[46:55].strip()
                particulars = line[55:73].strip()
                region = line[73:].strip()
                
                self._data.append([
                    event, event_begin, event_max, event_end, obs, quality,
                    event_type, loc, particulars, region
                ])

        return self._data

    def get_event(self):
        """Sets the event column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[0] for i in self._data]

    def get_begin(self):
        """Sets the begin column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[1] for i in self._data]

    def get_max(self):
        """Sets the max column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[2] for i in self._data]

    def get_end(self):
        """Sets the end column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[3] for i in self._data]

    def get_obs(self):
        """Sets the obs column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[4] for i in self._data]

    def get_Q(self):
        """Sets the Q column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[5] for i in self._data]

    def get_type(self):
        """Sets the type column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[6] for i in self._data]

    def get_freq(self):
        """Sets the loc/freq column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[7] for i in self._data]

    def get_particulars(self):
        """Sets the particulars column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[8] for i in self._data]

    def get_reg(self):
        """Sets the reg column.

        Returns
        -------
        list
            Contains the value for each line for the column.

        """

        self.__check_data()
        return [i[9] for i in self._data]

    def is_active_region(self, ar):
        try:
            ar = int(ar)
        except ValueError:
            return False

        ar = str(ar)
        if len(ar) != 4:
            return False

        return True

    def get_dataframe(self):
        """Stores all the data in a dataframe.

        Returns
        -------
        pandas.DatFrame
            A DataFrame with the data.

        """

        data = {
            "event": self.get_event(),
            "begin": self.get_begin(),
            "max": self.get_max(),
            "end": self.get_end(),
            "obs": self.get_obs(),
            "Q": self.get_Q(),
            "type": self.get_type(),
            "loc/freq": self.get_freq(),
            "particulars": self.get_particulars(),
            "reg": self.get_reg()
        }

        columns=["event", "begin", "max", "end", "obs", "Q", "type",
                "loc/freq", "particulars", "reg"]
        self.df = pd.DataFrame(data, columns=columns)

        return self.df

    def get_active_region(self, start_time, end_time):
        """Returns registered active region of a certain time range.

        Parameters
        ----------
        start_time: str
            Event's start time.
        end_time: str
            Event's end time.

        Returns
        -------
        list
            All the not None active regions.

        """

        start_time = str(start_time)
        end_time = str(end_time)
        start_time = start_time[11:16].replace(":", "")
        start_time = dt.timedelta(hours=int(start_time[0:2]),
                                  minutes=int(start_time[2:]))
        end_time = end_time[11:16].replace(":", "")
        end_time = dt.timedelta(hours=int(end_time[0:2]),
                                minutes=int(end_time[2:]))
        ar = []

        for i in range(0, len(self.df)):

            if not self.df["begin"][i][0].isnumeric():
                self.df["begin"][i] = self.df["begin"][i][1:]
            if not self.df["max"][i][0].isnumeric():
                self.df["max"][i] = self.df["max"][i][1:]
            if not self.df["end"][i][0].isnumeric():
                self.df["end"][i] = self.df["end"][i][1:]

            event_begin = dt.timedelta(hours=int(self.df["begin"][i][0:2]),
                                       minutes=int(self.df["begin"][i][2:]))

            event_end = dt.timedelta(hours=int(self.df["end"][i][0:2]),
                                     minutes=int(self.df["end"][i][2:]))

            eleven_oclock = dt.timedelta(hours=23, minutes=00)
            fifteen_minutes = dt.timedelta(minutes=15)
            if event_begin >= eleven_oclock:
                continue

            if (event_begin >= start_time and
                    event_end <= end_time + fifteen_minutes):
                print("\nBegin: {}".format(self.df["begin"][i]))
                print("Max: {}".format(self.df["max"][i]))
                print("End: {}".format(self.df["end"][i]))
                print("Type: {}".format(self.df["type"][i]))
                print("Loc/Freq: {}".format(self.df["loc/freq"][i]))
                print("Region: {}".format(self.df["reg"][i]))

                ar.append(self.df["reg"][i])

        ar = [x for x in ar if x is not None]
        if len(ar) == 0:
            print("No regions identified.")

        return ar

    def stuff(self):
        saves = []
        for i in range(0, len(self.df)):
            if (self.df["type"][i] == "XRA" and (
                self.df["particulars"][i].startswith("M")
                    or self.df["particulars"][i].startswith("X"))):
                if (int(self.df["begin"][i]) < 800
                        or int(self.df["begin"][i]) > 1800):
                    continue
                saves.append(i)

        for sav in saves:
            if sav+5 > len(self.df["type"]):
                df_max = (len(self.df["type"])-1)
                for i in range(sav-5, df_max):
                    if self.df["type"][i] == "RBR":
                        print("\nBegin: {}".format(self.df["begin"][i]))
                        print("Freq: {}".format(self.df["loc/freq"][i]))
                        print("Particulars: {}".format(
                            self.df["particulars"][i]))
                        print("Index: {}".format(i))

            if sav > 5:
                for i in range(sav-5, sav+5):
                    if self.df["type"][i] == "RBR":
                        print("\nBegin: {}".format(self.df["begin"][i]))
                        print("Freq: {}".format(self.df["loc/freq"][i]))
                        print("Particulars: {}".format(
                            self.df["particulars"][i]))
                        print("Index: {}".format(i))
            else:
                for i in range(0, sav+5):
                    if self.df["type"][i] == "RBR":
                        print("\nBegin: {}".format(self.df["begin"][i]))
                        print("Freq: {}".format(self.df["loc/freq"][i]))
                        print("Particulars: {}".format(
                            self.df["particulars"][i]))
                        print("Index: {}".format(i))
