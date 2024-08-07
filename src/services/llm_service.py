from google.cloud import aiplatform
from random import choice
import random
from openai import OpenAI
import json
import google.auth.transport.requests
import google.auth
from typing import List, Dict, Any
import re


class LLMService:
    """
    A class to retrieve a random LLM from a list of available LLMs in Vertex AI Managed AI Service.
    """
    def __init__(self, project_id, region):
        self.project_id = project_id
        self.region = region
        # print(f'project_id: {project_id}, region: {region}')
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
        return self.parse_response("")
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