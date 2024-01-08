import requests, re, dotenv, datetime




token =dotenv.get_key('.env','TOKEN') #enviroment virable for token

#headers/parameters to access api
header = {
    'Authorization': 'Bearer '+token,
    'accept':'application/json'
           }
params = {'season[]' : 181} #season = Over Under


reset_time = datetime.datetime.now()

class Team():
    def __init__(self, number, name, id) -> None:
        self.name = name
        self.number = number
        self.id = id
        self.driver = 0
        self.auto = 0
        self.score = self.driver + self.auto #combined total of driver and auto
        self.qualified = bool
        self.events = [int]
    
    def getSkillsScore(self, data) -> None:
        driver_runs = []
        auto_runs = []
        skills_scores =[int, str]
        for skills_run in data: #sort data into types of runs 
            if skills_run['type'] == 'driver':
                skills_run.append(driver_runs)
            else:
                skills_run.append(auto_runs)



    def toSheets(self) -> [str, str, int, int, int, bool]:
        return [self.name, self.number, self.score, self.driver, self.auto, self.qualified] 

class Event():
    def init(self, id):
        self.id = id
        self.driver = 0
        self.auto = 0
    
    def scores(self) -> tuple(int, int, int):
        return self.driver, self.auto, self.driver+self.auto
    

teams = [Team]
qualified  = [Team]

def parser(file):
    f = open(file, 'r')
    for line in f.readlines():
        num = re.search(r'[0-9]+[A-Z]', line).group(0)
        name = re.search(r'Name:\s*([^,]+)[^a-zA-Z0-9]', line).group(1)
        id = re.search(r'Id:\s*([0-9]+)', line).group(1)
        team = Team(num, name, id)
        teams.append(team)
        populate(team)
    isQualified()
    f.close()

def isQualified():
    response = requests.get('https://www.robotevents.com/api/v2/events/53761/teams', params=params, headers=header) #pulling teams from virginia state championship
    response = response.json()
    for team1 in response['data']:
        for team2 in teams:
            if team1['id'] == team2.id:
                team2.qualified = True
                print(team2)
                qualified.append(team2)
                

def populate(team: Team):
    response = requests.get('https://www.robotevents.com/api/v2/teams/{}/skills'.format(team.id), params=params, headers=header)
    print(response.text)
    time.sleep(1)
    response = response.json()
    data = response['data']
    
    event_id = None
    try:
        for run in data:
            run
        #  ~~  program design decision comment  ~~
        # So right now there are a couple ways I could try to find the highest total skill score for a team
        # Since the total skills score is the sum of the auto + driver at a single event, and given the way that runs of both types are indexed in the list within the API, I could either
        # A: Try to match each auto run with a driver run for that same event, then compare to other event pairs and add (all in this function)
        # B: Add all the runs to the class function and make a function that sorts it
        # C: Record each event for every team (which I was going to do later so I could update more frequently when events are live) and dig for skills score 

  
    except:
        print('Something went wrong when trying to write to team {}'.format(team.number))





parser('teams.txt')