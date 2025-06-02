# # Homework 13: Lithuanian Language Question Answering System

# ## Overview
# Create a Python script that accepts a user's question, determines if it's in Lithuanian language, 
# and if so, provides an answer to the question using an OpenAI language model.

# ## Technical requirements
# - use UV to initialise and store dependencies.
# - Store the code in the github.

# ## Reference Example
# See the example of using structured/JSON response in Python OpenAI at:
# `samples\json-mode\json_mode_applied.py`

# ## Requirements

# 1. **User Input**
#    - Create a console input that accepts a user question
#    - Example: `question = input("Enter your question: ")`

# 2. **Language Detection Model**
#    - Create a Pydantic model for language detection:
#    ```python
#    class LithuanianQuestionCheck(BaseModel):
#        is_lithuanian_language: bool
#    ```

# 3. **JSON Mode Implementation**
#    - Use the 'response_model' parameter in chat completions to parse the response into your model
#    - Make sure to set 'json_mode' correctly in your API call

# 4. **Language Verification**
#    - Add conditional logic to check if the question is in Lithuanian language
#    - Use the parsed response to make this determination

# 5. **Question Answering**
#    - If the question is in Lithuanian, make a second API call to answer the question
#    - Format the response appropriately for display to the user

# ## Submission
# Create a Python script that implements all the requirements above.




import openai
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print

load_dotenv()  # Load environment variables from .env file

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"


question = input("Enter your question: ")
# Complaint letter recogniser

# Generate me a mock complaint letter
complaint_letter = """Dear Customer Service,
I am writing to express my dissatisfaction with the recent purchase I made from your store.
 The product arrived damaged and did not match the description provided on your website. 
 I expected a much higher quality based on the price I paid. I would like a full refund and an apology for the inconvenience caused.
Thank you for your attention to this matter.
Sincerely,"""

love_letter = """ I love you more than words can express."""

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=token,
    base_url=endpoint)

class LithuanianQuestionCheck(BaseModel):
    """
    LetterInformation class for analyzing letter content.

    This class represents information about a letter, specifically focusing on
    whether it is a complaint and the reason for the complaint. It inherits
    from BaseModel to handle data validation and serialization.

    Attributes:
        is_complaint (bool): Indicates whether the letter is classified as a complaint.
        is_complaint_reason (str): The reason or explanation for why the letter is 
                                   classified as a complaint. If is_complaint is False,
                                   this may contain justification for why it's not a complaint. 
                                   Also mention why it is not a complaint
        confidence_score (float): A confidence score indicating the model's certainty
                                   about the classification if it is a complaint or not. 
                                   The score is up to 1 and 0 is the lowest confidence.
    """
    is_lithuanian_language: bool
    is_complaint_reason: str
    confidence_score: float

response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": """You are a helpful assistant that recognises complaint letters. 
             Please let us know if the letter is a complaint or not? Please response with True or False."""},
            {"role": "user", "content": complaint_letter}
        ],
        temperature=0.7,
        response_format=LetterInformation
    )

letter_info = response.choices[0].message.parsed

if letter_info is not None and letter_info.is_complaint:
    print("[bold red]This is a complaint letter.[/bold red]")
    print(f"Reason: {letter_info.is_complaint_reason} with confidence score {letter_info.confidence_score:.2f}")
else:
    print("[bold green]This is not a complaint letter.[/bold green]")
    print(f"Reason: {letter_info.is_complaint_reason} with confidence score {letter_info.confidence_score:.2f}")