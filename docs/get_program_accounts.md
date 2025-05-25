# getProgramAccounts

Get all accounts owned by a specific Solana program.

## Description

This tool queries the Solana blockchain via RPC to retrieve all accounts that are owned by the specified program. This is useful for finding token accounts, program data accounts, and other program-specific accounts. You can apply filters to narrow down results by account data size or specific byte patterns.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `program_id` | str | Yes | - | Program ID to query accounts for, as base-58 encoded string |
| `encoding` | str | No | "base58" | Encoding format for Account data (base58, base64, base64+zstd, jsonParsed) |
| `data_slice_offset` | int | No | None | Byte offset to start reading account data (only for base58, base64, or base64+zstd encodings) |
| `data_slice_length` | int | No | None | Number of bytes to return (only for base58, base64, or base64+zstd encodings) |
| `filters` | List[Dict] | No | None | Optional filters to apply to accounts (memcmp or dataSize filters) |
| `with_context` | bool | No | False | Whether to wrap the result in an RpcResponse JSON object |
| `commitment` | str | No | None | The level of commitment (processed, confirmed, finalized) |

## Filter Types

### dataSize Filter
Filter accounts by data size:
```python
filters = [{"dataSize": 165}]  # Only accounts with exactly 165 bytes of data
```

### memcmp Filter
Filter accounts by comparing bytes at specific offsets:
```python
filters = [
    {
        "memcmp": {
            "offset": 0,
            "bytes": "3Mc6vR"  # base58 encoded bytes to match
        }
    }
]
```

## Usage Examples

### Basic Usage
```python
# Get all accounts owned by the Token program
program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
result = get_program_accounts(program_id)
```

### With JSON Parsed Encoding
```python
# Get token accounts with parsed data
program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
result = get_program_accounts(program_id, encoding="jsonParsed")
```

### With Data Size Filter
```python
# Get only token accounts (which have 165 bytes of data)
program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
filters = [{"dataSize": 165}]
result = get_program_accounts(program_id, filters=filters)
```

### With Memory Compare Filter
```python
# Get token accounts for a specific mint
program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
mint_address = "So11111111111111111111111111111111111111112"  # Wrapped SOL
filters = [
    {"dataSize": 165},
    {
        "memcmp": {
            "offset": 0,
            "bytes": mint_address
        }
    }
]
result = get_program_accounts(program_id, filters=filters)
```

### With Context
```python
# Get accounts with RPC context information
program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
result = get_program_accounts(program_id, with_context=True)
```

## Return Values

The tool returns a response object containing:

- **status**: "success" or "error"
- **accounts**: List of program account objects
  - **pubkey**: Account public key as base-58 encoded string
  - **account**: Account data object
    - **data**: Account data in the specified encoding format
    - **executable**: Boolean indicating if account contains a program
    - **lamports**: Number of lamports assigned to the account
    - **owner**: Base-58 encoded Pubkey of the program that owns this account
    - **rentEpoch**: The epoch at which this account will next owe rent
    - **space**: The data size of the account
- **context**: RPC response context (only if with_context=True)
- **message**: Error message (if status is "error")
- **error**: Detailed error information (if status is "error")

## Example JSON Response

```json
{
  "status": "success",
  "accounts": [
    {
      "pubkey": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
      "account": {
        "data": ["dGVzdCBkYXRh", "base64"],
        "executable": false,
        "lamports": 2039280,
        "owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
        "rentEpoch": 361,
        "space": 165
      }
    },
    {
      "pubkey": "C2jDL4pcwpE2pP5EryTGn842JJUJTcurPGZUAFK8sUDB",
      "account": {
        "data": ["dGVzdCBkYXRhMg==", "base64"],
        "executable": false,
        "lamports": 2039280,
        "owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
        "rentEpoch": 361,
        "space": 165
      }
    }
  ]
}
```

## Common Program IDs

Here are some commonly queried program IDs:

- **Token Program**: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
- **Token 2022 Program**: `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
- **Associated Token Program**: `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
- **Metaplex Token Metadata**: `metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s`
- **System Program**: `11111111111111111111111111111111`

## Performance Considerations

- Can return large amounts of data depending on the program
- Use filters to reduce response size and improve performance
- Consider using data slicing for accounts with large data
- Results are limited to prevent overwhelming responses
- Use commitment levels appropriately for your use case

## Error Handling

- Returns error status if RPC request fails
- Invalid program ID will cause the request to fail
- Large result sets may be truncated by RPC limits
- Some RPC providers may have additional limits on this method

## Related Tools

- [get_account_info](get_account_info.md) - Get information for a single account
- [get_multiple_accounts](get_multiple_accounts.md) - Get information for multiple accounts at once
- [get_largest_accounts](get_largest_accounts.md) - Get the largest accounts on the network 