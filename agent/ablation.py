from agent.config import AblationConfig

current = AblationConfig()


def set_config(config):
    global current
    current = config


def reset():
    global current
    current = AblationConfig()
