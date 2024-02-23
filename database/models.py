from mongoengine import Document, StringField, DateTimeField, DictField, ListField, FloatField

class Bets(Document):
    BetProvider = StringField(required=True)
    GameTime = DateTimeField(required=True)
    HomeTeam = StringField(required=True)
    AwayTeam = StringField(required=True)
    Bets = DictField(
        Spread=ListField(
            DictField(
                Team=StringField(required=True),
                Line=FloatField(required=True),
                Odds=FloatField(required=True),
            )
        ),
        Total=ListField(
            DictField(
                Team=StringField(required=True),
                Line=FloatField(required=True),
                Odds=FloatField(required=True),
            )
        ),
        Moneyline=ListField(
            DictField(
                Team=StringField(required=True),
                Odds=FloatField(required=True),
            )
        ),
    )
