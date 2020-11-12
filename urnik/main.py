import argparse
from pathlib import Path
import datetime

from urnik.lib import util
from urnik.lib.browser import browser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to get my schedule for school (urnik pač)")
    parser.add_argument("-d", "--download", action='store_true', help="Download a new schedule for current week (if "
                                                                      "saturday, next weeks)")
    args = parser.parse_args()

    if not util.is_geckodriver():
        util.set_geckodriver()

    ical_file = Path(__file__).parent / "data/calendar.ics"
    if args.download:
        download_folder = str(ical_file.parent)
        browser = browser.Browser(download_folder)
        browser.download_schedule("https://www.wise-tt.com/wtt_um_feri/index.jsp?filterId=0;79;0;0;")

    else:
        start = datetime.datetime(2020, 11, 9)
        end = datetime.datetime(2020, 11, 15)

        schedule = util.extract_schedule(ical_file, start, end, use_filter=True)
        displayed_scheduler = util.display_schedule(schedule)

        print(displayed_scheduler)
