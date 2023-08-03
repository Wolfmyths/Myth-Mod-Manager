# Myth Mod Manager

A simple mod manager for PAYDAY 2 to make managing all of those files a little bit easier.

![GitHub all releases](https://img.shields.io/github/downloads/Wolfmyths/Myth-Mod-Manager/total)
![GitHub contributors](https://img.shields.io/github/contributors/Wolfmyths/Myth-Mod-Manager)
![License](https://img.shields.io/badge/License-MIT-blue)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Framework](https://img.shields.io/badge/Framework-PySide6-green)
![Platform](https://img.shields.io/badge/OS-Windows-blue)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C4MJZS9)

# Features

* Disable mods you don't want to use at the moment, and if you want to take it a step further, even delete them from your computer.
    + *This feature is good for testing out which mod is crashing the game!*

* Automatic installation by dragging and dropping files into the program.
    + This also includes automatic unzipping.

    + *You still have to choose what type of mod it is (mods, mod_overrides, maps)*

* Easy to access buttons for your game directory and starting the game.

* Search bar to find the mod you're looking for in seconds

* Backup all of your mods and package it into a compressed file.

In the future there will be profiles so stay tuned for that 😁

**Like all PAYDAY 2 Mods, [Super BLT](https://superblt.znix.xyz/) is required to run mods**

# Supported Platforms

### Reguarding OS

At the moment this is only supported on windows due to some dependencies
and their features being windows exclusive

### Reguarding Storefront

I only have access to the Steam version,
so I cannot say if it works for Epic Games
without feedback.

# Download
You may download any version of Myth Mod Manager and view changelogs at the [releases page](https://github.com/Wolfmyths/Myth-Mod-Manager/releases)

# Future Plans

+ Mod profiles
+ Dark Theme
+ .rar drop-install support
+ Improved visuals
+ Some kind of [modworkshop.net](https://modworkshop.net/g/payday-2) integration, see [issue #14](https://github.com/Wolfmyths/Myth-Mod-Manager/issues/14)

*Suggestions are appreciated!*

# Contributing

As long as there's an opened issue, please take a look and send a pull request of your contribution!

There are plans to add a CONTRIBUTING.md and maybe even a wiki.

### Things to know when contributing

+ `main.py` is the script that starts the program
+ The program auto-adjusts paths if running via script or EXE
+ Test your code through the EXE before submitting a PR, sometimes code will behave differently.
+ If you want to run the program through the EXE, run `createEXE.bat`
+ Variables that are used throughout the project are stored in `constant_vars.py`
+ Please keep your code formatting consistent with the rest of the project

If you have any questions, [contact me](https://github.com/Wolfmyths) on one of my socials.