import requests

teams = []
class Team():
    def __init__(self, number, name, id) -> None:
        self.number = str(number)
        self.name = str(name)
        self.id = int(id)

    def __str__(self) -> str:
        return "Num: {}, Name: {}, Id:{}\n".format(self.number, self.name, str(self.id))
        

def response_handler(response, i):
    yield response['data'][i]

def is_VA(team):
    if team['location']['region'] == 'Virginia':
        teams.append(Team(team['number'], team['team_name'], team['id']))

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiZWU2Njc5NTFiYTc3Y2RjNzFkMzdiOWQxNjc5MjRlMDdiZDI1NmI1NGE0NmVmYjVmZjRhOTBjNDcwYmJjYzMyOGNiNTM5ZDY2ZjExYjAxYmQiLCJpYXQiOjE3MDEzODg4MTIuMzMwNTU0LCJuYmYiOjE3MDEzODg4MTIuMzMwNTU3MSwiZXhwIjoyNjQ4MDczNjEyLjMyMDUzOSwic3ViIjoiMTExOTQ5Iiwic2NvcGVzIjpbXX0.bJV4fPtk1HL0Gn2N8iQDK_JpoqMbGqciqv076H5Qd79LK8eLeqypdeyV3j3y0qJP0YX_qAyoow6HPjbK31vCMcSNwVfi6fovhIqYV_flRsM4wbORqyvg44pm6aWft0UXVrDRI8idMHONdjp-_CfA4eYH767t1nAsNeT6XsYbVA-4Td86Uef3XZ_oYJVuHPC7Cy9NSPbg-xyAFdOtDLWcqf5FJ4U6bnQKbusy3HT6YwbQ8Z0YrLm3WFbevJljIU3W4ombuHBqxwbm6coL_Psgctco3_na4Q0t0WxGpUBV67RSUTKxrMDqW1nXF4FuDZiaVkyd1LO-ehvtpizDxH0XHyTs8HTUJj_0WjKUwcdG_4yz-RMExDJo2O_Ev8-3Xe_e5RKEqdCxWFKi2JxwwAOkefPGvtiFNM8w-OB6ZbTOUOiV8I2U7otMtfOmLE4nWy0J_CF5ew3e4cluD-JV39HGQS4Y7n-e_4jh3QqxdGTOcKXdvs6M4foI6MhWj8aCVeDynmFcUhfLdxaRdgYNtqAFBVhE7rCLz-P4ff7SdtFG7gR4IqgBrLXXsWueVMcRMgOTjqi-tq8FYk7uTC6zx7Hiu9eTtPupya6A-igi-HtW_pod7tOA6Su-3zIbQWDqV9AbafZwqo2cQmQpVpqMAEnbJUjbPReNQssCdsgfZ30Lsx4'
header = {
    'Authorization': 'Bearer '+token,
    'accept':'application/json'
           }
for i in range(1,30):
    print('page:{}'.format(str(i)))
    response = requests.get('https://www.robotevents.com/api/v2/teams?registered=true&program%5B%5D=1&grade%5B%5D=High%20School&country%5B%5D=US&myTeams=false&per_page=250&page={}'.format(str(i)), headers=header)
    response = response.json()
    for i in range(len(response['data'])):
     is_VA(next(response_handler(response, i)))

file = open('teams.txt', 'w')
for i in teams:
    print(str(i))
    file.write(str(i))
file.close()