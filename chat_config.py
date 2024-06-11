import tiktoken
import openai as OpenAI

class GPTAPIFacade:
  def __init__(self, openai_api_key, segment_limit=1000, temperature=0.5):
    self.temperature = temperature
    self.segment_limit = segment_limit
    self.model = 'gpt-4-turbo'
    self.client = OpenAI.OpenAI(api_key=openai_api_key)
    self.searchableDataFrame = None
    self.instructionText = "You will be given tables extracted from an Analysis Output data from a business and tables were extracted from an excel sheet. There might be some issues while extracting tables. Anyway, assist users by answering in text as details, exactly what they want."
    
    self.initialize_message_history()
  
  def initialize_message_history(self):
    self.message_history = [
        {"role" : "system", "content" : self.instructionText}
      ]
    
  def update_instruction(self, new_instructionText : str):
    self.message_history.append(
        {"role" : "system", "content" : new_instructionText}
    )

  def answer_with_gpt_4(self, prompt: str, max_tokens: int = 40000) -> str:
      chat_messages = self.prep_gpt_4_answer(prompt, max_tokens)
      response = self.client.chat.completions.create(model=self.model, messages=chat_messages, temperature=0.0, stream=True)
      return response
  
  ENC = tiktoken.encoding_for_model('gpt-4')
  @classmethod
  def get_number_of_token(cls, str):
     return len(cls.ENC.encode(str))

  def prep_gpt_4_answer(self, prompt: str, max_tokens: int = 40000  ) -> str:
      chat_messages = self.message_history + [{"role" : "user", "content": prompt}]
      
      chat_message_string = ' '.join([temp_message["role"] + " " + temp_message["content"] for temp_message in chat_messages])
      while GPTAPIFacade.get_number_of_token(chat_message_string) > 80000:
          self.message_history.pop(1)
          chat_messages.pop(1)
          
      
      return chat_messages
  
  def track_conversation(self, prompt, response_content):
      self.message_history.append({"role" : "user", "content": prompt})
      self.message_history.append({"role" : "assistant", "content": response_content})