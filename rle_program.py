from console_gfx import ConsoleGfx

# recommend separate functions

def menu_display(): # Prints the menu
    print("RLE Menu")
    print("-" * 8)
    print("0. Exit")
    # reading data and storing in list
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    # call stored variable
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data")

def to_hex_string(data): # translates string to hexidecimal
    # [3, 15, 6, 4] => "3f64"
    total = [] # creates a list to add to
    for item in data[::]: # Goes through each item
        # assigns the numeric values
        if item <= 1 and item >= 9:
            item = item
        elif item == 10:
            item = "a"
        elif item == 11:
            item = "b"
        elif item == 12:
            item = "c"
        elif item == 13:
            item = "d"
        elif item == 14:
            item = "e"
        elif item == 15:
            item = "f"
        item = str(item) # ensures the values are strings
        total.append(item) # adds value to list
    convert = "".join(total) # turns the list into one item
    return convert # returns the item

def count_runs(flat_data): # Returns number of runs of data in a set
    # [15, 15, 15, 4, 4, 4, 4, 4, 4] => int(2)
    count = 0 # Starts the count of the original number
    run_count = 0 # counts sets
    for i in range(0, len(flat_data)): # separates the list
        if flat_data[i-1] == flat_data[i]: # Checks to see if the previous number is the same as the current one
            count += 1 # Adds how many times the count is repreated
            if count == 15: # If there is a set of 15
                run_count += 1 # Counts that as one set
                count = 0 # resets the count to recount for 15
        else: # If not the same
            count = 0 # Resets the count
            run_count += 1 # adds a count if it's different
    return run_count

def encode_rle(flat_data): # counts repeating numbers and puts it in list
    # [15, 15, 15, 4, 4, 4, 4, 4, 4] => [3, 15, 6, 4]
    result = [] # creates list
    count = 1 # starts count of repeats
    for index in range(1, len(flat_data)): # separates values
        if flat_data[index-1] == flat_data[index]: # checks for if a previous number equal the current one
            count += 1 # keeps track of counts
            if count == 15: # If count is at 15
                result.append(count) # # adds repeat amount to list
                result.append(flat_data[index - 1]) # adds number that repeated to list
                count = 0 # resets count value to be able to count to another set of 15
        else: # if it's not a repeat
            result.append(count) # adds number of repeats to list
            result.append(flat_data[index-1]) # adds the number that was repeated to the list
            count = 1 # resets the count for next number
    result.append(count) # adds number of repeats to list
    result.append(flat_data[-1]) # adds number repeated to list
    return result

def get_decoded_length(rle_data): # adds number of repeats
    # [3, 15, 6, 4] => int(9)
    count = 0 # starts track for number of repeats
    for item in rle_data[::2]: # focuses on even index/repeats
        count += item # adds value of even index/repeats
    return count

def decode_rle(rle_data): # prints out list of repeating numbers
    # [3, 15, 6, 4] => [15, 15, 15, 4, 4, 4, 4, 4, 4]
    decode = [] # creates list
    even = 0 # sets value
    for odd in rle_data[1::2]: # separates number to be repeated
        repeat = rle_data[even] # distinguishes how many times number is ro be repeated
        for times in range(0, repeat): # goes through the times the number is to be repeated
            decode.append(odd) # adds repeat number to list
        even += 2 # adds even number to get to the next number in list to be repeated
    return decode

def string_to_data(data_string): # translates hex string to corresponding data list
    # "3f64" => [3, 15, 6, 4]
    data = [] # creates list
    string = list(data_string) # turns string into a list
    for char in string[::]: # goes through each part
        # assigns corresponding value
        if "0" <= char <= "9":
            char = int(char)
        elif char == "a":
            char = 10
        elif char == "b":
            char = 11
        elif char == "c":
            char = 12
        elif char == "d":
            char = 13
        elif char == "e":
            char = 14
        elif char == "f":
            char = 15
        data.append(char) # adds value to list
    return data

