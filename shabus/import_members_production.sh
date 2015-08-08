DATABASE_URL=$(heroku config:get DATABASE_URL -a shabus) python import_members.py 
