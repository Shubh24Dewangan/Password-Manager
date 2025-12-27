from db import Database
from security import hash_password, encrypt_password, decrypt_password

class PasswordManager:
    def __init__(self):
        self.db = Database()
        self.user = None

    def signIn(self):
        username = input("Enter your Username: ").strip()
        check = self.db.get_user(username)
        if check:
            print('This user already exists!')
            return False
        
        master_pass = input('Create your Master Password: ')
        self.db.add_user(username, hash_password(master_pass))
        print('Account has been created!!!')

    def logIn(self):

        username = input('Enter your Username: ').strip()
        user = self.db.get_user(username)
        if not user:
            print(f'User with username {username} does not exists!')
            return False
        
        master_pass = input('Enter your Master Password: ')
        if hash_password(master_pass) != user[2]:
            print('Wrong Password!')
            return False
        
        self.user = user
        print("You're successfully Logged In!")
        return True
    
    def addCredential(self):

        site = input("Enter Site name: ").strip()
        login_user = input("Login username (optional): ").strip()
        pswd = input("Password: ").strip()
        encrypted = encrypt_password(pswd)
        self.db.add_vault(self.user[0], site, encrypted, login_user)
        print("✅ Password saved!")

    def viewCredential(self):

        creds = self.db.get_vault(self.user[0])
        if not creds:
            print('No saved Credentials...!')
            return
        
        for i in creds:
            print(f"site : {i[0]}, username : {i[1]}, password : {decrypt_password(i[2])}")
    
    def deleteCredential(self):

        site = input('Enter site name you want to delete: ')
        self.db.delete_vault(self.user[0], site)
        print(f'site : {site} has been deleted.')
        return
                
    def menu(self):
        while True:
            print('\nPress 1 to Add Credential.')
            print('Press 2 to see Credential(s).')
            print('Press 3 to Delete Credential(s).')
            print('Press {e} to Exit..')

            choice = input('Enter your Choice: ').strip()
            if choice == '1':
                while True:
                    self.addCredential()
                    ask = input('Type {y} to confirm deleting more else {n}: ')
                    if ask not in 'yY':
                        break
            elif choice == '2':
                self.viewCredential()

            elif choice == '3':
                while True:
                    self.deleteCredential()
                    ask = input('Type {y} to confirm deleting more else {n}: ')
                    if ask not in 'yY':
                        break
            
            elif choice == 'e':
                print('Thank You!!')
                break

            else:
                print('Invalid Choice!!')

    def mainMenu(self):
        print('----------------Password Manager----------------\n')
        while True:
            print('1. Sign Up your account!')
            print('2. Log In to your Account!')
            print('3. Exit...')

            choice = input('Enter your choice: ').strip()
            if choice == '1':
                self.signIn()
            elif choice == '2':
                if self.logIn():
                    self.menu()

            elif choice == '3':
                print('Thank you!')
                break

            else:
                print('Invalid Choice!!')

        self.db.close()

if __name__ == "__main__":
    appObj = PasswordManager()
    appObj.mainMenu()