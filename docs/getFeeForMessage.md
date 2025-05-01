# getFeeForMessage

Get the fee in lamports for a message.

## Description

This tool queries the Solana blockchain via RPC to retrieve the fee that would be charged for a transaction containing the given message.

The message must be base-64 encoded, and should be properly formatted according to the Solana transaction message format (typically created by a Solana SDK).

Returns null if the blockhash in the message has expired or is invalid.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| message | string | Yes | Base-64 encoded message to get the fee for |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_fee_for_message(message="YOUR_BASE64_ENCODED_MESSAGE")

# With commitment level
response = get_fee_for_message(
    message="YOUR_BASE64_ENCODED_MESSAGE",
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| fee | integer | Fee in lamports for the message |
| message | string | Error message if status is "error" or message about expired blockhash |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "fee": 5000
}
```

### Expired Blockhash
```json
{
  "status": "success",
  "message": "Blockhash in the message has expired or is invalid"
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get fee for message: Invalid base64 encoding",
  "error": {
    "code": -32602,
    "message": "Invalid param: not base64 encoded"
  }
}
```

## Related Tools

- [getLatestBlockhash](getLatestBlockhash.md)
- [getTransaction](getTransaction.md)
- [getMinimumBalanceForRentExemption](getMinimumBalanceForRentExemption.md) 