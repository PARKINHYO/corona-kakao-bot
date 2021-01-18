# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
*/5 9-11 * * * python /home/ubuntu/CoronaBot/function1.py
0,30 13,17 * * * python /home/ubuntu/CoronaBot/function1.py
*/3 7-22 * * * python /home/ubuntu/CoronaBot/function2.py
0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57 23 * * * python /home/ubuntu/CoronaBot/function2.py
* 5 * * * cd /home/ubuntu/CoronaBot/Text/Cities/; rm *
*/5 7-22 * * * python /home/ubuntu/CoronaBot/function3.py
0,5,10,15,20,25,30,35,40,45,50,55 23 * * * python /home/ubuntu/CoronaBot/function3.py
