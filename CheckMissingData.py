from info import Caller

def check(cur_caller):
    # do a for loop going through each required information. 
    # If None, have a prompt audibly ask for the information
    if cur_caller.caller_name == "XXX":
        return "What is your name?"
    elif cur_caller.incident_location == "XXX":
        return "Where are you?"
    elif cur_caller.incident_type == "XXX":
        return "What is the emergency?"
    elif cur_caller.symptoms == "XXX":
        return "What are the symptoms?"
    else:
        return None
    
    
    