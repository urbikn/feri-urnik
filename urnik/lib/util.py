import os
import tarfile
import datetime
import re
import itertools
from pathlib import Path

from unidecode import unidecode
from fuzzywuzzy import fuzz
from icalevents.icalparser import Event
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


def filter_schedule(all_events: [Event], config_path: str) -> [Event]:
    """
    Given a list of events the function filters out the subjects with the groups not matching the
    accepted groups specified by the user saved in the configuration file.

    Subjects not specified in the configuration file are not filtered out.

    @param all_events: List of events
    @param config_path: Path to the configuration file
    @return: List of filtered events
    """
    # Load user settings
    with open(config_path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        user_groups = data['user'].get('groups', None)

    if user_groups is None:
        return all_events

    lecture_events = [event for event in all_events if 'PR' in event.description.split(',')[1]]
    general_groups = [get_groups(event) for event in lecture_events]
    general_groups = set(itertools.chain.from_iterable(general_groups))  # Flatten 2D to 1D list and get unique groups

    filtered_events = []
    for event in all_events:

        # Every description of a course is made out of these items
        # [name, type, organizers, groups]
        subject = [desc.strip() for desc in event.description.split(',')][0]
        groups = get_groups(event)

        # Finds all user specified groups of subject, if any specified
        # The partial_ratio is used so if the user makes a grammar mistake or just
        # specified part of the group
        matches = [user_subject['group'] for user_subject in user_groups if
                   fuzz.partial_ratio(user_subject['name'].lower(),
                                      subject.lower()) >= 90]  # Useful for grammar mistakes
        matches = list(itertools.chain.from_iterable(matches)) # 2D to 1D list. Just in case.

        # This could probably be done better, I just don't know yet, so here's the explanation:
        # The idea behind the matches is to first filter out general groups from the events groups.
        # The reason for this is that if this wasn't implemented, some events like SV (seminarske vaje)
        # can have no specific group, but still can get caught by the matches.
        if len(matches):
            # removes general groups event groups - easier to look if it has any group
            for i in range(len(groups)):
                for group in general_groups:
                    groups[i] = groups[i].replace(group, '').strip()

            if len("".join(groups)):
                scores = [fuzz.partial_ratio(group, user_group) for group in groups for user_group in matches]
                if any([fuzz.partial_ratio(group, user_group) >= 90 for group in groups for user_group in matches]):
                    filtered_events.append(event)
            else:
                filtered_events.append(event)
        else:
            filtered_events.append(event)

    return filtered_events


def extract_schedule(file: str, start: datetime.datetime, end: datetime.datetime, use_filter=False) -> [Event]:
    """
    Extract events from .ics file and return the events in a list

    Function extracts events by a datetime interval specified with the start and end parameters.

    By setting the use_filter parameter, the function filters the events by looking at the assigned groups saved in
    the programs configuration file. The filter will only affect the events in which there is a group.

    @param file: Path to .ics file
    @param start: start date
    @param end: end date
    @param use_filter: Use group filtering specified in configuration file
    @return: List of extracted events of type icalevents.icalparser.Event
    """
    events_list = events(file=file, start=start, end=end)

    if use_filter:
        config_file = Path(__file__).parent.parent / "config.yaml"
        events_list = filter_schedule(events_list, config_file)

    return events_list


def get_organizer(event: Event) -> [str]:
    """
    Return organizers of the event stored in the events description.

    The function does this by using regex to match valid Person names in the description string and store
    the matches into a list.

    @param event: Event instance of icalevents.icalparser.Event
    @return: List of event organizers
    """
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


def get_groups(event: Event) -> [str]:
    """
    Return groups of the event stored in the events description.

    @param event: Event instance of icalevents.icalparser.Event
    @return: List of event groups
    """
    organizers = get_organizer(event)

    description = [desc.strip() for desc in event.description.split(',')]
    last_organizer_index = description.index(organizers[-1])

    return description[last_organizer_index + 1:]


def create_cell_line(data: str, length: int) -> str:
    """
    Function creates a string centered with content and padded on each side with ' ' (spaces), starting and

    To specify the start and end of the cell the string has a prefix/suffix filled with character '#'.

    @param data: Content of the line
    @param length: Width of the cell
    @return: String with transformed content
    """
    string = "#"

    if data in ["#", " ", "&", "-", "=", "$"]:
        for i in range(0, length):
            string += data

        string = string[:-1]
    else:
        end = length - len(data) - 1
        for i in range(0, end):
            if i % 2 == 0:
                data = "{} ".format(data)
            else:
                data = " {}".format(data)

        string = "#%s" % data

    return string


def create_cell(event: Event) -> [str]:
    """
    Turn an event into a table cell by extracting the events duration, subject, location, organizers and
    subject groups (if any).

    The function before constructing the cell calculates the longest string/line which determines the width
    of the entire cell.

    A picture of the functions returned cell.

        #####################
        #                   #
        #    start - end    #
        #   subject (type)  #
        #     location      #
        #    organizers     #
        #      groups       #
        #                   #
        #####################

    @param event: Event instance of icalevents.icalparser.Event
    @return: List containing every line of the table cell
    """
    duration = event.start.strftime("%H:%M") + " - " + event.end.strftime("%H:%M")
    subject = event.summary + " ({})".format(event.description.split(',')[1].strip())  # saves "subject (type)"
    location = event.location
    organizers = ", ".join(get_organizer(event))
    groups = ", ".join(get_groups(event))

    table = ["#", " ", duration, subject, location, organizers, groups, " ", "#"]
    largest_len = max([len(string) for string in table]) + 10

    for i in range(len(table)):
        table[i] = create_cell_line(table[i], largest_len)

    return table


def display_schedule(schedule: [Event]) -> str:
    """
    Create a table from all the events in list.

    The table generated from the events looks like the picture below, where events for each day are stored
    in their own table. The cells for each event are concatenated to the end of the table, sorted by their
    start time.

        date: day
        #####################
        #                   #
        #    start - end    #
        #   subject (type)  #
        #     location      #
        #    organizers     #
        #      groups       #
        #                   #
        #####################

    The function returns a singe string containing all the tables separated by '\n'.

    @param schedule: List of events
    @return: Schedule in a string
    """
    days = sorted(set([event.start.date() for event in schedule]))
    schedule_by_day = [[event for event in schedule if event.start.date() == day] for day in days]

    display_by_day = []

    for events_by_day in schedule_by_day:

        day = ["PON", "TOR", "SRE", "ČET", "PET"][events_by_day[0].start.weekday()]
        date = events_by_day[0].start.strftime("%d.%m.%Y")

        table = [""] * 9  # The height of the table
        for event in events_by_day:
            cell = create_cell(event)
            for i in range(len(table)):
                table[i] += cell[i]

        # Close table
        for i in range(len(table)):
            table[i] += "#"

        # Adds date and day name to the top of table
        table.insert(0, "{}: {}".format(date, day))

        display_by_day.append("\n".join(table))

    return "\n\n".join(display_by_day)
