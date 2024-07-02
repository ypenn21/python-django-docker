from unittest.mock import patch, MagicMock  # Import MagicMock here
from src.api.llm_service import LLMService
import unittest


class LLMServiceTests(unittest.TestCase):
    @patch('src.api.llm_service.OpenAI')
    def test_list_llms(self, mock_openai):
        # Mock the OpenAI client and its response
        mock_response = MagicMock()
        mock_response.choices = [
            {
                "message": {
                    "content": "```json\n[{\"model_name\": \"model1\", \"domain\": \"domain1\", \"description\": \"description1\"}, {\"model_name\": \"model2\", \"domain\": \"domain2\", \"description\": \"description2\"}]```"
                }
            }
        ]


        mock_openai.return_value.chat.completions.create.return_value = mock_response

        # Initialize the LLMService with mock project ID and region
        llm_service = LLMService(project_id='test-project', region='us-central1')

        # Call the get_llms method
        llms = llm_service.get_llms()

        # Assert that the returned list is not empty
        self.assertNotEqual(llms, [])

        # Assert that each item in the list is a dictionary with the expected keys
        for llm in llms:
            self.assertIn('model_name', llm)
            self.assertIn('domain', llm)
            self.assertIn('description', llm)
if __name__ == '__main__':
	unittest.main(warnings = 'ignore')