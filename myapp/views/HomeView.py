import textwrap
from myapp.classes import reMarkable
from myapp.views.base import BaseView
from carta import Widget
import replicate
import requests
from myapp.views.NoInternet import NoInternetView

class ExampleView(BaseView):
    def __init__(self, reMarkable: reMarkable, additional_args: dict = {}) -> None:
        super().__init__(reMarkable, additional_args)
        self.hooks["*"] = self.send_instruction
        self.ignore_input = False
        self.messages = []
 


    def delete_first_messages(self, last_message_height):
        if last_message_height + 30 > 1600:
            self.messages.pop(0)
            messages_height = 75
            for message in self.messages:
                messages_height += 20
                for line in textwrap.wrap(f"{message['role']}: {message['content']}", width=1400//15):
                    messages_height += 30
            self.delete_first_messages(messages_height)

    def display(self):       
        try:
            requests.get("https://replicate.com/")
        except:
            v = NoInternetView(self.rm)
            self.rm.update_view(v)
            return
        print("Messages:" + str(self.messages))
        self.rm.add(
            Widget(
                "title", "label", "Chat with llama2", x="50%", y="10", fontsize="50px"
            )
        )

        messages_height = 75
        for message in self.messages:
            messages_height += 20
            for line in textwrap.wrap(f"{message['role']}: {message['content']}", width=1400//15):
                messages_height += 30
        self.delete_first_messages(messages_height)
        
        last_height = 75
        for index, message in enumerate(self.messages):
            last_height += 20 # Separate messages
            lines = textwrap.wrap(f"{message['role']}: {message['content']}", width=1400//15)
            for line_index, line in enumerate(lines):
                self.rm.add(
                    Widget(
                        "message_" + str(index) + "_" + str(line_index),
                        "label",
                        line,
                        x="20",
                        y=f"{last_height+30}",
                        justify="left",
                    )
                )
                last_height += 30
        self.rm.add(
            Widget(
                "input",
                "textarea",
                "Hello",
                x="10%",
                y="99%",
                fontsize="25px",
                width="90%",
            )
        )

    def send_instruction(self, clicked):
        output = ""
        self.messages.append({"role": "user", "content": clicked[1]})
        prompt = (
            "\n".join(
                [f"[INST] {message['content']} [/INST]" if message["role"] == "user" else message["content"] for message in self.messages  ]
            )
            + f"\n{self.messages[-1]['role']}: {self.messages[-1]['content']}"
        )
        for event in replicate.stream("meta/llama-2-7b-chat", input={"prompt": prompt}):
            output += str(event)
        self.messages.append({"role": "assistant", "content": output})
        self.rm.reset()
        self.display()
