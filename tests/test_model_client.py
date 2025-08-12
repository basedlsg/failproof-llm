import os
import unittest
from unittest.mock import MagicMock, patch

from backend.adapters.model_client import GeminiModelClient


class TestGeminiModelClient(unittest.TestCase):
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    @patch("dotenv.load_dotenv")
    def test_execute_success(
        self, mock_load_dotenv, mock_configure, mock_generative_model
    ):
        # Arrange
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
            client = GeminiModelClient()

            # Act
            result = client.execute("Test prompt")

            # Assert
            self.assertEqual(result, "Test response")
            mock_load_dotenv.assert_called_once()
            mock_configure.assert_called_once_with(api_key="test_key")
            mock_generative_model.assert_called_once_with("gemini-1.5-flash")
            mock_model_instance.generate_content.assert_called_once_with("Test prompt")

    @patch("dotenv.load_dotenv")
    def test_init_no_api_key(self, mock_load_dotenv):
        # Arrange
        with patch.dict(os.environ, {}, clear=True):
            # Act & Assert
            with self.assertRaises(ValueError) as context:
                GeminiModelClient()
            self.assertTrue(
                "GEMINI_API_KEY not found" in str(context.exception)
            )
        mock_load_dotenv.assert_called_once()


if __name__ == "__main__":
    unittest.main()