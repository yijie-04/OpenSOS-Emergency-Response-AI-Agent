import openai
import os
from info import caller
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key  = os.getenv("OPENAI_API_KEY")

def get_completion(input, model="gpt-3.5-turbo"):
    prompt = f"""
    Determine the emergency type.
    energency types: FIRE CALLS, POLICE CALLS, EMS CALLS
    ```{input}```
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.1, # lower the 随机性 it is
    )
    return response.choices[0].message["content"]

text = f"""
    I'm in 100 College St.\
"""
location_prompt = f"""
    Determine the incident location from the message. 
    The output should be in the format "Apartment Number", "Street Number", 
    "Street Name". The output should be a dictionary.
    If any of the information is not available, put N/A as the value.
```{text}```
"""
location = get_completion(location_prompt)

type_prompt = f"""
    Determine the emergency type.
    energency types: FIRE CALLS, POLICE CALLS, EMS CALLS
```{text}```
"""
etype = get_completion(location_prompt) 

type_prompt = f"""
    Determine the emergency type.
    energency types: FIRE CALLS, POLICE CALLS, EMS CALLS
```{text}```
"""
etype = get_completion(location_prompt) 



print(location)



# output
# print(response) 


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
