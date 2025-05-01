"""
Tests for Solana service
"""
import unittest
from unittest.mock import patch, MagicMock
from app.services.solana import get_solana_balance


class TestSolanaService(unittest.TestCase):
    """Tests for the Solana blockchain service"""
    
    @patch('app.services.solana.requests.post')
    def test_get_solana_balance_success(self, mock_post):
        """Test successful balance retrieval"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {
                "context": {"slot": 123456789},
                "value": 123000000000  # 123 SOL in lamports
            },
            "id": 1
        }
        mock_post.return_value = mock_response
        
        # Call the function
        result = get_solana_balance("test_address")
        
        # Assertions
        self.assertEqual(result.status, "success")
        self.assertEqual(result.address, "test_address")
        self.assertEqual(result.balance_lamports, 123000000000)
        self.assertEqual(result.balance_sol, 123.0)
    
    @patch('app.services.solana.requests.post')
    def test_get_solana_balance_error(self, mock_post):
        """Test error handling in balance retrieval"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32602,
                "message": "Invalid param: Invalid"
            },
            "id": 1
        }
        mock_post.return_value = mock_response
        
        # Call the function
        result = get_solana_balance("invalid_address")
        
        # Assertions
        self.assertEqual(result.status, "error")
        self.assertTrue("RPC error" in result.message)


if __name__ == "__main__":
    unittest.main() 