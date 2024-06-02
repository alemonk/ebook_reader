# Raspberry Pi E-Paper eBook Reader

## Overview
This project transforms a Raspberry Pi into a dedicated eBook reader using an e-paper display, providing a low-power, paper-like reading experience. It features a custom-built application that parses eBooks into a format suitable for the e-paper display and allows for easy navigation through the book's content.

## Features
- **E-Paper Display Compatibility**: Designed to work seamlessly with e-paper displays, offering excellent readability even in bright sunlight.
- **Automated Book Parsing**: Includes a script to automatically parse ePub files into text files, organizing the content by paragraphs for optimized display.
- **Efficient Navigation**: Utilizes physical buttons for page navigation, with support for both single and double press actions to move between pages.
- **Pre-Rendering Pages**: Enhances performance by pre-rendering all pages of the book, storing them as individual text files for quick access and display.
- **Screensaver Functionality**: Features a screensaver mode that displays random literary quotes when the reader is idle, enriching the user experience.
- **Network Management**: The system intelligently manages network connectivity, disabling it during reading to save power and re-enabling it as needed.
- **Robust Error Handling**: Implements error handling to ensure stability and provides informative logging for troubleshooting.

## How It Works
1. **Initialization**: On startup, the Raspberry Pi fetches the latest code from the repository and ensures that the WiFi is active.
2. **Book Selection**: Users can select the book they wish to read by specifying the title in the provided script.
3. **Parsing**: The included ePub parser converts the selected book into a series of text files, each representing a screen's worth of content.
4. **Reading**: The main application (`read_book.py`) handles the display of the book's content on the e-paper screen, responding to button presses to navigate through the book.

## Installation and Setup

Follow these steps to install and set up the eBook reader on your Raspberry Pi:

1. **Clone the Repository**: Clone this git repository to your Raspberry Pi and navigate to the directory containing the repository. You can do this with the following commands:
    ```bash
    git clone git@github.com:alemonk/ebook_reader.git
    cd ebook_reader
    ```

2. **Run the Install Script**: Execute the `install.sh` script. This script installs necessary dependencies and sets up a Python virtual environment. Run the script with the following command:
    ```bash
    bash install.sh
    ```

3. **Modify rc.local**: Open the `/etc/rc.local` file with a text editor (such as nano) with root permissions:
    ```bash
    sudo nano /etc/rc.local
    ```
    Before the line that says `exit 0`, insert the following command:
    ```bash
    cd /path/to/repository/ebook_reader && bash run.sh &
    ```
    Make sure to modify `/path/to/repository/ebook_reader` with the correct path.
    Save and exit the file.

4. **Reboot**: Finally, reboot your Raspberry Pi with the following command:
    ```bash
    sudo reboot
    ```

After following these steps, the eBook reader application will start automatically whenever the Raspberry Pi is powered on. Enjoy your reading!

## Troubleshooting

Epaper display manual: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi .

If you encounter issues where the Raspberry Pi doesn’t execute the program on reboot, it’s important to check the `/etc/rc.local` file. The file should look like this:

```bash
#!/bin/bash
cd /path/to/repository/ebook_reader && bash run.sh &
exit 0
```
Ensure that the shebang line (`#!/bin/bash`) is present at the top of the file. This line specifies the interpreter for the script. Also, make sure that the exit 0 line is at the end of the file. This line signifies that the script has finished executing successfully.

If you’re still experiencing problems, a good way to troubleshoot is to check the system logs. Depending on your system, you can use either `sudo journalctl` or `sudo cat /var/log/syslog`. These commands will display system logs that can help identify any errors.

For example, to check for rc.local related entries in the system logs, you can use `sudo journalctl | grep rc.local` or `sudo cat /var/log/syslog | grep rc.local`.
