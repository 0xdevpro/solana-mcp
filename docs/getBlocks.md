# getBlocks

Get a list of confirmed blocks between two slots.

## Description

This tool queries the Solana blockchain via RPC to retrieve a list of confirmed blocks between the specified start and end slots.

Note that not every slot produces a block, so there may be gaps in the sequence of block numbers returned.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start_slot | integer | Yes | Start slot (inclusive) |
| end_slot | integer | No | End slot (inclusive), if not provided, latest block will be used |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_blocks(start_slot=12345678)

# With an end slot
response = get_blocks(start_slot=12345678, end_slot=12345778)

# With commitment level
response = get_blocks(
    start_slot=12345678, 
    end_slot=12345778,
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
  "message": "Failed to get blocks: Invalid parameter: Slot 999999999999 is too large",
  "error": {
    "code": -32602,
    "message": "Invalid parameter: Slot 999999999999 is too large"
  }
}
```

## Related Tools

- [getBlock](getBlock.md)
- [getBlocksWithLimit](getBlocksWithLimit.md)
- [getBlockHeight](getBlockHeight.md)
- [getFirstAvailableBlock](getFirstAvailableBlock.md) 