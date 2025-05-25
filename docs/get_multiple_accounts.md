# getMultipleAccounts

Get information for multiple Solana accounts at once.

## Description

This tool queries the Solana blockchain via RPC to retrieve detailed account information for multiple accounts in a single request, which is more efficient than multiple individual calls. This is particularly useful when you need to fetch information for several accounts simultaneously.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `addresses` | List[str] | Yes | - | List of account addresses to query (max 100), as base-58 encoded strings |
| `encoding` | str | No | "base58" | Encoding format for Account data (base58, base64, base64+zstd, jsonParsed) |
| `data_slice_offset` | int | No | None | Byte offset to start reading account data (only for base58, base64, or base64+zstd encodings) |
| `data_slice_length` | int | No | None | Number of bytes to return (only for base58, base64, or base64+zstd encodings) |
| `commitment` | str | No | None | The level of commitment (processed, confirmed, finalized) |

## Usage Examples

### Basic Usage
```python
# Get information for multiple accounts
addresses = [
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "11111111111111111111111111111111",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
]
result = get_multiple_accounts(addresses)
```

### With JSON Parsed Encoding
```python
# Get multiple token accounts with parsed data
addresses = [
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
]
result = get_multiple_accounts(addresses, encoding="jsonParsed")
```

### With Data Slice
```python
# Get partial account data for multiple accounts
addresses = [
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "11111111111111111111111111111111"
]
result = get_multiple_accounts(
    addresses, 
    encoding="base64",
    data_slice_offset=0,
    data_slice_length=32
)
```

## Return Values

The tool returns a response object containing:

- **status**: "success" or "error"
- **value**: List of account information objects (or None if account not found)
  - **data**: Account data in the specified encoding format
  - **executable**: Boolean indicating if account contains a program
  - **lamports**: Number of lamports assigned to the account
  - **owner**: Base-58 encoded Pubkey of the program that owns this account
  - **rentEpoch**: The epoch at which this account will next owe rent
  - **space**: The data size of the account
- **context**: RPC response context with slot information
- **message**: Error message (if status is "error")
- **error**: Detailed error information (if status is "error")

## Example JSON Response

```json
{
  "status": "success",
  "value": [
    {
      "data": ["", "base58"],
      "executable": false,
      "lamports": 1000000000,
      "owner": "11111111111111111111111111111111",
      "rentEpoch": 18446744073709551615,
      "space": 0
    },
    null,
    {
      "data": ["AQAAAAEAAAACAAAAAwAAAAQAAAA=", "base64"],
      "executable": true,
      "lamports": 1169280,
      "owner": "BPFLoaderUpgradeab1e11111111111111111111111",
      "rentEpoch": 361,
      "space": 36
    }
  ],
  "context": {
    "slot": 123456789
  }
}
```

## Error Handling

- Returns error status if RPC request fails
- Individual accounts in the list can be null if the account doesn't exist
- Maximum of 100 addresses can be queried at once
- Invalid addresses will cause the entire request to fail

## Performance Notes

- More efficient than making multiple individual `getAccountInfo` calls
- Reduces network overhead when querying multiple accounts
- Useful for batch operations and portfolio management
- Consider using data slicing for large accounts to reduce response size

## Related Tools

- [get_account_info](get_account_info.md) - Get information for a single account
- [get_program_accounts](get_program_accounts.md) - Get all accounts owned by a program
- [get_largest_accounts](get_largest_accounts.md) - Get the largest accounts on the network 