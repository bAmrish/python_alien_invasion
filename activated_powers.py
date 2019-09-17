from power import PowerType
from threading import Timer


class ActivatedPowers:
    """ This class manages activated powers for the game. """

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.powers = []

    def activate(self, power_type: PowerType):
        print('Power activated: ' + str(power_type))
        self.powers.append(power_type)
        timer = Timer(10, self.deactivate_power, [power_type])
        timer.start()

    def deactivate_power(self, power_type: PowerType):
        print('Power deactivated: ' + str(power_type))
        self.powers.remove(power_type)

    def is_active(self, power_type: PowerType):
        return power_type in self.powers


