
import json

SEMESTER = "13981"
users = []
sess_data = {}

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.dep_id = '2903' 
        self.courses = []
    
    def search_course(self):
        pass
        
    # def __eq__(self, num):
    #     return self.chat_id == num

 
def get_user(chat_id):
    for user in users:
        if user.chat_id == chat_id:
            return user
    u = User(chat_id)
    users.append(u)
    return u

def load_data():
    global sess_data
    f = open('scrap/' + SEMESTER + '.txt', 'r')
    sess_data = json.loads(f.read())
    f.close()


load_data()