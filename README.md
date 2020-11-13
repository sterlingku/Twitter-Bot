This bot will reply to specific keywords when you '@<bot-name>' in a tweet.  Currently, the bot looks for '#helloworld!', '#helloworld', 'quotes', and 'quote'.

Example tweets: 
- @AutoKuBot #helloworld!
- @AutoKuBot give me a quote please
- quotes are nice @AutoKuBot

For this app to work correctly:
- (respond-bot.py ran locally only - Heroku doesn't write to files) Ensure the tweet_log.txt file exists and has an integer value on the first row.  The code looks for an int value to decide where to start the script.
- Ensure quotes.txt file exists and contains one quote per row.
- When testing locally, ensure you have a '.env' file with your API keys/secrets.  You will need to comment/uncomment some code to make the API calls locally vs. on Heroku
- If you need to generate a text file of all the previous @ mentions, comment out the 'api.update_status' lines, so that the script can write to the tweet_log.txt without running into a duplicate or already favorited issue

Additional notes:
- Added a 12 second sleep timer due to Twitter API call limits

There are many resources out there to learn how to use Heroku.  I will provide the basic steps to deploy this app:
1. On Heroku: create app, connect to GitHub repo, enable automatic updates, and enter your API keys/secrets in the Config Vars section
2. Install pipreqs onto machine by running the command: 'pip install pipreqs'
3. Run pipreqs in project folder to create 'requirements.txt' doc: 'pipreqs <project folder location>'.  This file is required for Heroku to know what packages to install
4. Create a 'runtime.txt' file and add python version in case python needs to run in a specific version such that dependencies are compatible
5. Create 'Procfile' for Heroku to run specific commands.  This is required for Heroku to know which 'workers' to enable
6. Commit and push code to GitHub and wait for build to complete on Heroku.  Enable workers on Heroku

If you run into issues, install Heroku CLI and run the following commands to troubleshoot:
1. heroku login -i
2. enter username and password
3. heroku logs --tail --app <app-name>


Learning courtesy of: https://youtu.be/W0wWwglE1Vc
Deployment courtesy of: https://www.youtube.com/watch?v=iLvMYXKIcPo
See Twitter rate limits: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/faq


Future Enhancements:
- add quotes to MongoDB
- add stats, so users can see their metadata when they @mention