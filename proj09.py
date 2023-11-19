###########################################################
#  Computer Project #9
#
#    define functions
#       1. open file
#       2. read file
#       3. add prices 
#       4. get max price of company 
#       5. find max company price 
#       6. get avg price of company 
#       7. display list 
#    define main
#       print the welcoming banner
#       open both files and create your master dictionary by calling the respective functions
#       always display the options, and then ask for the user input. Re-prompt on invalid input.
#       options:
#           if option == '1':
#               Display the title first. "Companies in the New York Stock Market from 2010 to 2016" which should be 105 characters long and centered. Print the set of companies, sorted alphabetically. After sorting, print it calling the display_list function.
#           if option == '2':
#               same as option 1 but with the companies’ code instead of the names. Then print the title first "\ncompanies' symbols:"
#           if option == '3':
#               ask the user for the company symbol, re-prompt if the company symbol is not in the master dictionary. Use the symbol to find the max price of that company. Then print the  message with the price and the date. If there were no prices, then print an appropriate message.
#           if option == '4':
#               Find the company with the maximum stock price by calling find_max_company_price. Print the company’s name and stock price.
#           if option == '5':
#               Prompt for a company symbol; re-prompt if it is not in the master dictionary. Find the average high price. If there were no prices, then print an appropriate message.
#           if option == '6':
#               Quit the program
###########################################################

import csv
from operator import itemgetter

MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"
    
def open_file():
    '''
    This function is going to ask the user for both files to open. You will\
        keep looping for the first one until a file is open. Afterwards, you \
            have to do the same for the second file.
    Parameters: None
    Returns: Two file pointers. (file pointer of prices, and the file pointer \
                                 of securities) in that order
    '''
    file_pointer_price = None
    file_pointer_security = None
    file_pointer_price = input("\nEnter the price's filename: ")
    while True:
        try:
            file_pointer_price = open(file_pointer_price, "r")
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            file_pointer_price = input("\nEnter the price's filename: ")
    file_pointer_security = input("\nEnter the security's filename: ")
    while True:
        try:
            file_pointer_security = open(file_pointer_security, "r")
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            file_pointer_security = input("\nEnter the security's filename: ")
    return file_pointer_price, file_pointer_security

def read_file(securities_fp):
    '''
    This function takes the security’s file pointer that has the names of the\
        companies and their codes.
    securities_fp: A file pointer
    Returns: set, dictionary
    '''
    reader = csv.reader(securities_fp)
    next(reader, None)
    D = {}
    names = set()
    for line in reader:
        code = line[0]
        name = line[1]
        sector = line[3]
        subsector = line[4]
        address = line[5]
        date_add = line[6]
        line_list = [name, sector, subsector, address, date_add, []]
        D[code] = line_list
        names.add(name)
    return names, D

def add_prices (master_dictionary, prices_file_pointer):
    '''
    This function does not return anything, but it changes the master \
        dictionary while reading the prices file.
    master_dictionary, prices_file_pointer: dictionary, file pointer
    Returns: None
    '''
    reader = csv.reader(prices_file_pointer)
    next(reader, None)
    for line in reader:
        date = line[0]
        symbol = line[1]
        open_info = float(line[2])
        close_info = float(line[3])
        low_info = float(line[4])
        high_info = float(line[5])
        line_list = [date, open_info, close_info, low_info, high_info]
        if symbol in master_dictionary:
            master_dictionary[symbol][5].append(line_list)

def get_max_price_of_company (master_dictionary, company_symbol):
    '''
    This function takes the master dictionary and a company symbol, and it \
        gets the max high price and the date of the max price.
    master_dictionary, company_symbol: dictionary, string
    Returns: (float, string)
    '''
    master_list = []
    if company_symbol not in master_dictionary or \
        master_dictionary[company_symbol][5] == []:
        return None, None
    for price_list in master_dictionary[company_symbol][5]:
        date = price_list[0]
        high_info = price_list[4]
        my_tuple = (high_info, date)
        master_list.append(my_tuple)
    return max(master_list)

