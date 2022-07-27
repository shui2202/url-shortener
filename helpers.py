import random
import string
import time
from datetime import date

BASE_URL = "https://day9-1.coder2237.repl.co/url"

def random_str(n=7):
  result = ""
  for i in range(n):
    result += random.choice(string.ascii_letters + string.digits)
  return result

def get_timestamp():
  today = date.today()
  _date = today.strftime("%m/%d/%y")
  ts = time.gmtime()
  timestamp = time.strftime("%x %X", ts)
  return _date, timestamp
