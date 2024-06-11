from chat_config import GPTAPIFacade
from pre_data_process import *

import os
from os import walk

from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
 
# accessing and printing value
openai_api_key=os.getenv("API_KEY")

if openai_api_key is None:
  print("No API key detected from .env file. Please insert key as 'API_KEY= ... '")

else:
  mypath = './tests/'

  filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
  sheet_name='Analysis Output'
  facade = GPTAPIFacade(openai_api_key)

  for filename in filenames:
    table_string = get_combined_table_string(mypath + filename, sheet_name)
    facade.update_instruction(table_string)

  quiz = ""
  answer = ""


  while quiz != 'E':
    print('press E to finish this app')
    quiz = input('User Question:\n')
    if quiz == 'E' or quiz == 'e':
      break
    print("System Answer:")
    response = facade.answer_with_gpt_4(quiz)

    for item in response:
      if hasattr(item.choices[0].delta, "content"):
        answer_text = item.choices[0].delta.content

        if answer_text is not None:
          print(answer_text, end="")
          answer += answer_text
        else:
          answer_text = ""
    facade.track_conversation(quiz, answer)
    answer = ""
    print("\n")