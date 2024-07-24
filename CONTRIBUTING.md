As long as there's an opened issue, please take a look and send a pull request of your contribution!

There are plans to maybe even add a wiki.

# Things to know when contributing

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

## Translating

### Improving a language (Grammar, punctuation, etc...)

Improving a language is fairly simple. (Except for English because it's hardcoded in the program.)
The translation files are written in XML despite their extension being ".ts"

Translation files are located in the `translations` folder

Here is what a translation entry looks like:
```xml
<context>
    <name>BackupMods</name>
    <message>
        <location filename="../src/threaded/backupMods.py" line="48"/>
        <source>Validating backup folder paths</source>
        <translation>Validación de rutas de carpetas de copia de seguridad</translation>
    </message>
</context>
```

The only thing you have to edit is the text in between the <translation> container.
The text in between the <source> container is the original text from the code.

If you are going to improve English text go to the next section.

### Improving English

We have to be careful when fixing typos in the English language because it is the basis of how other languages are translated.

The number one rule is to NOT HAVE ANY LINE BREAKS OR ESCAPE CHARACTERS in the string.

To fix a typo in the program, you have to unfortunately find it in the source code which is located in `./src`.
If you aren't familiar with programming or python, create an issue and someone or me (wolfmyths) will fix it.

When you see text that is to be translated, it will look like this:
```py
qapp.translate('Options', 'General')
```

The first argument is context for .ts files, the second is the actual text itself

After you have fixed the typo, update the .ts files by opening your terminal and inputting this command:
`util/scrape_translations_needed.py -u`

Make sure you changed directory to the repo otherwise it probably won't work!

### Implementing a new language

To create a new language you can copy and paste `en_US.ts` and then rename the filename, `en_US.ts` is a placeholder with no translations attached.

The naming convention of .ts files are [ISO 649 set 1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) language codes and [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) territory codes seperated by an underscore. The wiki has all the language/territory codes documented.

Open the file and go to line 3, you will see a attribute to the <TS> container tag called `language`. Replace `en_US` with the file name of your language/territory of choice. 

The rest of the process requires a little bit of manual work.
However, there are external python scripts that have been created to help with the process.

In the utils folder of this repo, there is a file called `scrape_translations_needed.py`.
The script looks through a .ts file, checks for missing translations, and then outputs the English text of the missing translations line-by-line in a .txt.
It also updates all .ts files' <source> container tags.

To use the script, make sure you have python and the packages in `requirements.txt` installed.
Open up your command prompt and follow these steps:
1. Change directory to the repo
2. Use the command `util/scrape_translations_needed.py -e -u`

The -e flag is if you want to export the missing translations.
The -u flag is if you want to update the .ts files' source language.

If you used the -e flag, there should be a file named "translation_needed_*language*.txt".
This is what you will be translating.

If you are fluent in your chosen language, translate as many lines as you're willing to contribute your time to.
You can also use a machine translator.

There are a couple things to consider before translating:
+ Seperate each translation entry by pressing the return/enter key, the next script that we will talk about uses line breaks to differentiate between entries
+ Do not have any escape characters (\n, etc) in translations
+ Do not use line breaks in translation entries

After you have translated your script you can now go back to your terminal and type the following command:
`util/update_ts_files path_to_ts_file path_to_translation_file`

The script will update the specified ts file and replace the missing translations with the ones in the translation file and you have your translation!
However the computer won't be able to use this file unless we convert it into a .qm file, which is fairly simple.

Enter this command: `pyside6-lrelease path_to_ts_file -qm ./src/lang/ts_file_name.qm`

All that's left is to add it into the source code, which is located in `src/settings.py`.
On the top of the script you should see a variable named `language_string_to_code`.
Add a new entry to the variable and follow the example of the other entries.
Make sure the key value (the one of the left) is translated.

That is how you add a new language!

For more help see the documentation for .qm and .ts files:
https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html
