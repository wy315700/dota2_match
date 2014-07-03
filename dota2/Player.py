from dota2Error import Dota2APIError

class Player():
    def __init__(self, matchref):
        # Reference to the match this player was in
        self.match = matchref

        # Basic player info
        self.account_id = None
        self.player_slot = None
        self.hero_id = None

        # Detailed player info

