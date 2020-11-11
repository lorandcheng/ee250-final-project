#!/usr/bin/env python3

# This file was adapted from http://www.postgresqltutorial.com/postgresql-python/connect/

# The following config() function reads in the database.ini file and returns the connection
# parameters as a dictionary. This function will be imported in to the main python script:

#!/usr/bin/python
from configparser import ConfigParser
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    
    # Checks to see if section (postgresql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
         
    # Returns an error if a parameter is called that is not listed in the initialization file
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db




# import configparser


# def config():
#     config = configparser.ConfigParser()
#     config.read('database.ini')
#     print(config['postgresql'])

#     host = config['postgresql']['host']
#     database = config['postgresql']['database']
#     user = config['postgresql']['user']
#     password = config['postgresql']['password']

#     # return 0

if __name__ == '__main__':
    print(config())