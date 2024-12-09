# Mtg-Spoiler-App

# # BEFORE YOU RUN mtg.py!

Run generateAllSets.py first.  This will make all_sets.txt which will be your base for sets you do and don't want to send to discord.  Copy all sets from here that you don't want sent to discord and put them in old_sets.txt.  The sets will show up in order of most recent ---> oldest.  

# Usage
- python3 -m venv venv
- Activate the venv
  - Windows
    - cd venv\Scripts\activate.bat
  - Linux
    - source venv/bin/activate
- pip install -r requirements.txt

- Make webhook.py in the main directory and inside the file, put a line that says:

```
webhook = r"<DISCORD WEBHOOK URL>"
```

But replace the <...> with your channels webhook url.

# Advanced Use (Linux or WSL2 for Windows)

To have this run consistently, you can run this as a cronjob.

To run this as a cronjob you will need to either have a Linux machine or WSL2 installed on your windows computer.
If you don't for some reason have cron on your machine, do:
```
sudo apt install cron
```

After, do:
```
crontab -e
```

This will open your crontab and here you can install a cronjob.  Example cronjob would be something like this:
```
*/5 * * * * ~/Mtg-Spoiler-App/venv/bin/python3 ~/Mtg-Spoiler-App/mtg.py >> ~/Mtg-Spoiler-App/mtg.log 2>&1
```

This will run every 5 minutes and output all errors to the log file.
