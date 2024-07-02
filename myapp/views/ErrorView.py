
import importlib
import textwrap
import traceback
from myapp.views.base import BaseView
from carta import Widget
from myapp.classes import reMarkable

class ErrorView(BaseView):
    def __init__(self, reMarkable: reMarkable,  additional_args: dict = {}) -> None:
        super().__init__(reMarkable, additional_args)
        self.hooks["error_back"] = self.error_back_hook
    
    def display(self):
        error = traceback.format_exc()
        wrapped = textwrap.wrap(error, width=1400//15)
        self.rm.add(
            Widget(
                id="error",
                typ="label",
                value="Error",
                justify="center",
                x="50%",
                y="10",
                
                fontsize="50",
            )
        )
        self.rm.add(
            Widget(
                id="error_message",
                typ="paragraph",
                value="\n".join(wrapped),
                justify="center",
                x="10",
                y="70",
                fontsize="30",
            )
        )
        self.rm.add(
            Widget(
                id="error_back",
                typ="button",
                value="Back",
                justify="left",
                x="0",
                y="100%",
            )
        )
    
    def error_back_hook(self, clicked: tuple):
        if clicked and clicked[0] == "error_back":
            self.rm.reset()
            self.current_view.clear()
            self.rm.update_view(importlib.import_module("myapp.views.HomeView").ExampleView(self.rm))
            self.current_view.clear()
            return None