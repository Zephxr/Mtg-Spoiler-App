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
