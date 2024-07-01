from google.cloud import aiplatform
from random import choice
import random
from openai import OpenAI
import json
import google.auth.transport.requests
import google.auth
import re


class LLMService:
    """
    A class to retrieve a random LLM from a list of available LLMs in Vertex AI Managed AI Service.
    """
    def __init__(self, project_id, region):
        self.project_id = project_id
        self.region = region

        # Obtain credentials
        creds, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)

        # Initialize OpenAI with Vertex AI endpoint and credentials
        self.endpoint= f'https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/endpoints/openapi'
        self.client = OpenAI(
            api_key=creds.token,
            base_url=f'https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/endpoints/openapi'
        )

    def list_llms(self):
        response = self.client.chat.completions.create(model='google/gemini-1.5-pro-001',
        messages=[{
            'role': 'user',
            'content': 'What foundational models are available in model garden in Vertex AI Managed AI Service? Give me a list of 5 foundational models including Gemini models in json format with properties model_name, domain, and description.'
        },
        {'role': 'system',
        'content': 'You are a expert on google cloud AI and its suite of services including Vertex AI Managed AI Service'
        }])
        models = self.parse_response(response)
        return models

    def parse_response(self, response):
        text = f'{response}'
        # text = jsonModelResponse.choices[0].message['content']
        # Remove the leading and trailing triple backticks and "json" keyword
        # Extract the content from the response

        # Use regular expression to find the JSON string
        match = re.search(r'```json(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            print(json_str)
            try:
                # Parse the JSON string
                cleaned_json_string = re.sub(r'\\n*', '', json_str)
                print(cleaned_json_string)
                model_list = json.loads(cleaned_json_string)
                return model_list
            except json.JSONDecodeError:
                pass

        # If no JSON found or parsing failed, return an empty list
        return []

    def get_random_llm(self):
        llms = self.list_llms()
        if not llms:
            raise ValueError("No LLMs available")
        return llms