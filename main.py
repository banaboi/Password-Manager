import psycopg2
from _secrets import *
TABLE_NAME = "login_info"


'''
    Inserts data into the login_info database

    Parameters:
        - username : string of the username being entered
        - email : string of the email being entered
        - password : string of the password being entered
        - service : string of the service being entered
'''
def put_into_table(connection, username, email, password, service):
    cursor = connection.cursor()
    put_query = f"""INSERT into {TABLE_NAME} VALUES('{username}', '{email}', '{password}', '{service}');"""
    cursor.execute(put_query)
    cursor.close()
    connection.commit()


'''
    Gets all the data in the database
'''
def get_all_info(connection):
    cursor = connection.cursor()
    get_all_query = f"""SELECT * from {TABLE_NAME};"""
    cursor.execute(get_all_query)
    cursor.close()
    connection.commit()

'''
    Gets the row of data from the database which specifies the login details of the 
    given service

    Parameters:
        - service : string of the service which is being queried
    
    Returns:
        - result : login information in the form of a list of strings
'''
def get_info_by_service(service):
    cursor = connection.cursor()
    get_by_service = f"""SELECT * from {TABLE_NAME} WHERE service = '{service}';"""
    cursor.execute(get_by_service)
    result = cursor.fetchall()
    cursor.close()
    connection.commit()

    return result
'''
    Connects to the database and returns the connection

    Returns:
        - connection : a database connection
'''
def connect_to_db():
    try:
        # Connect to the database #
        connection = psycopg2.connect(
            host = "localhost",
            database = "password_manager_db",
            user = "postgres",
            password = SECRET_PASSWORD
        )
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

'''
    Hashes a word given as a string

    Parameters:
        - word : string to be hashed
    
    Returns:
        - hashed_string : string that is the result after hashing
'''
def hash_string(word):
    hashed_string = ""
    for i in range(0, len(word)):
        hashed_string += chr(len(word)*17 + ord(word[i]))
    
    return hashed_string

'''
    Function which performs an api call to enter information into 
    the database

    Parameters:
        - connection : database connection object
'''
def enter_login_info(connection):
    print("#" * 30)
    username = input("Enter the username: ")
    email = input("Enter the email: ")
    password = input("Enter the soft password: ")
    service = input("Enter the service: ")
    put_into_table(connection, username, email, hash_string(password), service)
    print("Login information added successfully")
    print("#" * 30)
    print("\n")

'''
    Function which performs an api call to fetch information from 
    the database regarding login information for a specific service

    Parameters:
        - connection : database connection object
'''
def look_up_info_by_service(connection):
    print("#" * 30)
    service = input("Which service is this for? ")
    result = get_info_by_service(service)
    print(f"Information --> {result}")
    print("#" * 30)
    print("\n")


if __name__ == "__main__":
    entry = input("Please enter the master password: ")
    if entry == SECRET_PASSWORD:
        print("Welcome to your Password Manager")
        print("#" * 30)
        connection = connect_to_db()
        while True:
            print("What would you like to do?")
            print("1: Enter new login information")
            print("2: Look up login information by service")
            print("3: Quit")
            command = int(input())
            if command == 1:
                enter_login_info(connection)
            elif command == 2:
                look_up_info_by_service(connection)
            else:
                exit()
    else:
        exit()