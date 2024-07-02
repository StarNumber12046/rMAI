
from myapp.views.base import BaseView
from carta import Widget
from myapp.classes import reMarkable

class NoInternetView(BaseView):
    def __init__(self, reMarkable: reMarkable,  additional_args: dict = {}) -> None:
        super().__init__(reMarkable, additional_args)
    

    def display(self):
        self.rm.add(
            Widget(
                id="no_internet",
                typ="label",
                value="No Internet",
                justify="center",
                x="50%",
                y="10",
                
                fontsize="50",
            )
        )
        self.rm.add(
            Widget(
                id="no_internet_message",
                typ="label",
                value="Please check your internet connection",
                justify="center",
                x="50%",
                y="70",
                fontsize="30",
            )
        )
