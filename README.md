Learning courtesy of: https://youtu.be/W0wWwglE1Vc

For this app to work correctly:
- Remove all Reply Tweets on AutoKuBot's Twitter.  It won't post duplicates.
- Ensure the last_seen.txt has only one line on the first row.  Remove empty lines.

Deploy to Heroku:
1. Connect to GitHub repo
2. Install pipreqs onto machine: 'pip install pipreqs'
3. Run pipreqs in project folder to create requirements.txt doc: 'pipreqs <folder location>'
4. Create runtime.txt and add python version in case python needs to run in a specific version such that dependencies are compatible
5. Create Procfile for Heroku to run specific commands