# Edit-Me-Webserver

[![Python 3.8](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://www.python.org/downloads/release/python-380/)

**Edit-Me-Webserver** is a local webserver skeleton which handles GET and POST requests and uses a simple flat-file data store written in pure python. It is meant as an introduction to webserver development in python.

## Getting Started

1. Download the [Python 3 installer](https://www.python.org/downloads). I reccomend the most recent version, but note that this project has only been tested on Python 3.8.0

2. Run the installer. All the default settings are fine and these settings can always be modified in the future.

3. Download the Edit-Me-Webserver code from github. Clone or Download > Download Zip. Unzip the file to wherever you'd like.

## Running and Editing

**Run the webserver:** Locate the `webserver.py` file and click on it to open it with Python. A black box should open up indicating that the webserver is running.

**Look at the website:** By default, the server's address is `http://localhost:8080`. Just type this into a web browser and have a look at the site.

**Stop the webserver:** Right now the only way to stop the server is by closing the window it's running in. Find the black python text window and close it.

*Start Editing!* Open any of the files in a text editor to look at the code and start editing. I reccomend an editor such as [Notepad++](https://notepad-plus-plus.org/downloads) which is well suited to simple code editing.

## File Map

    .
    ├── datafiles            # Directory for all files created by DataStore.py
    │   └── names.json       # The guestlist storage file
    ├── res                  # resources used by the webpage
    │   ├── favicon.ico      # A tiny image this displays in the webpage tab in the browser
  	│   └── style.css        # Stylist information such as font and text colors
    ├── DataStore.py         # A helper module I wrote to store files with
    ├── README.md            # This document you're reading right now
    ├── index.html           # The webpage itself, ready to have information templated into it
    └── webserver.py         # The main webserver code


## Going Forward

There are a multitude of features and practices missing from this project. When you're ready, consider broadening your understanding from the list below:

**Git and Version Control** — If you find yourself having trouble undoing bad changes or saving multiple copies of files as backups, consider using a version control system like [Git](https://gitforwindows.org).

**Input Validation** — If a website allows users to enter their own info into a website, there's a lot of risk of unexpected inputs causing big problems. I would reccomend putting in strong checks that every input looks like what is expected. For instance, is a user's name allowed to contain emoji? Or be 10,000 characters long? Or contain `<i>HTML</i>`?

**Database** — The DataStore utility is easy to use and run, but it's flimsy. If the server crashes while writing data it could lose it all. And it's pretty slow. This issue of persistantly storing data has been solved though with Database software, which is easy to integrate into a Python application. I reccomend getting started with [MySQL](https://www.mysql.com), which is free and easy to install on Windows.

**Templating Engine** — Right now we're using string.Template to insert data into the page. It is easy, but doesn't have many features. If you want to start putting a lot of data into the webpage each load, you should consider a templating engine like [Jinja](https://jinja.palletsprojects.com/en/2.10.x).