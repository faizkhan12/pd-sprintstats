#Sprint Stats
This is a python script you can run after a completed sprint to gather some statistics about that sprint from JIRA.

## Usage
### Prerequisites
To use the script, you need a few things.
* The url for a valid JIRA instance (e.g. https://pagerduty.atlassian.net)
* A user with access to that instance (e.g. jdiller)
* That user's password.

The easiest thing to do is make a config file and specify these things there using the following format: 

    [default]
    user=YOUR_USER
    server=https://pagerduty.atlassian.net/
    password=YOUR_PASSWORD

The script will look for the config file in the following locations (if found, the higher item on this list takes precedence):
* In the location specified in the command line with the `--config` or `-c` option.
* A file named `config.cfg` in the current working directory.
* A file named `.sprintstats.cfg` in the current user's home directory *Recommended*
* `/usr/local/etc/sprintstats.cfg`
* `/etc/sprintstats.cfg`

Alternatively, you can specify them on the command line. See the help-text.

###Run your sprint stats
Once you've got your credentials set up, you can process some stats!

*Note*: You need to know either the name or the id of your JIRA Rapidboard where you're tracking your sprints. If you prefer the succintness of an id you can use the `--list-boards` command line option to find the ID of your board and specify that.

    $ sprintstats -b "My Board" -t "My Sprint"

    Completed Issues
    ================
    MB-2      As a user I can print my schedule
    MB-3      As a user I can export my schedule as a PDF file
    MB-4      As an admin I can give users permission to print or export schedules

    Incomplete Issues
    =================
    MB-9      As a user I can export my schedule as a CSV file
    MB-14     As a user I can import a schedule from a CSV File

    Cycle Time Statistics
    =====================
    cycle_time_stddev   :12.1537766029
    velocity            :44.0
    min_cycle_time      :4
    average_cycle_time  :16.0
    max_cycle_time      :38


##Development
The script is written in python 2.7 and has a number of dependencies. For ease, it's recommended you use a virtual environment
for development purposes.

If you haven't developed in python before, you may need a couple of additional tools to get up and running, namely `pip` and `virtualenv`
Run the following commands in a terminal to get them set up.

    $ sudo -H easy_install pip
    $ sudo -H pip install virtualenv

Once those are installed, and you've cloned this repository you're all set.

    $ cd /path/to/pd-sprintstats
    $ virtualenv env
    New python executable in env/bin/python
    Installing setuptools, pip...done.

    #activate the virtualenv
    $ . env/bin/activate

    #install the required libraries
    $ pip install -r requirements.txt
    Downloading/unpacking jira==0.39 (from -r requirements.txt (line 1))
      Downloading jira-0.39-py2.py3-none-any.whl (42kB): 42kB downloaded
    ...etc



The script should now be ready to run. Try it out.

    $./sprintstats -h

    usage: sprintstats [-h] [--user USER] [--password PASSWORD] [-P]
                       [--list-boards] [--server SERVER] [--board [BOARD]]
                       [--sprint [SPRINT]] [--config CONFIG]

    Gather some statistics about a JIRA sprint

    optional arguments:
      -h, --help            show this help message and exit
      --user USER, -u USER  The JIRA user name to used for auth. If omitted the
                            current user name will be used.
      --password PASSWORD, -p PASSWORD
                            The JIRA password to be used for auth. If omitted you
                            will be prompted.
      -P                    Prompt for password.
      --list-boards, -l     When supplied, a list of RapidBoards and their
                            associated IDs are displayed
      --server SERVER, -s SERVER
      --board [BOARD], -b [BOARD]
                            The id of the rapidboard that houses the sprint on
                            which you want to gather stats. (Use --list-boards to
                            find it
      --sprint [SPRINT], -t [SPRINT]
                            The name of the sprint on which to produce the stats
      --config CONFIG, -c CONFIG
                            The path to a config file containing jira server
                            and/or credentials (See README.md)


