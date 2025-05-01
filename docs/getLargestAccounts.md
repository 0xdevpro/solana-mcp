# getLargestAccounts

Get the largest accounts on the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve a list of the largest accounts by balance. You can optionally filter to show only circulating or non-circulating accounts.

This is useful for analyzing wealth distribution on the Solana network.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| filter_opt | string | No | Filter by account type: "circulating" or "nonCirculating" |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Get all largest accounts
response = get_largest_accounts()

# Get only circulating accounts
response = get_largest_accounts(filter_opt="circulating")

# Get only non-circulating accounts with commitment level
response = get_largest_accounts(
    filter_opt="nonCirculating",
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| accounts | array | Array of account objects |
| accounts[].address | string | Account address (base-58 encoded) |
| accounts[].lamports | integer | Account balance in lamports |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "accounts": [
    {
      "address": "83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri",
      "lamports": 999999999999999
    },
    {
      "address": "7vYe2KRUL2sbqSqbCn4UMoZnxy6vHqgQxHyXVbd3WBZe",
      "lamports": 800000000000000
    },
    {
      "address": "CP1co2QMMoDPbsmV7PGcUTBFN1LCpShKQZhDnXnLoRsk",
      "lamports": 700000000000000
    },
    {
      "address": "6LKEobZYKcweSXfunfzRXSzfLRPTu6fZiS9GcXgNvSmC",
      "lamports": 600000000000000
    },
    {
      "address": "9huDUZfxoJ7wGMTffUE7vh1xePqef7gyrLJu9NApncqA",
      "lamports": 500000000000000
    }
  ]
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get largest accounts: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getBalance](getBalance.md)
- [getAccountInfo](getAccountInfo.md)
- [getInflationRate](getInflationRate.md) 