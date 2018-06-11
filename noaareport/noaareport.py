"""
MIT License

Copyright (c) 2018 Edison Neto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

import pandas as pd


class NoaaReport:
    """Reads noaa report.

    Reads the last active region on the file from the previous day,
    and compares to the first one.
        
    Arguments:
        year {str or int} -- [description]
        month {str or int} -- [description]
        day {str or int} -- [description]
    """

    def __init__(self, year, month, day):
        self._year = str(year)
        self._month = str(month)
        self._day = str(day)
        self._filename = self.__set_filename()
        self._data = []
        self.df = None

    def __set_filename(self):
        """[summary]
        
        Returns:
            str -- The name of the file.
        """

        if len(self._month) == 1:
            self._month = "0" + self._month
        if len(self._day) == 1:
            self._day = "0" + self._day
        filename = self._year + self._month + self._day + "events.txt"
        filename = "reports/2017_events/" + filename
        return filename

    def __check_data(self):
        """Checks if the data has already been saved.

        Returns:
            boolean -- [description]
        """

        if len(self._data):
            return True

        self._read_data()

    def _read_data(self):
        """Reads the file.
        """
        with open(self._filename) as _file:
            for line in _file.readlines():
                sep = line.split()

                try:
                    if (not sep[0].startswith(":") and
                            not sep[0].startswith("#")):
                        self._data.append(sep)
                except IndexError:
                    pass

            for event in self._data:
                if event[1] == "+":
                    event[0] += " +"
                    del event[1]

    def set_Qs(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        Qs = []
        for info in self._data:
            if len(info[5]) == 1:
                Qs.append(info[5])
            else:
                Qs.append("None")
        return Qs

    def set_observatories(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        index = 0
        observatories = []
        while index < len(self._data):
            if len(self._data[index][4]) == 3:
                observatories.append(self._data[index][4])
                index += 1
            else:
                del self._data[index]

        return observatories

    def set_particulars(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        particulars = []
        index = 0
        regs = self.set_regions()
        while index < len(self._data):
            try:
                last_index = len(self._data[index]) - 1
                last_reg = ""
                for reg in regs:
                    if reg != "None":
                        last_reg = reg
                        break

                if (self._data[index][last_index].isdigit()
                        and len(self._data[index][last_index]) == 4):
                    if len(self._data[index]) > 10:
                        particular = (self._data[index][last_index - 2] + " " +
                                     self._data[index][last_index - 1])
                    elif (self._data[index][last_index] != last_reg
                            and int(self._data[index][last_index])-1 != last_reg):
                        particular = self._data[index][last_index]
                    else:
                        particular = self._data[index][last_index - 1]
                else:
                    if len(self._data[index]) > 9:
                        particular = (self._data[index][last_index - 1] + " " +
                                     self._data[index][last_index])
                    else:
                        particular = self._data[index][last_index]

                particulars.append(particular)
            except IndexError:
                particulars.append("None")

            index += 1

        return particulars

    def set_regions(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        reg = []
        rreg = []
        for info in self._data:
            try:
                last_index = len(info) - 1
                if info[last_index].isdigit() and len(info[last_index]) == 4:
                    if len(rreg) == 0:
                        reg.append(info[last_index])
                        rreg.append(info[last_index])
                    elif info[last_index] == rreg[-1]:
                        reg.append(info[last_index])
                        rreg.append(info[last_index])
                    else:
                        reg.append("None")
                else:
                    reg.append("None")
            except IndexError:
                reg.append("None")
        
        return reg

    def set_event(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[0] for i in self._data]

    def set_begin(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[1] for i in self._data]

    def set_max(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[2] for i in self._data]

    def set_end(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[3] for i in self._data]

    def set_type(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[6] for i in self._data]

    def set_freq(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        self.__check_data()
        return [i[7] for i in self._data]

    def set_final_data(self):
        """[summary]
        """

        self.__check_data()

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

        self.df = pd.DataFrame(final_data, columns=columns)
        print(self.df)

    def get_active_region(self, start_time, end_time):
        """Returns registered active region of a certain time range.
        
        Arguments:
            start_time {str} -- event's start time.
            end_time {str} -- event's end time.

        Returns:
            list<str> -- [description]
        """

        start_time = str(start_time)
        end_time= str(end_time)
        start_time = start_time[11:16].replace(":", "")
        end_time = end_time[11:16].replace(":", "")
        ar = []

        for i in range(0, len(self.df)):
            if self.df["end"][i] < "10":
                continue

            if (self.df["begin"][i] >= start_time
                    and self.df["end"][i] <= end_time):
                print(self.df["begin"][i])
                ar.append(self.df["reg"][i])

        return ar