import os

def get_email():
    return os.environ["EMAIL"]

def get_password():
    return os.environ["PASSWORD"]

def get_iit_delhi_url():
    return os.environ["IIT_DELHI"]
