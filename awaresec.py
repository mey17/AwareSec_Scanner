def print_large_title(title):

    bold_start = "\033[1m"
    bold_end = "\033[0m"
    green_color = "\033[32m"  # Green color code
    
    print(f"{bold_start}{green_color}{title}{bold_end}")


def printTitle():
    title_text = """
                                                 _____                           
                     /\                         / ____|                          
  ______ ______     /  \__      ____ _ _ __ ___| (___   ___  ___   ______ ______ 
 |______|______|   / /\ \ \ /\ / / _` | '__/ _ \\___ \ / _ \/ __| |______|______|
                  / ____ \ V  V / (_| | | |  __/____) |  __/ (__                 
                 /_/    \_\_/\_/ \__,_|_|  \___|_____/ \___|\___|                
                                                                                 
                                                                                """
    print_large_title(title_text)
    print("https://awaresec.am                  v.1.2                  © Copyright 2024 awaresec.am or one of its authors.")

printTitle()    
