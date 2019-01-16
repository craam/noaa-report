import sys
import os

import pandas as pd

from .noaareport import NoaaReport

def usage(status):
    print("Usage: report [PATH] [YEAR] [MONTH] [DAY]")
    print("Optional: report [PATH] [YEAR] [MONTH] [DAY] [EVENT_BEGIN] [EVENT_END]")
    print("\t-h\t this help message.")
    print("\nExample:")
    print("report ~/reports/2002_events/ 2002 4 9 12:40:00 13:00:00")
    print("\nWritten by Edison Neto (2019)")
    sys.exit(status)

if len(sys.argv) == 1:
    usage(-1)

if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    usage(0)

if len(sys.argv) < 5:
    print("You need more arguments.")
    sys.exit(-1)

path = sys.argv[1]
year = sys.argv[2]
month = sys.argv[3]
day = sys.argv[4]

report = NoaaReport(year, month, day, path)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(report.get_dataframe())

if len(sys.argv) > 6:
    common_str = "0000-00-00 "
    begin = common_str + sys.argv[5]
    end = common_str + sys.argv[6]
    ars = report.get_active_region(begin, end)
    print(ars)
