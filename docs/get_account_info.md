# getAccountInfo

Get all information associated with a Solana account by its address.

## Description

This tool queries the Solana blockchain via RPC to retrieve detailed account information including balance, owner, executable status, and data in the specified encoding format.

For token accounts, program accounts, and other specialized account types, use 'jsonParsed' encoding to receive structured data.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| address | string | Yes | The Solana account address to query, as base-58 encoded string |
| encoding | string | No | Encoding format for Account data (base58, base64, base64+zstd, jsonParsed). Default: "base58" |
| data_slice_offset | integer | No | Byte offset to start reading account data (only for base58, base64, or base64+zstd encodings) |
| data_slice_length | integer | No | Number of bytes to return (only for base58, base64, or base64+zstd encodings) |

## Usage

```python
# Basic usage
response = get_account_info(address="YOUR_SOLANA_ACCOUNT_ADDRESS")

# With jsonParsed encoding (for token accounts, etc.)
response = get_account_info(
    address="YOUR_SOLANA_ACCOUNT_ADDRESS",
    encoding="jsonParsed"
)

# With data slice (for large accounts)
response = get_account_info(
    address="YOUR_SOLANA_ACCOUNT_ADDRESS",
    encoding="base64",
    data_slice_offset=0,
    data_slice_length=100
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| address | string | The queried Solana account address |
| value | object | Account information if found |
| value.data | array or object | Account data in the specified encoding format |
| value.executable | boolean | Whether the account contains a program and is strictly read-only |
| value.lamports | integer | Number of lamports assigned to this account |
| value.owner | string | Base-58 encoded Pubkey of the program this account has been assigned to |
| value.rentEpoch | integer | The epoch at which this account will next owe rent |
| value.space | integer | The data size of the account |
| message | string | Error message if status is "error" or message about account not found |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "address": "YOUR_SOLANA_ACCOUNT_ADDRESS",
  "value": {
    "data": ["encoded-data-depends-on-format", "base58"],
    "executable": false,
    "lamports": 1000000000,
    "owner": "11111111111111111111111111111111",
    "rentEpoch": 361,
    "space": 0
  }
}
```

### Account Not Found
```json
{
  "status": "success",
  "address": "YOUR_SOLANA_ACCOUNT_ADDRESS",
  "value": null,
  "message": "Account not found"
}
```

### Error
```json
{
  "status": "error",
  "address": "YOUR_SOLANA_ACCOUNT_ADDRESS",
  "message": "Failed to get account info: Invalid address format",
  "error": {
    "code": -32602,
    "message": "Invalid param: WrongSize"
  }
}
```

## Related Tools

- [get_solana_balance](get_solana_balance.md)
- [get_largest_accounts](get_largest_accounts.md)
- [get_minimum_balance_for_rent_exemption](get_minimum_balance_for_rent_exemption.md) 