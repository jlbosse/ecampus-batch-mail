# ecampus_batch_mail.py

A short script to easily send out corrected exercise sheets to all your students using python.

## Installation
None really. Clone this repo and put `send_mails.py` and `config.ini` wherever you
deem to be a good place. You may want to run a 
```bash
$ chmox +x send_mails.py
```
to make the script executable without needing to type out `python send_mails.py`.

## Configuration
All configuration is stored in the `config.ini`. The port and adress settings are
currently such that they work with the standard
`maximilian.musterfrau@stud.uni-goettingen.de` addresses. You will still need
to enter your own username and e-mail address though. The password is not saved
but asked for during runtime for security reasons.

## Usage
Running `python send_mails.py` will tell you the following about the usage
of the script:

```manpage
usage: send_mails.py [-h] [-f FILES [FILES ...]] [-s SUBJECT] [-m MESSAGE]
                     [-a ADDRESSLIST]

Automatically send out the corrected sheets to all students.

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        List of files you want to send. Must be of the form
                        'stuff_<name>_morestuff' where <name> must be before
                        the last underscore
  -s SUBJECT, --subject SUBJECT
                        The subject of the E-Mail
  -m MESSAGE, --message MESSAGE
                        A file with the contents of the E-Mail.Any occurence
                        of '<name>' will be replaced withthe recipients name
  -a ADDRESSLIST, --addresslist ADDRESSLIST
                        A csv file containing <name>, <email-address>
```
 