def find_max_company_price (master_dictionary):
    '''
    This function takes the master dictionary and finds the company with the\
        highest high price.
    master_dictionary: dictionary
    Returns: (string, float)
    '''
    new_list = []
    for item in master_dictionary:
        company_high = get_max_price_of_company(master_dictionary, item)
        if company_high == (None, None):
            continue 
        else:
            my_tuple = (item, company_high[0])
            new_list.append(my_tuple)
        new_list = sorted(new_list, key = itemgetter(1), reverse = True)
    return new_list[0]

def get_avg_price_of_company (master_dictionary, company_symbol):
    '''
    This function uses the master dictionary and company symbol to find the\
        average high price for the company.
    master_dictionary, company_symbol: dictionary, string
    Returns: float
    '''
    master_list = []
    avg = 0
    if company_symbol in master_dictionary.keys():
        value = master_dictionary[company_symbol][5]
        for num in value:
            price = num[4]
            master_list.append(price)
            avg = (sum(master_list))/(len(master_list))
    elif company_symbol not in master_dictionary.keys(): 
        return 0.0
    return round(avg,2)
            
def display_list (lst):  # "{:^35s}"
    '''
    This function does not return anything, but it takes a list of strings and\
        displays that list in three columns, each column is 35 characters wide.
    lst: list of strings
    Returns: None
    '''
    tally = 0
    for line in lst:
        print("{:^35s}".format(line), end = "")
        tally += 1
        if tally == 3:
            print()
            tally = 0
    print('\n')

def main():
    print(WELCOME) #print the welcoming banner 
    fp_price, fp_security = open_file() #open both files
    set_1, master_dictionary = read_file(fp_security) #create your master dictionary
    add_prices(master_dictionary, fp_price) #add prices to the dictionary 

    print(MENU) #display the options
    prompt = input("\nOption: ") #ask for the user input
    while prompt != "6": #if 6 break, else countinue or reprompt for correct option 
        if prompt == "1":
            print('\n{:^105s}'.format\
                  ("Companies in the New York Stock Market from 2010 to 2016")) #display the title first which should be 105 characters long and centered
            sorted_set = sorted(set_1) #print the set of companies, sorted alphabetically
            display_list(sorted_set) 
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

        elif prompt == "2": #same as option 1 but with the companies’ code instead of the names
            print("\ncompanies' symbols:") #display the title
            sorted_code = sorted(master_dictionary.keys()) #print the set of company codes, sorted alphabetically
            display_list(sorted_code)
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

        elif prompt == "3":
            company_symbol = input("\nEnter company symbol for max price: ") #ask the user for the company symbol
            while company_symbol not in master_dictionary: # re-prompt if the company symbol is not in the master dictionary
                print("\nError: not a company symbol. Please try again.")
                company_symbol = input\
                    ("\nEnter company symbol for max price: ")

            max_price = get_max_price_of_company(master_dictionary, \
                                                 company_symbol) # Use the symbol to find the max price of that company

            if max_price[0] is not None: #print the message with the price and the date 
                print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".\
                      format(max_price[0], max_price[1]))
            else: #If there were no prices, then print an appropriate message
                print("\nThere were no prices.")
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

        elif prompt == "4": #Find the company with the maximum stock price
            max_company = find_max_company_price(master_dictionary) 
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".\
                  format(max_company[0], max_company[1])) #Print the company’s name and stock price
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

        elif prompt == "5": 
            company_symbol = input\
                ("\nEnter company symbol for average price: ") #Prompt for a company symbol
            while company_symbol not in master_dictionary: #re-prompt if it is not in the master dictionary
                print("\nError: not a company symbol. Please try again.")
                company_symbol = input\
                    ("\nEnter company symbol for average price: ")

            avg_price = get_avg_price_of_company(master_dictionary, \
                                                 company_symbol) #Find the average high price

            if avg_price != 0.0:
                print("\nThe average stock price was ${:.2f}.\n".format\
                      (avg_price))
            else: #If there were no prices, then print an appropriate message
                print("\nThere were no prices.")
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

        else: #Re-prompt on invalid input
            print("\nInvalid option. Please try again.") #prompt invalid input  
            print(MENU) #display the options
            prompt = input("\nOption: ") #ask for the user input

if __name__ == "__main__": 
    main()