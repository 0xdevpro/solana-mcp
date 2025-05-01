# getLatestBlockhash

Get the latest blockhash from the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve the latest blockhash, which is necessary for creating and submitting transactions. Each transaction requires a recent blockhash to be considered valid.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_latest_blockhash()

# With commitment level
response = get_latest_blockhash(commitment="finalized")
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| value | object | Latest blockhash information |
| value.blockhash | string | The blockhash as base-58 encoded string |
| value.lastValidBlockHeight | integer | Last valid block height for this blockhash |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "value": {
    "blockhash": "EkSnNWid2cvwEVnVx9aBqawnmiCNiDgp3gUdkDPTKN1N",
    "lastValidBlockHeight": 143042878
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get latest blockhash: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [get_block](get_block.md)
- [get_block_height](get_block_height.md)
- [get_fee_for_message](get_fee_for_message.md) 