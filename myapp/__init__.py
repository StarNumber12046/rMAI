import argparse
import importlib

from myapp.classes import reMarkable
from myapp.views.HomeView import ExampleView


def quit_hook(clicked):
    
    if clicked and clicked[0] == "exit":
            return "exit"



def main():
    parser = argparse.ArgumentParser(
        prog="myapp",
        description="Example carta application",
    )
    parser.add_argument(
        "--simple-executable",
        help="Path to the simple application",
        action="store",
        default=None,
        dest="simple",
    )
    args = parser.parse_args()

    rm = reMarkable(simple=args.simple) if args.simple is not None else reMarkable()

    rm.eclear()
    
    rm.update_view(ExampleView(rm))
    print("Updated base view")
    while True:
        try:
            clicked = rm.display()
            if quit_hook(clicked) == "exit":
                break
            rm.view.handle_buttons(clicked) # type: ignore
        except:
            rm.reset()
            rm.update_view(importlib.import_module("myapp.views.ErrorView").ErrorView(rm))
            rm.display()
            rm.view.display()