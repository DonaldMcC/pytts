# store credentials
# from https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only?rq=1
import os

def getCredentials():
    import base64

    splitter='<PC+,DFS/-SHQ.R'
    directory='C:\\PCT'

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(directory+'\\Credentials.txt', 'r') as file:
            cred = file.read()
            file.close()
    except:
        print('I could not file the credentials file. \nSo I dont keep asking you for your email and password everytime you run me, I will be saving an encrypted file at {}.\n'.format(directory))

        lanid = base64.b64encode(bytes(input('   LanID: '), encoding='utf-8')).decode('utf-8')
        email = base64.b64encode(bytes(input('   eMail: '), encoding='utf-8')).decode('utf-8')
        password = base64.b64encode(bytes(input('   PassW: '), encoding='utf-8')).decode('utf-8')
        cred = lanid+splitter+email+splitter+password
        with open(directory+'\\Credentials.txt','w+') as file:
            file.write(cred)
            file.close()

    return {'lanid':base64.b64decode(bytes(cred.split(splitter)[0], encoding='utf-8')).decode('utf-8'),
            'email':base64.b64decode(bytes(cred.split(splitter)[1], encoding='utf-8')).decode('utf-8'),
            'password':base64.b64decode(bytes(cred.split(splitter)[2], encoding='utf-8')).decode('utf-8')}

def updateCredentials():
    import base64

    splitter='<PC+,DFS/-SHQ.R'
    directory='C:\\PCT'

    if not os.path.exists(directory):
        os.makedirs(directory)

    print('I will be saving an encrypted file at {}.\n'.format(directory))

    lanid = base64.b64encode(bytes(input('   LanID: '), encoding='utf-8')).decode('utf-8')
    email = base64.b64encode(bytes(input('   eMail: '), encoding='utf-8')).decode('utf-8')
    password = base64.b64encode(bytes(input('   PassW: '), encoding='utf-8')).decode('utf-8')
    cred = lanid+splitter+email+splitter+password
    with open(directory+'\\Credentials.txt','w+') as file:
        file.write(cred)
        file.close()

cred = getCredentials()

updateCredentials()
