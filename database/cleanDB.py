from datetime import datetime
from database.models import Bets
from mongoengine import connect
import ./constants


def clean_past_bets():
    # Get the current time
    now = datetime.now()

    # Connect to the database
    connect(db='betterPicks', host=constants.MONGO_URI)

    # Query the database for bets with a GameTime in the past and delete them
    Bets.objects(GameTime__lt=now).delete()

#clean_past_bets()
