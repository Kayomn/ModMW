import argparse
import os
import pathlib
import shutil
from platform import system


def install_mod(path, config_path) -> None:
	mod_data_path = path

	if (not os.path.exists(mod_data_path)):
		print("Path \"%s\" does not exist" % mod_data_path)
		exit(1)

	mod_data_path = os.path.abspath(mod_data_path)

	with open(config_file_path, "r") as config_file:
		for line in config_file:
			if (mod_data_path in line):
				print(mod_data_path, "is already installed!")
				exit(1)

	with open(config_path, "a") as config_file:
		config_file.write("data=\"%s\"\n" % mod_data_path)

		for file_name in os.listdir(mod_data_path):
			if (file_name.endswith(".bsa")):
				config_file.write("fallback-archive=%s\n" % file_name)

	print(mod_data_path, "installed!")


def uninstall_mod(path, config_path) -> None:
	mod_data_path = path

	with open(config_path, "r") as config_file:
		lines = config_file.readlines()

	with open(config_path, "w") as config_file:
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


def list_mods(config_path) -> None:
	with open(config_path, "r") as config_file:
		mod_iterations = 0

		for line in config_file:
			if (line.startswith("data")):
				split_line = line.split("=")

				if (len(split_line) == 2):
					mod_data_path = split_line[1].strip("\t\n ")
					mod_name = os.path.split(mod_data_path)[1].strip("\"")

					print("[%d]: %s (%s)" % (mod_iterations, mod_name, mod_data_path))

					mod_iterations += 1


def backup_config(path, config_path) -> None:
	backup_path = path

	if (not os.path.exists(backup_path) and not os.path.exists(os.path.split(backup_path)[0])):
		print("Config file backup path is not valid")
		exit(1)

	shutil.copy2(config_path, backup_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument("--install", type=str, default=None, action="store", required=False,
						help="Provide this parameter with the path of a single  mod folder that should be added to the "
							 "config file")
	parser.add_argument("--uninstall", type=str, default=None, action="store", required=False,
						help="Provide this parameter with path of a single mod folder that should be removed from the "
							 "config file")
	parser.add_argument("--list", default=None, action="store_true", required=False,
						help="Commands the script to list the current mod folders from the config file.")
	parser.add_argument("--backup", type=str, default=None, action="store", required=False,
						help="Provide this parameter with the path where the backup file should be placed.")
	parser.add_argument("--configfile", type=str, default=None, action="store", required=False,
						help="In case the config file is not in the default location, provide this parameter with the "
							 "path including(!) the openmw.cfg file.")

	p = parser.parse_args()

	if (p.configfile):
		config_file_path = p.configfile

	else:

		config_file_name = "openmw.cfg"
		plt = system()

		if (plt == "Windows"):
			config_file_path = os.path.join(pathlib.Path.home(), "Documents", "my games", "openmw", config_file_name)
		else:
			config_file_path = os.path.join(pathlib.Path.home(), ".config", "openmw", config_file_name)

	if not (os.path.exists(config_file_path)):
		print("Could not find", config_file_name, "at", config_file_path)
		exit(1)

	if (p.install):
		install_path = p.install
		install_mod(install_path, config_file_path)

	elif (p.uninstall):
		uninstall_path = p.uninstall
		uninstall_mod(uninstall_path, config_file_path)

	elif (p.list):
		list_mods(config_file_path)

	elif (p.backup):
		backup_path = p.backup
		backup_config(backup_path, config_file_path)

	else:
		print("No valid parameter provided. You can use -h in order to see the valid possibilities.")
