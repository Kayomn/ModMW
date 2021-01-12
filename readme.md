# ModMW

# Overview

A really simple Python3 script I wrote in one night for managing OpenMW mods.

Currently there are choices in the script that prevent it from working on platforms other than OpenMW for Linux.

# How to Use

ModMW supports 4 commands right now:

  * `install path/to/mod_dir`: Registers a data directory and any of its BSA files with OpenMW's VFS.
  * `uninstall path/to/mod_dir`: Unregisters a data directory and any of its BSA that has previously been registered.
  * `list`: Lists all currently installed mod data directories in order of file overwrite priority, from first (lowest) to last (highest).
  * `backup path/to/backup/location`: Backs up the `openmw.cfg` file in its current state to the given file path.

This manager makes some assumptions about the file contents when uninstalling mods, such as any `content` declarations immediately following the target `data` declaration line belong to it. As such, manually editing the data / content lines is not recommended.
