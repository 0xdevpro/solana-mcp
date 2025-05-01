# getFirstAvailableBlock

Get the first available block in the Solana ledger.

## Description

This tool queries the Solana blockchain via RPC to retrieve the slot number of the first available block in the ledger. This can be useful for determining the earliest point from which historical data can be retrieved.

## Parameters

None

## Usage

```python
response = get_first_available_block()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| firstAvailableBlock | integer | The slot number of the first available block |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "firstAvailableBlock": 1
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get first available block: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getBlocks](getBlocks.md)
- [getBlocksWithLimit](getBlocksWithLimit.md)
- [getBlock](getBlock.md) 