# Sprint Stats
This is a python script you can run after a completed sprint to gather some statistics about that sprint from JIRA.

## License
[Apache 2](http://www.apache.org/licenses/LICENSE-2.0)

## Contributing
Feel free to fork the repository and submit any useful changes back as via a pull request.


## Usage

### Prerequisites
To use the script, you need a few things.
* The url for a valid JIRA instance (e.g. https://company.atlassian.net)
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

Alternatively, you can specify the credentials on the command line. See the help-text.

###Run your sprint stats
Once you've got your credentials set up, you can process some stats!

    $ sprintstats -b "My Board" -t "My Sprint" --project "AProject"

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


### Scripts and Options

    $./sprintstats -h
    usage: sprintstats [-h] [--user USER] [--password PASSWORD] [-P]
                       [--list-boards] [--server SERVER] [--board [BOARD]]
                       [--sprint [SPRINT]] [--project PROJECT] [--config CONFIG]
                       [--json]

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
                            The name or id of the rapidboard that houses the
                            sprint for which you want to gather stats.
      --sprint [SPRINT], -t [SPRINT]
                            The name of the sprint on which to produce the stats
      --project PROJECT, -r PROJECT
                            The project for which to gather backlog stats
      --config CONFIG, -c CONFIG
                            The path to a config file containing jira server
                            and/or credentials (See README.md)
      --json, -j            Produce output in JSON format


##Wiki-fy the results
If you want to create a sprint review wiki page, you can pipe the json output from the `sprintstats` script into the `wikifysprint` script.

    usage: wikifysprint [-h] [--user USER] [--password PASSWORD] [-P]
                        [--server SERVER] [--config CONFIG] [--space SPACE]
                        [--parent [PARENT]] [--title TITLE]

    Create a new Confluence page with sprint stats

    optional arguments:
      -h, --help            show this help message and exit
      --user USER, -u USER  The Confluence user name to used for auth. If omitted
                            the current user name will be used.
      --password PASSWORD, -p PASSWORD
                            The Confluence password to be used for auth.
      -P                    Prompt for password.
      --server SERVER, -s SERVER
      --config CONFIG, -c CONFIG
                            The path to a config file containing Confluence server
                            and/or credentials (See README.md)
      --space SPACE, -e SPACE
                            The space that will contain the created/updated page
      --parent [PARENT], -r [PARENT]
                            The parent of the created/updated page.
      --title TITLE, -t TITLE
                            The title of the created/updated page

This script will use the same credentials files in the same precedence as the statistics gathering sscript.

###Using the two together
    sprintstats -b "My Board" -t "My Sprint" -r "AProject" --json | wikifysprint -e "Team Space" -t "My Sprint Review"

