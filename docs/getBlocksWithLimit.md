# getBlocksWithLimit

Get a list of confirmed blocks starting at a slot with a limit.

## Description

This tool queries the Solana blockchain via RPC to retrieve a list of confirmed blocks starting at the specified slot, up to the specified limit.

Note that not every slot produces a block, so there may be gaps in the sequence of block numbers returned.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start_slot | integer | Yes | Start slot (inclusive) |
| limit | integer | Yes | Maximum number of blocks to return (must be no more than 500,000) |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_blocks_with_limit(start_slot=12345678, limit=100)

# With commitment level
response = get_blocks_with_limit(
    start_slot=12345678,
    limit=100,
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| blocks | array | List of block slot numbers |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "blocks": [12345678, 12345680, 12345681, 12345683, 12345684, 12345686, 12345687]
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get blocks with limit: Limit exceeds max allowed",
  "error": {
    "code": -32602,
    "message": "Limit exceeds max allowed"
  }
}
```

## Related Tools

- [getBlocks](getBlocks.md)
- [getBlock](getBlock.md)
- [getBlockHeight](getBlockHeight.md)
- [getFirstAvailableBlock](getFirstAvailableBlock.md) 