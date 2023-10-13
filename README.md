# Myth Mod Manager

A simple mod manager for PAYDAY 2 to make managing all of those files a little bit easier.

<img src="./assets/icon.png" width="150" height="150" align="right">

![GitHub all releases](https://img.shields.io/github/downloads/Wolfmyths/Myth-Mod-Manager/total)
![GitHub contributors](https://img.shields.io/github/contributors/Wolfmyths/Myth-Mod-Manager)
![License](https://img.shields.io/badge/License-MIT-blue)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Framework](https://img.shields.io/badge/Framework-PySide6-green)
![Platform](https://img.shields.io/badge/OS-Windows-blue)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C4MJZS9)

# Features

* Disable mods you don't want to use at the moment.
    + *This feature is good for testing out which mod is crashing the game!*

* Search bar to find the installed mod you're looking for in seconds.

* Create profiles to organize your mods.

* Delete mods from your computer.

* Automatic installation by dragging and dropping files into the program.
    + This also includes automatic unzipping.

    + *You still have to choose what type of mod it is (mods, mod_overrides, maps)*

* Easy to access buttons for your game directory, crash logs, and starting the game.

* Backup all of your mods and package it into a compressed file.
  
* Auto detects and installs Myth Mod Manager's updates.

**Like all PAYDAY 2 Mods, [Super BLT](https://superblt.znix.xyz/) is required to run mods**

# Showcase

<img src="./assets/preview.png" width="600" height="600" alt='Preview'>

<br>

# Anti-Virus False Positives (And building the exe yourself)

There have been multiple reports from users that anti virus programs believe the program contains
a trojan.

[This issue is being worked on](https://github.com/Wolfmyths/Myth-Mod-Manager/issues/22)

Rest assured, this program does not contain malicious code.

**When a release is published, github builds the executable as seen [here](https://github.com/Wolfmyths/Myth-Mod-Manager/blob/main/.github/workflows/release.yml), not me.**

If you still are suspicious, you can build the executable yourself with these steps:

1. [Install Python 3.11](https://www.python.org/downloads/)
2. Clone this repository
3. Run `createEXE.bat`
4. After the `createEXE.bat` automatically closes, there will be a folder created called `Myth Mod Manager` which contains the newly compiled executable. This is created within the repository.
5. Move `Myth Mod Manager` to your preferred directory and start it.

# Supported Platforms

### Reguarding OS

At the moment this is only supported on windows due to some dependencies
and their features being windows exclusive

There are plans to release on Linux

See more about it in [this issue here](https://github.com/Wolfmyths/Myth-Mod-Manager/issues/18)

### Reguarding Storefront

It works with both steam and epic games versions.

# Download
You may download any version of Myth Mod Manager and view changelogs at the [releases page](https://github.com/Wolfmyths/Myth-Mod-Manager/releases)

# Future Plans

+ New Icon/Logo
+ Duplicate mod detection
+ Auto mod type detection
+ Linux support
+ Some kind of [modworkshop.net](https://modworkshop.net/g/payday-2) integration, see [issue #14](https://github.com/Wolfmyths/Myth-Mod-Manager/issues/14)

*Suggestions are appreciated!*

# Contributing

As long as there's an opened issue, please take a look and send a pull request of your contribution!

There are plans to add a CONTRIBUTING.md and maybe even a wiki.

### Things to know when contributing

+ `start_MMM.bat` is the script that starts the program
+ The program auto-adjusts paths if running via script or EXE
+ If you want to compile an exe on your system, run `createEXE.bat`
+ Variables that are used throughout the project are stored in `constant_vars.py`
+ Please keep your code formatting consistent with the rest of the project
+ **Use the other branch which includes the next update when submitting commits and PRs**

If you have any questions, [contact me](https://github.com/Wolfmyths) on one of my socials.
