#!/bin/python3

import os
import pathlib
import sys
import shutil

config_file_name = "openmw.cfg"
config_file_path = os.path.join(pathlib.Path.home(), ".config", "openmw", config_file_name)

if (not os.path.exists(config_file_path)):
	print("Could not find", config_file_name, "at", config_file_path)
	exit(1)

def getarg(args: list, index: int, arg_type: type):
	if (index >= len(args)):
		print("Missing argument", index)
		exit(1)

	arg = args[index]

	if (type(arg) != arg_type):
		print("Argument", index, "must be a", str(arg_type))
		exit(1)

	return arg

def install_mod(args: list) -> None:
	mod_data_path = getarg(args, 0, str)

	if (not os.path.exists(mod_data_path)):
		print("Path \"%s\" does not exist" % mod_data_path)
		exit(1)

	mod_data_path = os.path.abspath(mod_data_path)

	with open(config_file_path, "r") as config_file:
		for line in config_file:
			if (mod_data_path in line):
				print(mod_data_path, "is already installed!")
				exit(1)

	with open(config_file_path, "a") as config_file:
		config_file.write("data=\"%s\"\n" % mod_data_path)

		for file_name in os.listdir(mod_data_path):
			if (file_name.endswith(".bsa")):
				config_file.write("fallback-archive=%s\n" % file_name)

	print(mod_data_path, "installed!")

def uninstall_mod(args: list) -> None:
	mod_data_path = os.path.abspath(getarg(args, 0, str))

	with open(config_file_path, "r") as config_file:
		lines = config_file.readlines()

	with open(config_file_path, "w") as config_file:
		line_index = 0

		while (line_index < len(lines)):
			if mod_data_path in lines[line_index]:
				line_index += 1

				while (
					(line_index < len(lines)) and
					lines[line_index].startswith("fallback-archive")
				):
					line_index += 1
			else:
				config_file.write(lines[line_index])

				line_index += 1

def list_mods(args: list) -> None:
	with open(config_file_path, "r") as config_file:
		mod_iterations = 0

		for line in config_file:
			if (line.startswith("data")):
				split_line = line.split("=")

				if (len(split_line) == 2):
					mod_data_path = split_line[1].strip("\t\n ")
					mod_name = os.path.split(mod_data_path)[1].strip("\"")

					print("[%d]: %s (%s)" % (mod_iterations, mod_name, mod_data_path))

					mod_iterations += 1

def backup_config(args: list) -> None:
	backup_path = getarg(args, 0, str)

	if (not os.path.exists(backup_path) and not os.path.exists(os.path.split(backup_path)[0])):
		print("Config file backup path is not valid")
		exit(1)

	shutil.copy2(config_file_path, backup_path)

actions = {
	"install": install_mod,
	"uninstall": uninstall_mod,
	"list": list_mods,
	"backup": backup_config
}

if (len(sys.argv) < 2):
	print("Expected an action")
	exit(1)

action_name = sys.argv[1]

if (not action_name in actions):
	print("Unknown action \"%s\". Supported actions:" % action_name, list(actions.keys()))
	exit(1)

actions[action_name](sys.argv[2:])
