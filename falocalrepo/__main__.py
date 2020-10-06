from sys import argv
from sys import exit
from traceback import print_exc
from typing import List

from .console import MalformedCommand
from .console import UnknownCommand
from .console import console


def main(args: List[str] = None):
    # Run main program
    args = argv[1:] if args is None else args
    try:
        console(*args)
    except KeyboardInterrupt:
        print()
        pass
    except (MalformedCommand, UnknownCommand) as err:
        print(repr(err))
        exit(1)
    except ConnectionError as err:
        print(repr(err))
        exit(2)
    except (Exception, BaseException) as err:
        with open("FA.log", "w") as f:
            print_exc(file=f)
            print(repr(err))
            print(f"Trace written to {f.name}")
        exit(3)


if __name__ == "__main__":
    main(argv)
