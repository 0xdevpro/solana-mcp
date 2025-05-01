# get_solana_balance

Get the SOL balance for a Solana wallet address.

## Description

This tool queries the Solana blockchain via RPC to retrieve the current balance of the specified wallet address.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| address | string | Yes | The Solana wallet address to check |

## Usage

```python
response = get_solana_balance(address="YOUR_SOLANA_ADDRESS")
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| address | string | The queried Solana wallet address |
| balance_lamports | integer | Balance in lamports (the smallest unit of SOL) |
| balance_sol | float | Balance in SOL (1 SOL = 1,000,000,000 lamports) |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "address": "YOUR_SOLANA_ADDRESS",
  "balance_lamports": 1000000000,
  "balance_sol": 1.0
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get balance: Invalid address format",
  "error": {
    "code": -32602,
    "message": "Invalid param: WrongSize"
  }
}
```

## Related Tools

- [get_account_info](get_account_info.md)
- [get_largest_accounts](get_largest_accounts.md) 