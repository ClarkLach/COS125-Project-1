# File: LaChance_p1.py
# Author: Clark LaChance
# Date: 17 Nov 2022
# Section: 1 # E-mail: clark.lachance@maine.edu
# Description:
# Calculates sentiment of words based on ratings provided in a training file. Allows user several functions
# such as highest/lowest scoring words in a file, finding sentiment of a specific word, and average score of a file.
# Collaboration:
# I did not collaborate with any of my peers on this assignment.

TRAINING = "movieReviews.txt"

def ConstructDict(text): 
    # Constucts a dictionary based on the words provided in the training file
    # Each key contains a list (min len of 1) of each score found for a given word
    train = open(text, "r") 
    sent_dict = {} 

    for line in train:
        for i in [",", ";", ":", ".", "!", "?", "\n", "\t"]: # Quick way to eliminate puncuation
            line = line.replace(i, "")
        formatted_data = line.split(" ")

        for item in formatted_data[1:]: # Use [1:] to ignore the sentiment score at beginning of list
            item = item.lower() # lowercases all words
            if item not in sent_dict:
                sent_dict[item] = [int(formatted_data[0])] # Specifically add sentiment as an int in a list, so more scores can be appended
            else:
                sent_dict[item].append(int(formatted_data[0]))

    train.close()
    return sent_dict # returns the entire dictionary so it can be used in other functions

def SingleWordSentiment(word, text):
    # Calculates the score of a single user-provided word
    sent_dict = ConstructDict(text) 

    if word not in sent_dict:
        print(f"{word} was not found in the provided data set.")
        print("")
    else:
        sent_list = sent_dict[word] # locates word in dict, computes avg score
        counter = 0
        for i in sent_list:
            counter += i
        avg_score = counter / len(sent_list)

        print(f"\"{word}\" appears {len(sent_list)} times.")
        print(f"The average score for reviews containing \"{word}\" is {avg_score}.")
        print("")

def CleanFile(text):
    # Used to standardize the text in a user-provided file, removes (most) formatting, lowercases all words
    user_file = open(text, "r")
    file_data = user_file.read()

    for i in [",", ";", ":", ".", "!", "?", "\t"]: # Handles data slightly different than training file
        file_data = file_data.replace(i, "") # Treats all words as one long line rather than line by line
    file_data = file_data.replace("\n"," ")

    formatted_data = file_data.split(" ")
    for item in range(len(formatted_data)):
        formatted_data[item] = formatted_data[item].lower()
    
    user_file.close()
    return formatted_data, text # Returns the formatted data as a list of words, also returns the name of file itself
                                # Did this so print statements in other functions can still refer to the file name


def AvgScore(clean_text):
    # Calculates the average score of a user-provided file.
    sent_dict = ConstructDict(TRAINING)
    sent_total = 0
    counter = 0

    for word in clean_text[0]: #needs [0] because both the list and the file name are returned in CleanFile()
        counter += 1
        if word in sent_dict:
            for score in sent_dict[word]:
                this_word = 0
                this_word += score
                sent_total += (this_word / len(sent_dict[word]))

        else:
            sent_total += 2 # Magic number?? If a word is not found I'm adding the neutral value of 2.
    
    avg_score = round((sent_total / counter),3) # Rounds score to 3 decimals
    print(f"The average score of the words in {clean_text[1]} is {avg_score}. ", end="")
    if avg_score > 2.25: # These are hard-coded values provided in the assignment!
        print("This is a compliment.")
    elif avg_score < 1.75:
        print("This is an insult.")
    else:
        print("")
    print("")

def HighLow(clean_text):
    # Calculates the highest and lowest scoring words in a user-provided file
    sent_dict = ConstructDict(TRAINING)
    base_low = 5 # reversing high and low to ensure they will always get replaced in the loop below
    base_high = 0
    low = ""
    high = ""

    for word in clean_text[0]:
        if word in sent_dict:
            counter = 0
            score_total = 0
            for score in sent_dict[word]:
                counter += 1
                score_total += score
            word_avg = (score_total / counter)

            if (word_avg) < base_low:
                base_low = word_avg
                low = word
            if (word_avg) > base_high:
                base_high = word_avg
                high = word

    print(f"The most positive word in {clean_text[1]} is {high} with a score of {base_high}.")
    print(f"The most negative word in {clean_text[1]} is {low} with a score of {base_low}.")
    print("")


def main():
    while True:
        print("What would you like to do?")
        print("   1. Calculate the sentiment score of a single word")
        print("   2. Calculate the average score of words in a file")
        print("   3. Find the highest and lowest scoring words in a file.")
        print("   4. Exit the program")

        user_input = input("Enter a number 1-4: ")
        if user_input == "1":
            user_word = input("Enter a word: ")
            SingleWordSentiment(user_word, TRAINING)

        elif user_input == "2":
            user_file = input("Enter the name of the file with words: ")
            AvgScore(CleanFile(user_file))

        elif user_input == "3":
            user_file = input("Enter the name of the file with words: ")
            HighLow(CleanFile(user_file))

        elif user_input == "4":
            print("Goodbye!")
            break # only way to exit the program by breaking the main while loop

        else:
            print("Not a valid input!")

main()