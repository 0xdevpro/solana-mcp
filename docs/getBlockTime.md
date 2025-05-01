# getBlockTime

Get the estimated production time of a block.

## Description

This tool queries the Solana blockchain via RPC to retrieve the estimated production time of a block at the specified slot. The time is returned as a Unix timestamp (seconds since the Unix epoch).

Returns null if the block is not available or not yet confirmed.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| slot | integer | Yes | The slot of the block to get the time for |

## Usage

```python
response = get_block_time(slot=12345678)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| blockTime | integer | The estimated production time as a Unix timestamp (seconds since the Unix epoch) |
| message | string | Error message if status is "error" or message if block is not found |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "blockTime": 1632155606
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
  "message": "Failed to get block time: Invalid parameter: Slot 999999999999 is too large",
  "error": {
    "code": -32602,
    "message": "Invalid parameter: Slot 999999999999 is too large"
  }
}
```

## Related Tools

- [getBlock](getBlock.md)
- [getBlocks](getBlocks.md)
- [getBlockHeight](getBlockHeight.md)
- [getFirstAvailableBlock](getFirstAvailableBlock.md) 