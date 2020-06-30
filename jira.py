from Tools import tools_v000 as tools
import os
from os.path import dirname


# -4 for the name of this project Jira
save_path = dirname(__file__)[ : -4]
propertiesFolder_path = save_path + "Properties"

# Example of used
user_text = tools.readProperty(propertiesFolder_path, 'Jira', 'user_text=')
