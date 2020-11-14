import argparse
import os
import sys
import glob
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

from urnik.lib import util
from urnik.lib.browser import browser
import yaml


def main():
    parser = argparse.ArgumentParser("urnik", formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                        Program to get my schedule for school (urnik pac)
                                     
                                        With no arguments the program returns the schedule for the
                                        current day. Use --week if you want to see the entire week.
                                        
                                     --------------------------------
                                     '''))
    parser.add_argument("-w", "--week", action="store_true", help="")
    parser.add_argument("-s", "--start", type=str, metavar="date", help="Starting date of schedule. Date string "
                                                                        "format 'd.m.y' or 'd.m'. If --end not "
                                                                        "specified auto uses end of week")
    parser.add_argument("-e", "--end", type=str, metavar="date", help="Ending date of schedule. Date string format "
                                                                      "'d.m.y' or 'd.m'. If --start not specified "
                                                                      "auto uses begging of week")
    parser.add_argument("-f", "--no-filter", action='store_true', help="Disable filtering from user configuration. "
                                                                        "This just reads the entire schedule and "
                                                                        "displays it")
    parser.add_argument("-d", "--download", action='store_true', help="Download a schedule for the current week")
    parser.add_argument("-c", "--configure", action='store_true', help="Open configuration file of the program with "
                                                                       "$EDITOR")
    args = parser.parse_args()

    valid_date_formats = ["%d.%m", "%d.%m.%y"]
    ical_file = Path(__file__).parent.resolve() / "data/calendar.ics"
    config_file = Path(__file__).parent.resolve() / "config.yaml"

    if not util.is_geckodriver():
        util.set_geckodriver()
    if args.configure:
        editor = os.getenv('EDITOR')

        if not os.path.isfile(config_file):
            print("Couldn't find configuration file at location: " + str(config_file))
            sys.exit()

        os.system(editor + ' ' + str(config_file))

    elif args.download:
        download_folder = str(ical_file.parent)
        client = browser.Browser(download_folder, hide_browser=True)

        with open(config_file, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            link = data['user'].get('url', "https://www.wise-tt.com/wtt_um_feri/")

        client.download_schedule(link)

        print("Downloaded file to: " + str(download_folder))

    else:
        # For displaying the current day
        start = datetime.now().replace(hour=0)
        end = start.replace(hour=23)

        # Displaying the entire week
        if args.week or args.end is not None or args.start is not None:
            # Saves the start (monday) and end (sunday) date of current week
            start = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end = start + timedelta(days=6)

        # Displaying a set interval date
        if args.start is not None:
            start = util.parse_date(args.start, valid_date_formats)
            start = start.replace(hour=0)
        if args.end is not None:
            end = util.parse_date(args.end, valid_date_formats)
            end = end.replace(hour=23)

        # If the file doesn't exist try to get first ics file in the files directory
        if not os.path.isfile(ical_file):
            ical_files = glob.glob(str(ical_file.parent) + "/*.ics")
            if len(ical_files) == 0:
                print("Program ni našel .ics datoteke. Uporabi argument '--download', da se prenese novi urnik.")
                sys.exit()

            ical_file = Path(ical_files[0])

        schedule = util.extract_schedule(ical_file, start, end, use_filter=(not args.no_filter))
        displayed_scheduler = util.display_schedule(schedule)

        if len(displayed_scheduler):
            print(displayed_scheduler)
        else:
            print("Danes nimaš pouka.")
