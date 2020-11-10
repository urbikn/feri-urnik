import os
from pathlib import Path
import tarfile


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
