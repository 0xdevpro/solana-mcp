# getBlock

Get information about a confirmed block by slot number.

## Description

This tool queries the Solana blockchain via RPC to retrieve detailed information about a block at the specified slot, including transactions and their statuses.

Use 'accounts' for transaction_details to get a faster response with account balance changes.
Set rewards to False if you don't need validator rewards information.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| slot | integer | Yes | The slot of the block to query |
| encoding | string | No | Encoding format for transaction data (json, jsonParsed, base58, base64). Default: "json" |
| transaction_details | string | No | Level of transaction detail to return (full, accounts, signatures, none). Default: "full" |
| rewards | boolean | No | Whether to include rewards in the response. Default: true |
| max_supported_transaction_version | integer | No | Filter for max transaction version |

## Usage

```python
# Basic usage
response = get_block(slot=12345678)

# With custom parameters
response = get_block(
    slot=12345678,
    encoding="jsonParsed",
    transaction_details="accounts",
    rewards=False
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| blockhash | string | The blockhash of this block |
| parentSlot | integer | The slot index of this block's parent |
| previousBlockhash | string | The blockhash of this block's parent |
| blockHeight | integer | The block height of this block |
| blockTime | integer | Estimated production time of this block, as Unix timestamp |
| transactions | array | Array of transaction objects (if requested) |
| rewards | array | Array of reward objects (if requested) |
| message | string | Error message if status is "error" or message about block not found |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "blockhash": "4oC8xRVnjZyBUGB1qrUbCU9FTRbJQn8rxWLQQBTNywdf",
  "parentSlot": 12345677,
  "previousBlockhash": "6H9JtWdP7SVrC7kmjrRfqRTWEj6Gy1xSF8qfq1rKXS6o",
  "blockHeight": 9876543,
  "blockTime": 1632155606,
  "transactions": [
    {
      "meta": {
        "err": null,
        "fee": 5000,
        "postBalances": [499995000, 15000000],
        "preBalances": [500000000, 10000000],
        "status": { "Ok": null }
      },
      "transaction": {
        "message": {
          "accountKeys": ["sender", "receiver"],
          "header": { /* header data */ },
          "instructions": [/* array of instructions */],
          "recentBlockhash": "previous-blockhash"
        },
        "signatures": ["sig1", "sig2"]
      }
    }
  ],
  "rewards": [
    {
      "pubkey": "validator-pubkey",
      "lamports": 1234,
      "postBalance": 9999999,
      "rewardType": "fee",
      "commission": 10
    }
  ]
}
```

### Block Not Found
```json
{
  "status": "success",
  "message": "Block not found or not confirmed"
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get block: Invalid parameter: Slot 999999999999 is too large",
  "error": {
    "code": -32602,
    "message": "Invalid parameter: Slot 999999999999 is too large"
  }
}
```

## Related Tools

- [get_blocks](get_blocks.md)
- [get_blocks_with_limit](get_blocks_with_limit.md)
- [get_block_height](get_block_height.md)
- [get_block_time](get_block_time.md)
- [get_block_commitment](get_block_commitment.md) 