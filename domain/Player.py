class Player():
    hp = 0
    maxHp = 0
    energy = 0
    maxEnergy = 0
    itens = []
    position = (50, 50)
    equipedGun = None
    equipedHelmet = None
    equipedArmor = None
    itens = []
    color = (250,0,0)
    moveSpeed = 5

    def __init__(self, color):
        self.color = color

    def prepare(self):
        self.maxHp = 100
        self.hp = self.maxHp
        self.maxEnergy = 100
        self.energy = self.maxEnergy
        self.moveSpeed = 5