def to_rle_string(rle_data): # translates data to RLE
    # [15, 15, 6, 4] => "15f : 64"
    string = [] # creates list
    for i in range(1, len(rle_data), 2): #takes all the even values of the list
        rle_data[i] = hex(rle_data[i])[2:] # turns the item into a hex value and excludes the first two outputs
    for i in range(0, len(rle_data), 2): # takes all the odd value of the list
        rle_data[i] = str(rle_data[i]) # returns the values
    for i in range(0, len(rle_data)): # goes through all the items in the list
        if i % 2 == 0: # if the item is even
            string.append(rle_data[i]) # adds the rle_data
        else: # if the index is odd
            string.append(rle_data[i]) # adds the data
            string.append(":") # adds ":"
    string.pop() # removes the ":" at the end
    string = "".join(string) # turns the list into a string
    return string # returns the string value

def string_to_rle(rle_string): # translates a string in readable rle format
    # "15f : 64" => [15, 15, 6, 4]
    data = rle_string.split(":") # creates a list where each item is split by ":"
    byte_list = [] # forms a new list
    for element in data: # goes through each of the items in rle_string
        if len(element) == 3: # if there are three digits in the item
            first_byte = int(element[0:2]) # isolates the first two digits in list
            last_byte = int(element[-1], 16) # isolates the last digit in list
        elif len(element) == 2:
            first_byte = int(element[0:1]) # isolates first item in list
            last_byte = int(element[-1], 16) # isolates the last item in list
        byte_list.append(first_byte) # adds the first isolated item to new list
        byte_list.append(last_byte) # adds last isolated item to new list
    return byte_list # returns new list

if __name__ == "__main__":
    user_input = 0
    image_data = None
    condition = True
    print("Welcome to the RLE image encoder!")  # Not exact wording
    print("Displaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)  # Prints out the rainbow
    while condition == True:
        menu_display() # Defines the variable to print out what's in the def new_menu
        user_input = input("Select a Menu Option: ")
        if user_input == "0": # Exits the loop
            condition = False
        elif user_input == "1": # Loads the file
            file = input("Enter name of file to load: ") # Loads file if someone inputs it
            image_data = ConsoleGfx.load_file(file) # Loads the file, but does not print
        elif user_input == "2":
            image_data = ConsoleGfx.test_image
            print("Test image data loaded.") # loads the file, but does not print it
        elif user_input == "3":
            file = input("Enter an RLE string to be decoded: ")
            # "3f : 64" (RLE String) => [3, 15, 6, 4] (RLE byte data) = > [15,15,15,4,4,4,4,4,4] (Flat Byte data)
            image_data = decode_rle(string_to_rle(file))
        elif user_input == "4":
            file = input("Enter the hex string holding RLE data: ")
            # "3f64" (RLE Hex String) => [3, 15, 6, 4] (RLE byte data) = > [15,15,15,4,4,4,4,4,4] (Flat Byte data)
            image_data = decode_rle(string_to_data(file))
        elif user_input == "5":
            file = input("Enter the hex string holding flat data: ")
            # "fff444444" (Flat String) = > [15,15,15,4,4,4,4,4,4] (Flat Byte data)
            image_data = string_to_data(file)
        elif user_input == "6":
            print("Displaying image...")
            if image_data == None or image_data == "(no data)":
                print("(no data)")
            else:
                ConsoleGfx.display_image(image_data) # prints the loaded display image
        elif user_input == "7":
            if image_data == None or image_data == "(no data)":
                image_data = "(no data)"
            else:
                # [15,15,15,4,4,4,4,4,4] (Flat Byte Data) => [3, 15, 6, 4] (RLE Byte Data) = > "3f : 64" (RLE String)
                image = to_rle_string(encode_rle(image_data))
            print(f"RLE representation: {image}")
        elif user_input == "8":
            if image_data == None or image_data == "(no data)":
                image_data = "(no data)"
            else:
                # [15,15,15,4,4,4,4,4,4] (Flat Byte Data) => [3, 15, 6, 4] (RLE Byte Data) = > "3f64" (RLE Hex String)
                image = to_hex_string(encode_rle(image_data))
            print(f"RLE hex values: {image}")
        elif user_input == "9":
            if image_data == None or image_data == "(no data)":
                image_data = "(no data)"
            else:
                # [15,15,15,4,4,4,4,4,4] (Flat Byte Data) => "fff444444" (Flat String)
                image = to_hex_string(image_data)
            print(f"Flat hex values: {image}")
        else:
            print("Error! Invalid input.")