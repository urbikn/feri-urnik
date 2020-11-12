import argparse
from pathlib import Path
from datetime import datetime, timedelta

from urnik.lib import util
from urnik.lib.browser import browser

valid_date_formats = ["%d.%m", "%d.%m.%y"]

if __name__ == '__main__':
    parser = argparse.ArgumentParser("urnik", description="Program to get my schedule for school (urnik pač)")
    parser.add_argument("-d", "--download", action='store_true', help="Download a schedule for current week")
    parser.add_argument("-nf", "--no-filter", action='store_true', help="Disable filtering from user configuration. "
                                                                        "This just reads the entire schedule and "
                                                                        "displays it")
    parser.add_argument("-s", "--start", type=str, metavar="date", help="Starting date of schedule. Date string "
                                                                        "format 'd.m.y' or 'd.m'")
    parser.add_argument("-e", "--end", type=str, metavar="date", help="Ending date of schedule. Date string format "
                                                                      "'d.m.y' or 'd.m'")
    args = parser.parse_args()

    if not util.is_geckodriver():
        util.set_geckodriver()

    ical_file = Path(__file__).parent / "data/calendar.ics"
    print(args)
    if args.download:
        download_folder = str(ical_file.parent)
        browser = browser.Browser(download_folder, hide_browser=True)
        browser.download_schedule("https://www.wise-tt.com/wtt_um_feri/index.jsp?filterId=0;79;0;0;")

    else:
        # Saves the start (monday) and end (sunday) date of current week
        start = datetime.now().date() - timedelta(days=datetime.now().weekday())
        end = start + timedelta(days=6)

        if args.start is not None:
            start = util.parse_date(args.start, valid_date_formats)
        if args.end is not None:
            end = util.parse_date(args.end, valid_date_formats)

        schedule = util.extract_schedule(ical_file, start, end, use_filter=(not args.no_filter))
        displayed_scheduler = util.display_schedule(schedule)

        print(displayed_scheduler)
