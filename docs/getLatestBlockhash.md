# getLatestBlockhash

Get the latest blockhash from the Solana cluster.

## Description

This tool queries the Solana blockchain via RPC to retrieve the latest blockhash along with the last valid block height.

Blockhashes are used for transaction uniqueness and to prevent replay attacks. Each transaction must include a recent blockhash, and this blockhash is only valid until a certain block height.

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
| value | object | Object containing blockhash information |
| value.blockhash | string | The latest blockhash (base-58 encoded) |
| value.lastValidBlockHeight | integer | Last block height at which the blockhash will be valid |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "value": {
    "blockhash": "Eit7RCyhUixAe2hGBS8oqnw59QK3kgMMjfLME5bm9wRn",
    "lastValidBlockHeight": 150795674
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

- [getFeeForMessage](getFeeForMessage.md)
- [getBlock](getBlock.md)
- [getBlockHeight](getBlockHeight.md) 