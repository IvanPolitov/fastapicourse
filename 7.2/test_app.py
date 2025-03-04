import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import (app, fetch_random_fact, process_fact, fetch_last_page,
                  process_last_page)


client = TestClient(app)


class TestMain(unittest.TestCase):
    @patch("main.fetch_random_fact")
    @patch("main.process_fact")
    def test_get_and_process_fact(self, mock_process_data: MagicMock, mock_fetch_data: MagicMock):
        mock_response = {"fact": "value", "length": 5}
        mock_fetch_data.return_value = mock_response

        mock_processed_data = "value"
        mock_process_data.return_value = mock_processed_data

        response = client.get("/random_fact")

        mock_fetch_data.assert_called_once()
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"random_fact": "value"})

    @patch("main.fetch_last_page")
    @patch("main.process_last_page")
    def test_get_and_process_last_page(self, mock_process_data: MagicMock, mock_fetch_data: MagicMock):
        mock_response = {
            "current_page": 1,
            "data": [{"fact": "value", "length": 5}],
            "first_page_url": "https:\\catfact.ninja\facts?page=1",
            "from": 1,
            "last_page": 34,
            "last_page_url": "https:\\catfact.ninja\facts?page=34",
            "links": [],
            "next_page_url": "https:\\catfact.ninja\facts?page=2",
            "path": "https:\\catfact.ninja\facts",
            "per_page": 10,
            "prev_page_url": None,
            "to": 10,
            "total": 332
        }
        mock_fetch_data.return_value = mock_response

        mock_processed_data = {"last_page": 34}
        mock_process_data.return_value = mock_processed_data

        response = client.get("/last_page")

        mock_fetch_data.assert_called_once()
        mock_process_data.assert_called_once_with(mock_response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_processed_data)


if __name__ == '__main__':
    unittest.main()
