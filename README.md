# eBook Reader for Raspberry Pi

This repository contains the code for an eBook reader designed to run on a Raspberry Pi. The application is set up to start automatically whenever the Raspberry Pi is powered on.

## Installation and Setup

Follow these steps to install and set up the eBook reader on your Raspberry Pi:

1. **Clone the Repository**: Clone this git repository to your Raspberry Pi and navigate to the directory containing the repository. You can do this with the following commands:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
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
    cd /home/alemonk/ebook_reader && bash run.sh &
    ```
    Save and exit the file.

4. **Reboot**: Finally, reboot your Raspberry Pi with the following command:
    ```bash
    sudo reboot
    ```

After following these steps, the eBook reader application will start automatically whenever the Raspberry Pi is powered on. Enjoy your reading!

