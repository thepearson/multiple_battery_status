#!/usr/bin/env python
import os

# proc path
ACPI_PROC_PATH="/proc/acpi/battery"
ACPI_BAT_PREFIX="BAT"

bats = []

current = 0
total = 0


def get_batteries(path, prefix=ACPI_BAT_PREFIX):
  """
  Returns a list of batteries under /proc/acpi/battery
    Currently uses the folder names
  """
  ret = []
  for x in os.walk(path):
    if os.path.split(x[0])[1].startswith(prefix):
      ret.append(os.path.split(x[0])[1])
  return ret


def get_proc_file_list(fname):
  """
  Returns the proc file as a list, only includes lines that have ":"
  """
  ret = {}
  i = open(fname, 'r')
  for line in i.read().split("\n"):
    if line.count(":") > 0:
      key, value = line.split(":")
      ret[key.strip()] = value.strip()
  return ret


def load_battery_info(bat):
  """
  Given a battery "name" (folder name) will return an info list
  """
  return get_proc_file_list('/proc/acpi/battery/' + bat + '/info')


def load_battery_state(bat):
  """
  Given a battery "name" (folder name) will return a state list
  """
  return get_proc_file_list('/proc/acpi/battery/' + bat + '/state')


def get_last_full_capacity(bat):
  """
  Returns an int of the last mWh capacity
  """
  info = load_battery_info(bat)
  return int(info['last full capacity'].split()[0])


def get_current_usage(bat):
  """
  Returns an int of the current mWh usage of bat
  """
  state = load_battery_state(bat)
  return int(state['remaining capacity'].split()[0])


bats = get_batteries(ACPI_PROC_PATH)
for bat in bats:
  current += get_current_usage(bat)
  total += get_last_full_capacity(bat)

percent = (100./total)*current
print "Battery capacity: %.2f%%" % percent


