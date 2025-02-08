import json
from src.services.prompt_service import format_prompt_book_analysis, format_tf_transform
import google.auth.transport.requests
import google.auth
from openai import OpenAI, OpenAIError
from typing import List, Dict, Any
import re

# langchain integration sample: https://github.com/gitrey/gcp-vertexai-langchain/blob/main/03/code.py
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
        """
        Prompts Gemini to list available LLMs in Vertex AI.

        Returns:
            A list of LLM names in JSON format.
        """
        system_message = "You are a helpful AI assistant that can provide information about Vertex AI Managed AI Service. You are able to access and process information from the real world through Google Search and keep your response consistent with search results."
        user_message = 'What foundational models are available in model garden in Vertex AI Managed AI Service? Give me a list of 5 foundational models including Gemini models in json format with properties model_name, domain, and description.'
        response = self.prompt_gemini(system_message, user_message)
        return self.parse_response_to_json(response)

    def tf_transform(self, shell_script: str, context: str) -> str:
        system_message = """You are an expert in Google Cloud Platform (GCP), fluent in `gcloud` commands,
                            deeply familiar with Terraform modules for GCP. """
        user_prompt = format_tf_transform(shell_script, context)
        print(user_prompt)
        response = self.prompt_gemini(system_message, user_prompt)
        return response

    def analysis_book(self, book_title: str, author_name: str, book_pages: List[Dict[str, Any]], keywords: List[str]) -> str:
        system_message = """You are a helpful AI assistant that can provide literary analysis of classic literature books, particularly those from the Shakespearean era. You have access to a vast knowledge base of literary theory, historical context, and the works of Shakespeare himself. 
        Your responses should be insightful, well-written, and demonstrate a deep understanding of literary analysis. 
        """
        user_prompt = format_prompt_book_analysis(
            book={"book": book_title, "author": author_name},
            book_pages=book_pages,
            keywords=keywords
        )
        print(user_prompt)
        response = self.prompt_gemini(system_message, user_prompt)
        return response


    def prompt_gemini(self, system_message: str, user_message: str) -> str:
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model="google/gemini-2.0-flash-001",
                    messages=[
                        {
                            "role": "system",
                            "content": system_message
                        },
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                )
                if response.choices and response.choices[0].message and hasattr(response.choices[0].message, 'content'):
                    return response.choices[0].message.content
                else:
                    retries += 1
                    print(f"OpenAIError: Response content is missing or null. Retrying... (Attempt {retries}/{max_retries})")
            except OpenAIError as e:
                retries += 1
                print(f"OpenAIError: {e}. Retrying... (Attempt {retries}/{max_retries})")
        raise OpenAIError(f"Failed to get response from Gemini after {max_retries} retries.")
    def parse_response_to_json(self, response):
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