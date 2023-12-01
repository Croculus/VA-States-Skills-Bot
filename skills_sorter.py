import VA_TeamGen, requests, re


teams = []
class Team(VA_TeamGen.Team):
    def __init__(self, number, name, id) -> None:
        super().__init__(number, name, id)
        self.driver = int
        self.auto = int
        self.skills = int #total of driver and auto
        self.qualified = bool

def parser(file):
    f = open(file, 'r')
    for line in f.readlines():
        num = re.search('([0-9])+[A-Z]', line).string
        name = re.search
        Team(num, name, id)