# getMinimumBalanceForRentExemption

Get the minimum balance required for rent exemption for a data size.

## Description

This tool queries the Solana blockchain via RPC to calculate the minimum lamports required for an account of the specified size to be rent exempt.

In Solana, accounts must either pay rent or maintain a minimum balance to be "rent exempt". Rent-exempt accounts do not need to pay rent and will not be purged from the network.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data_size | integer | Yes | Size of the account data in bytes |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_minimum_balance_for_rent_exemption(data_size=100)

# With commitment level
response = get_minimum_balance_for_rent_exemption(
    data_size=100,
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| lamports | integer | Minimum lamports required for rent exemption |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "lamports": 2039280
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get minimum balance for rent exemption: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getAccountInfo](getAccountInfo.md)
- [getBalance](getBalance.md)
- [getFeeForMessage](getFeeForMessage.md) 