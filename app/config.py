# app/config.py
#import os

#class Config:
 #   SQLALCHEMY_DATABASE_URI = os.getenv(
  #      'DATABASE_URL',
   #     'mysql+pymysql://root:@localhost/followup_db'
    #)
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SCHEDULER_INTERVAL_MINUTES = int(os.getenv('SCHEDULER_INTERVAL_MINUTES', '1'))




   # app/config.py

class Config:
    # Force MySQL connection (no fallback to SQLite)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/followup_db'

    # Disable modification tracking to avoid warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Scheduler interval in minutes
    SCHEDULER_INTERVAL_MINUTES = 1



