from apiCalls import apiMe
from apiCalls import apiChooseUser
from apiCalls import apiSendMail
from apiCalls import apiQueryMail
from apiCalls import apiOneDriveQuery
from apiCalls import apiCreateInboxRule
from apiCalls import apiListInboxRules
from apiCalls import apiRefreshToken
from os import system
import sys

#implemented APIs
apiActions = ['1) Get User/Check Token', 
              '2) Send Email', 
              '3) Query Mail (work/school acct. only)' , 
              '4) Access OneDrive', 
              '5) Create Inbox Rule', 
              '6) List/Delete Inbox Rules', 
              '7) Refresh Token',  
              '\nu) Change User', 
              'q) Quit']

#Choose user from available tokens
def pickUser():
    system('clear')
    user = apiChooseUser.pickUser()
    system('clear')
    return user

def init():
    user = ''
    return user

def main(user):
    while True:

        if user == '':
            try:
                user = pickUser()
            except:
                print('No tokens, make sure token file is present or grab some tokens!')
                return

        print(f'[USER]: {user}\n')
        print('\033[4mAvailable Actions:\033[0m')
        for action in apiActions:
            print(f'{action}')

        #Choose API
        actionChoice = input('\nAction to perform: ')

        if actionChoice == '1':
            apiMe.sendQuery(user)
            system('clear')

        elif actionChoice == '2':
            apiSendMail.sendQuery(user)
            system('clear')

        elif actionChoice == '3':
            apiQueryMail.sendQuery(user)
            system('clear')

        elif actionChoice == '4':
            system('clear')
            apiOneDriveQuery.sendQuery(user)

        elif actionChoice == '5':
            apiCreateInboxRule.sendQuery(user)

        elif actionChoice == '6':
            system('clear')
            try:
                apiListInboxRules.sendQuery(user)
            except:
                print('[-] Error, likely a bad token\n')
                input('Press ENTER to continue...')
                system('clear')

        elif actionChoice == '7':
            apiRefreshToken.sendQuery(user)

        elif actionChoice == 'u':
            system('clear')
            user = apiChooseUser.pickUser()
            system('clear')

        elif actionChoice == 'q':
            system('clear')
            sys.exit()

        else:
            print('[-] Not a valid command')
            input('')
            system('clear')

        continue

if __name__=='__main__':
    user = init()
    main(user)