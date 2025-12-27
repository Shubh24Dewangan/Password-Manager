from db import Database
from security import hash_password, encrypt_password, decrypt_password

def main():
    db = Database()
    print('---------> PASSWORD MANAGER\n')

    username = input('Enter your username: ').strip()
    #if user exists then true else false
    user = db.get_user(username)

    if not user:
        master = input('Create a master password: ')
        db.add_user(username, hash_password(master))
        print('Account has been created!!!')
        db.close()
        return
    
    master = input('Enter your master password: ')
    if hash_password(master) != user[2]:
        print('Wrong password!')
        db.close()
        return
    
    print('You are Logged in!!')

    user_id = user[0]

    while True:
        print('\nPress 1 to Add Credentials.')
        print('Press 2 to see your Credentials.')
        print('Press 3 to delete your Credential(s).')
        print('Press {e} to exit!\n')

        choice = input('Enter your choice: ').strip()

        if choice == '1':
            while True:
                site = input('*Enter site name /app name /url: ')
                login_user = input('Enter your login username (optional): ')
                passwd = input('*Enter password: ')
                db.add_vault(user_id, site, login_user, encrypt_password(passwd))
                print('Credentials saved! ✅')
                ask = input('Type {y} to add more otherwise {n}: ')
                if ask not in 'yY':
                    break

        if choice == '2':
            creds = db.get_vault(user_id)
            print(creds) #debug remove later
            if not creds:
                print('No saved Credentials.')
            for i in creds:
                print(f"site : {i[0]}, username : {i[1]}, password : {decrypt_password(i[2])}")
            break

        if choice == '3': # add a function where if site name not present then give another chance
            while True:
                site = input('Enter site name you want to delete: ')
                db.delete_vault(user_id, site)
                print(f'site : {site} has been deleted.')
                choice = input('Type {y} to confirm deleting more else {n}: ')
                if choice not in 'yY':
                    break

        if choice.lower() == 'e':
            break

        else:
            print('Invalid choice!!!')

    db.close()


if __name__ == '__main__':
    main()