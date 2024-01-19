import requests, re, dotenv, datetime, time, json




token =dotenv.get_key('.env','TOKEN') #enviroment virable for token

#headers/parameters to access api
header = {
    'Authorization': 'Bearer '+token,
    'accept':'application/json'
           }
params = {'season[]' : 181} #season = Over Under


reset_time = datetime.datetime.now()

class Team():
    def __init__(self, number, name, id, qualified) -> None:
        self.name = name
        self.number = number
        self.id = id
        self.driver = 0
        self.auto = 0
        self.score = self.driver + self.auto #combined total of driver and auto
        self.qualified = qualified
    
    def findSkillsScore(self, data) -> None:
        highest_total = 0
        for i in range(len(data)): #sort data into types of runs 
            skills_run = data[i]
            try:
                next_run = data[i+1]
            except:
                next_run = None

            #event vars
            driver= 0
            auto = 0
            total = 0

            if skills_run['type'] == 'driver': #check for a driver run
                driver = skills_run['score']
                total = driver
                if next_run['type'] == 'programming' and skills_run['event']['id'] == next_run['event']['id']: #works under the assumption that the corresponding auto run will always be ahead of the skills
                    auto = next_run['score']
                    total+= auto
                    #iterate over the next program
                    

            else:
                auto = skills_run['score']
                total = auto
            
            if total > highest_total:
                highest_total = total
                self.driver = driver
                self.auto = auto
                self.score = total 

    def getId(self) -> int:
        return self.id

    def toSheets(self) -> [str, str, int, int, int, bool]:
        return [self.name, self.number, self.score, self.driver, self.auto, str(self.qualified)] 


teams = []
qualified  = [Team]

def parser(file):
    loadQualified()
    f = open(file, 'r')
    for line in f.readlines():
        num = re.search(r'[0-9]+[A-Z]', line).group(0)
        name = re.search(r'Name:\s*([^,]+)[^a-zA-Z0-9]', line).group(1)
        id = re.search(r'Id:\s*([0-9]+)', line).group(1)
        team = Team(num, name, id, isQualified(id))
        teams.append(team)
    f.close()

def isQualified(id) -> bool: #helper function for determining who already qualified   
    for qualifiedId in qualified:
        if int(id) == qualifiedId:
            return True
    return False
qualified = []
def loadQualified(): # helper for my helper function
    response = requests.get('https://www.robotevents.com/api/v2/events/53761/teams', params=params, headers=header) #pulling teams from virginia state championship
    response = response.json()
    for team in response['data']:
        qualified.append(team['id'])

def sortHelper(team):
    return team[2] #total skills score of team


def sendTeams():
    parser('teams.txt')
    for team in teams:
        rate_limited = True
        while(rate_limited): # helps with rate limitation
            try:
                response = requests.get('https://www.robotevents.com/api/v2/teams/{}/skills'.format(team.getId()), params=params, headers=header)
                response = response.json()
                team.findSkillsScore(data=response['data'])
                print(team.toSheets())
                rate_limited = False
            except: # once rate limited, wait a bit before pulling more
                time.sleep(5)
                continue
    temp = [team.toSheets() for team in teams]
    temp.sort(reverse= True, key=sortHelper)
    return (json.dumps(temp, indent= 4), 56-len(qualified))

if __name__ == '__main__': # run this every 24 hrs
    sendTeams()