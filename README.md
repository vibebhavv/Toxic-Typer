# Toxic-Typer

ToxicTyper is a modified version of BDSMTyper, it is a software tool that allows you to copy and paste text on websites where pasting is not allowed. Works perfectly on ACE Editor and supports pasting on any website using the right control key of the keyboard. ToxicTyper is a single executable file that can be run with just one click, without any installation.

## New Features

-   Tabs for multiple copied content
-   Paste multiple content from tabs just by selecting tabs in background.

## How to use new Feature

-  Start typer and copy multiple answers
-  Press CTRL+Tab_no. (like CTRL+1) and press shortcut you have set to start typing.

## How to use

1. Download the ToxicTyper executable file from the Releases section of this repository.
2. Run the ToxicTyper executable file.
3. In order to paste text on a website where pasting is not allowed, click on START button to activate the ToxicTyper editor.
4. Copy the text you want to paste on the website to the clipboard.
5. Click on the right control key of your keyboard to paste the copied text on the website.

## Build

To build ToxicTyper from the source code, you will need to have PyInstaller installed. PyInstaller is a Python package that can be used to convert Python scripts into standalone executable files.

To install PyInstaller, run the following command:

```
pip install pyinstaller
```

Once PyInstaller is installed, you can use the build.sh script to build the ToxicTyper executable file. To do so, follow these steps:

1. Open a terminal window and navigate to the root directory of the ToxicTyper project.
2. Run the following command to make the build.sh script executable:

```
chmod +x build.sh
```

3. Run the build.sh script by executing the following command:

```
./build.sh
```

4. The build process will start, and once it's complete, you'll find the ToxicTyper executable file in the `dist` directory.

## License

ToxicTyper is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more information.
