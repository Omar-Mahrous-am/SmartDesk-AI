import os


class BaseController:

    def __init__(self):
        self.OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.files_dir = os.path.join("src", "assets")

