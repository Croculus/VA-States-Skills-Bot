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
    
    def generateEvents(self, data) -> None:
        highest_total = 0
        for i in range(len(data)): #sort data into types of runs 
            skills_run = data[i]
            next_run = data[i+1]

            #event vars
            driver= 0
            auto = 0
            total = 0

            if skills_run['type'] == 'driver': #check for a driver run
                driver = skills_run['score']
                total = driver
                if next_run['type'] == 'programming' and skills_run['event']['id'] == next_run['event']['id']: #works under the assumption that the corresponding auto run will always be ahead of the skills
                    auto = next_run['score']
                    

            else:
                auto = skills_run['score']
                total = auto
            
            if total > highest_total:
                self.driver = driver
                self.auto = auto
                self.score = total 
  


    def toSheets(self) -> [str, str, int, int, int, bool]:
        return [self.name, self.number, self.score, self.driver, self.auto, self.qualified] 


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
    response = response.json()
    data = response['data']
    
        #  ~~  program design decision comment  ~~
        # So right now there are a couple ways I could try to find the highest total skill score for a team
        # Since the total skills score is the sum of the auto + driver at a single event, and given the way that runs of both types are indexed in the list within the API, I could either
        # A: Try to match each auto run with a driver run for that same event, then compare to other event pairs and add (all in this function)
        # B: Add all the runs to the class function and make a function that sorts it
        # C: Record each event for every team (which I was going to do later so I could update more frequently when events are live) and dig for skills score 

        #decided to go with A b/c of least amount of calls and comparisons
    
    try:
        pass
    except:
        print('Something went wrong when trying to write to team {}'.format(team.number))


