# eBook Reader for Raspberry Pi

This repository contains the code for an eBook reader designed to run on a Raspberry Pi. The application is set up to start automatically whenever the Raspberry Pi is powered on.

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
