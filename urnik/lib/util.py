import os
import tarfile
import datetime
import re
from pathlib import Path

from unidecode import unidecode
from fuzzywuzzy import fuzz
from icalevents.icalevents import events
import yaml


def is_geckodriver() -> bool:
    """
    Checks if geckodriver executable is in the $PATH.

    @rtype: bool
    """
    paths = [path + "/geckodriver" for path in os.environ["PATH"].split(":")]

    return any([os.path.isfile(file) for file in paths])


def set_geckodriver() -> None:
    """
    Adds geckodriver executable to ~/.local/bin folder.
    """

    tarfile_path = str(Path(__file__).parent.parent / "data/geckodriver-v0.28.0-linux64.tar.gz")
    tar = tarfile.open(tarfile_path, "r:gz")
    tar.extractall(str(Path.home() / ".local/bin"))
    tar.close()


def filter_schedule(all_events, config_file: str):
    event_descriptions = [event.description for event in all_events]

    # Load user settings
    with open(config_file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        user_groups = data['user']['groups']

    filtered_events = []

    # Every description of a course is made out of these items
    # [name, type, organizers, groups]
    for i, description in enumerate(event_descriptions):
        items = description.split(",")

        # TODO: explain that this just check if the subjects are similar
        # useful for grammer mistakes and such
        matches = [subject['group'] for subject in user_groups if
                   fuzz.partial_ratio(subject['name'].lower(), items[0].lower()) >= 90]

        if len(matches):
            # TODO: checks if the group is anywhere in the item and if so add
            if any([fuzz.partial_ratio(group, item) >= 80 for item in items for group in matches]):
                filtered_events.append(all_events[i])
        else:
            filtered_events.append(all_events[i])

    return filtered_events


# TODO: make start and end automatically using a function for beginning and end of week
def extract_schedule(file: str, start: datetime.datetime, end: datetime.datetime, use_filter=False):
    events_list = events(file=file, start=start, end=end)

    if use_filter:
        config_file = Path(__file__).parent.parent / "config.yaml"
        events_list = filter_schedule(events_list, config_file)

    return events_list


def get_organizer(event) -> []:
    # Using regex to get organizer names
    person_name = re.compile(r"[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*")

    description = [desc.strip() for desc in event.description.split(',')]
    # Unidecode turns all unicode characters to ASCII for regex pattern
    normalized_desc = [unidecode(desc) for desc in description]

    # 2:-1 because we know the index 2 starts with the organizer names
    # and the index -1 is the description ending with at least one group
    normalized_organizers = list(filter(person_name.fullmatch, normalized_desc[2:-1]))

    organizers = []
    for organizer in normalized_organizers:
        index = normalized_desc.index(organizer)
        organizers.append(description[index])

    return organizers


def get_groups(event) -> []:
    organizers = get_organizer(event)

    description = [desc.strip() for desc in event.description.split(',')]
    last_organizer_index = description.index(organizers[-1])

    return description[last_organizer_index + 1:]


def create_cell(data: str, lenght: int) -> str:
    string = "#"

    if data in ["#", " ", "&", "-", "=", "$"]:
        for i in range(0, lenght):
            string += data

        string = string[:-1]
    else:
        end = lenght - len(data) - 1
        for i in range(0, end):
            if i % 2 == 0:
                data = "{} ".format(data)
            else:
                data = " {}".format(data)

        string = "#%s" % data

    return string


def display_cell(event) -> []:
    time = event.start.strftime("%H:%M") + " - " + event.end.strftime("%H:%M")
    subject = event.summary + " ({})".format(event.description.split(',')[1].strip()) # saves "subject (type)"
    location = event.location
    organizers = ", ".join(get_organizer(event))
    groups = ", ".join(get_groups(event))

    table = ["#", " ", time, subject, location, organizers, groups, " ", "#"]
    largest_len = max([len(string) for string in table]) + 10

    for i in range(len(table)):
        table[i] = create_cell(table[i], largest_len)

    return table


def display_schedule(schedule) -> str:
    days = sorted(set([event.start.date() for event in schedule]))
    schedule_by_day = [[event for event in schedule if event.start.date() == day] for day in days]

    display_by_day = []

    for events_by_day in schedule_by_day:

        day = ["PON", "TOR", "SRE", "ČET", "PET"][events_by_day[0].start.weekday()]
        date = events_by_day[0].start.strftime("%d.%m.%Y")

        table = [""] * 9  # The height of the table
        for event in events_by_day:
            cell = display_cell(event)
            for i in range(len(table)):
                table[i] += cell[i]

        # Close table
        for i in range(len(table)):
            table[i] += "#"

        # Adds date and day name to the top of table
        table.insert(0, "{}: {}".format(date, day))

        display_by_day.append("\n".join(table))

    return "\n\n".join(display_by_day)
