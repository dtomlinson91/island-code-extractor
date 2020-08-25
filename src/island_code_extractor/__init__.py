"""Island code extractor for Animal Crossing."""
import os

import panaetius
from panaetius.config import Config

CONFIG = Config(path="~/.config/island-code-extractor", header="island-code-extractor")

panaetius.set_config(CONFIG, "reddit.secret")
panaetius.set_config(CONFIG, "reddit.id")
panaetius.set_config(CONFIG, "reddit.user_agent")
panaetius.set_config(CONFIG, "reddit.thread_id")
panaetius.set_config(CONFIG, "reddit.output_path")
