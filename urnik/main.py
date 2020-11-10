from urnik.lib import util

if __name__ == '__main__':

    if not util.is_geckodriver():
        util.set_geckodriver()
