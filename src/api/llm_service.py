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
        required_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        creds, project = google.auth.default(scopes=required_scopes)
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)

        # Initialize OpenAI with Vertex AI endpoint and credentials
        self.endpoint= f'https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/endpoints/openapi'
        self.client = OpenAI(
            api_key=creds.token,
            base_url=f'https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/endpoints/openapi'
        )
    def list_llms(self):
        """
        Prompts Gemini to list available foundational models in Vertex AI Managed AI Service.
        """
        response = self.client.chat.completions.create(
            model="google/gemini-1.5-pro-001",
            messages=[
                {
                    "role": "user",
                    "content": "What foundational models are available in model garden in Vertex AI Managed AI Service? Give me a list of 5 foundational models including Gemini models in json format with properties model_name, domain, and description."
                },
                {'role': 'system',
                'content': 'You are a expert on google cloud AI and its suite of services including Vertex AI Managed AI Service'
                }
            ])
        return self.parse_response(f'{response.choices[0]}')
    # def list_llms(self):
    #     return self.parse_response("\"message\": {\"content\": \"```json[{}]```\"")
    #implement the function parse_response by parsing out the json string enclosed by ```json ```using regex, and parse the json string to json.
    def parse_response(self, response):
        print(response)
        # Find JSON string enclosed by ```json ... ```
        match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                # Parse the extracted JSON string
                cleaned_json_string = re.sub(r'\\n*', '', json_str)
                return json.loads(cleaned_json_string)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in response.")
                return []
        else:
            print("Error: No JSON string found in response.")
        # If no JSON found or parsing failed, return an empty list
        return []

    def get_llms(self):
        llms = self.list_llms()
        if not llms:
            raise ValueError("No LLMs available")
        return llms