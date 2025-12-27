from db import Database
from security import hash_password, encrypt_password, decrypt_password

class PasswordManager:
    def __init__(self):
        self.db = Database()
        self.user = None

    def signIn(self):
        while True:
            username = input("Enter your Username: ").strip()
            if username:
                break

            print('Your username should not be empty!')

        if self.db.get_user(username):
            print('This user already exists!')
            return False
        #add a feature to generate a master password
        master_pass = input('Create a strong Master Password: ')
        try: 
            self.db.add_user(username, hash_password(master_pass))
            print('Account has been created!!')
            return True
        except Exception as e:
            print('Database error. Try again later...')
            return False

    def logIn(self):

        while True:
            username = input("Enter your Username: ").strip()
            if not username:
                print('Your username should not be empty!')
            else:
                break
        user = self.db.get_user(username)
        if not user:
            print(f'User with username {username} does not exists!')
            return False
        
        master_pass = input('Enter your Master Password: ')
        if hash_password(master_pass) != user[2]:
            print('Wrong Password!')
            return False
        
        try:
            self.user = user
            print("You're successfully Logged In!")
            return True
        except Exception as e:
            print('Database error. Try Again later.')
            return False
    
    def addCredential(self):
        while True:
            site = input("Enter Site name/ url: ").strip()
            login_user = input("Login username (optional): ").strip()
            pswd = input("Password: ").strip()
            if len(site) < 4 or len(site) > 100 or len(pswd) < 5:
                print('The length of site name/ url should [4-100] and password should be above 5.\nTry Agian!')
            else:
                break

        try:
            encrypted = encrypt_password(pswd)
            self.db.add_vault(self.user[0], site, encrypted, login_user)
            print("✅ Password saved!")
        except Exception as e:
            print(f'{e}. Try Agaian later!')

    def viewCredential(self):
        try:
            creds = self.db.get_vault(self.user[0])
        except Exception:
            print('Failed to fetch this data. Try Again')

        if not creds:
            print('No saved Credentials...!')
            return

        for i in creds:
            try:
                decrypted = decrypt_password(i[2])
            except Exception:
                decrypted = '[Decryption failed]'

            print(
                f'Site: {i[0]}, '
                f'Username: {i[1]}, '
                f'Password: {decrypted}'
            )
    
    def deleteCredential(self):

        while True:
            site = input('Enter site name you want to delete: ')
            if site:
                break
            print('Site name cannot be empty!')

        try:
            deleted = self.db.delete_vault(self.user[0], site)
            if deleted == 0:
                print('No such site found!')
            else:
                print(f'site : {site} has been deleted.')
        except Exception as e:
            print('Database error..Try Again later!')

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
                    ask = input('Type {y} to confirm adding more else {n}: ')
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