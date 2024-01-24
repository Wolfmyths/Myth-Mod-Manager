As long as there's an opened issue, please take a look and send a pull request of your contribution!

There are plans to maybe even add a wiki.

## Things to know when contributing

+ `start_MMM.bat` and `start_MMM.sh` are the scripts that starts the program
+ The program auto-adjusts paths if running via script or EXE
+ If you want to compile an exe on your system, run `createEXE.bat` or `createEXE.sh`
+ Variables that are used throughout the project are stored in `constant_vars.py`
+ Please keep your code formatting consistent with the rest of the project
+ **Use the `future-update` branch when submitting commits and PRs**

## Automated Testing

To make sure everything works, before submitting a PR please run PyTest to double check your code.

PyTest doesn't cover every function yet but it covers most of it.

### How to run PyTest

1. Open your terminal and make sure your current directory is the repository
2. Execute command `python3 -m venv /venv`
   + Steps 1-2 do not have to be repeated once done
3. Start the venv via:
   + Windows: `venv/scripts/activate.bat`
   + Linux (bash/zsh): `venv/bin/activate`
4. Install/Update dependencies in the venv `pip install -r requirements.txt`
5. Execute command `pytest tests` and it should work

If you have any questions, [contact me](https://github.com/Wolfmyths) on one of my socials.