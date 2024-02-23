import mongoengine
from datetime import datetime
from database.models import Bets

def clean_past_bets():
    # Get the current time
    now = datetime.now()

    # Query the database for bets with a GameTime in the past and delete them
    Bets.objects(GameTime__lt=now).delete()
