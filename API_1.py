import openai
import os
from info import Caller
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = ' 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'
openai.api_key  = os.getenv("OPENAI_API_KEY")

def get_completion(input, cur_caller, model="gpt-3.5-turbo"):
    
    if cur_caller.incident_type == "XXX":
        type_prompt = f"""
        Determine the emergency type.
        emergency types: FIRE CALLS, POLICE CALLS, EMS CALLS
        Output the type only.
        If any of the information is not available, put XXX as the value.
        ```{input}```
        """
        etype = [{"role": "user", "content": type_prompt}]
        etype_res = openai.ChatCompletion.create(
            model=model,
            messages=etype,
            temperature=0.1, # lower the 随机性 it is
        )
        etype_res = etype_res.choices[0].message["content"]
        print(etype_res)
        cur_caller.incident_type = etype_res
    
    if cur_caller.incident_location == "XXX":
        location_prompt = f"""
        Determine the incident location from the message. This should be an address or a defining location.
        If the information is not explicitly available, put XXX as the value.
        ```{input}```
        """
        # The output should be in the format "Apartment Number", "Street Number", 
        # "Street Name". The output should be a dictionary.
        location = [{"role": "user", "content": location_prompt}]
        location_res = openai.ChatCompletion.create(
            model=model,
            messages=location,
            temperature=0.1, # lower the 随机性 it is
        )
        location_res = location_res.choices[0].message["content"]
        cur_caller.incident_location = location_res

    if cur_caller.caller_name == "XXX":
        name_prompt = f"""
        Determine the name of the caller.
        Output the name only.
        If any of the information is not explicitly available, put XXX as the value.
        ```{input}```
        """
        name = [{"role": "user", "content": name_prompt}]
        name_res = openai.ChatCompletion.create(
            model=model,
            messages=name,
            temperature=0.1, # lower the 随机性 it is
        )
        name_res = name_res.choices[0].message["content"]
        cur_caller.caller_name = name_res

    if cur_caller.symptoms == "XXX":
        if cur_caller.incident_type == 'EMS CALLS':
            sym = "XXX"
            sym_prompt = f"""
                Determine the symptoms of the medical emergency.
                Output in a list format of symptoms
                If any of the information is not available, put XXX as the value.
            ```{input}```
            """
            sym = [{"role": "user", "content": sym_prompt}]
            sym_res = openai.ChatCompletion.create(
                model=model,
                messages=sym,
                temperature=0.1, # lower the 随机性 it is
            )
            sym_res = sym_res.choices[0].message["content"]
            cur_caller.symptoms = sym_res
        else:
            cur_caller.symptoms = "N/A"
            
    
    # cur_caller = Caller(caller_name = name_res, symptoms = sym, incident_type = etype_res, incident_location = location_res)
    cur_caller.print_info()
    return cur_caller
    
    #return response.choices[0].message["content"]

# text = f"""
#     My name is Amy. My friend fell down the stairs. Her ankle is swollen and 
#     her nose is bleeding. We are in 100 College St.\
# """
# get_completion(text)
# location_prompt = f"""
#     Determine the incident location from the message. 
#     The output should be in the format "Apartment Number", "Street Number", 
#     "Street Name". The output should be a dictionary.
#     If any of the information is not available, put N/A as the value.
# ```{text}```
# """
# location = get_completion(location_prompt)

# type_prompt = f"""
#     Determine the emergency type.
#     energency types: FIRE CALLS, POLICE CALLS, EMS CALLS
# ```{text}```
# """
# etype = get_completion(type_prompt) 

# name_prompt = f"""
#     Determine the name of the caller.
# ```{text}```
# """
# name = get_completion(name_prompt)

# if etype == 'EMS CALLS':
#     sym_prompt = f"""
#         Determine the symptoms of the medical emergency.
#         Output in a list format of symptoms
#     ```{text}```
#     """
#     sym = get_completion(name_prompt) 


# cur_caller = Caller(caller_name = name, symptoms = sym, incident_type = etype, incident_location = location)

# print(cur_caller.print_info)
'''
emergency -> 
type -> 
address -> street name / apartment number / N/A

medical -> 
fire -> 

number of ambulence
severity

special case -> emergency
'''
