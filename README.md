#Sprint Stats
This is a python script you can run after a completed sprint to gather some statistics about that sprint from JIRA.

##Installation
For now, the easiest way to install this is to clone the repo and run the script inside a python virtualenv.

`
cd /path/to/pd-sprintstats
pd-sprintstats $ virtualenv env
virtualenv env
New python executable in env/bin/python
Installing setuptools, pip...done.

#activate the virtualenv
pd-sprintstats $ . env/bin/activate

#install the required libraries
(env)pd-sprintstats $ pip install -r requirements.txt
Downloading/unpacking jira==0.39 (from -r requirements.txt (line 1))
  Downloading jira-0.39-py2.py3-none-any.whl (42kB): 42kB downloaded
...etc

`

The script should now be ready to run. Try it out.

`(env)pd-sprintstats $./sprintstats.py -h`

`
usage: sprintstats.py [-h] [--user USER] [--password PASSWORD] [-P]
                      [--list-boards] [--server SERVER] [--board [BOARD]]
                      [--sprint [SPRINT]]

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
`

## Usage
### Prerequisites
To use the script, you need a few things.
* The url for a valid JIRA instance (e.g. https://pagerduty.atlassian.net)
* A user with access to that instance (e.g. jdiller)
* That user's password.

The easiest thing to do is make a file called `config.cfg` and specify these things there using the following format: 
`
[default]
user=YOUR_USER
server=https://pagerduty.atlassian.net/
password=YOUR_PASSWORD

`
Alternatively, you can specify them on the command line. See the help-text above.

###Run your sprint stats
Once you've got your credentials set up, you can process some stats!

*Note*: You need to know either the name or the id of your JIRA Rapidboard where you're tracking your sprints. If you prefer the succintness of an id you can use the `--list-boards` command line option to find the ID of your board and specify that.

`(env)pd-sprintstats $./sprintstats.py -b "WorkFlow Scrum Board" -t "Sprint 1"

Completed Issues
================
WF-2      An Admin can set the default severity on a service
WF-23     Conduct discovery for severities
WF-28     Low severity incidents do not escalate
WF-52     SPIKE: Align on Time of Day stories
WF-58     SPIKE: Investigate how severity flows in our 10 most common integrations
WF-59     Don't reassign low-severity incidents to new escalation levels
WF-60     Rename "Severity" to "Urgency"

Incomplete Issues
=================
WF-9      A responder can see the severity of an incident in the email
WF-14     A responder will only be alerted by email for low severity alerts
WF-50     As a Responder, I can filter out low-urgency issues in the mobile app
WF-53     As a user, I can filter and sort my incidents based on severity
WF-54     SPIKE: Investigate changing incident severity
WF-61     SPIKE: Investigate how to map Severity from monitoring systems into PD Urgency
..............
Cycle Time Statistics
=====================
cycle_time_stddev   :12.1537766029
velocity            :44.0
min_cycle_time      :4
average_cycle_time  :16.0
max_cycle_time      :38

`



