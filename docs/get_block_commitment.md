# getBlockCommitment

Get commitment (confirmation status) information for a block.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about how much stake has voted for a block at the specified slot.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| slot | integer | Yes | The slot to query commitment information for |

## Usage

```python
response = get_block_commitment(slot=12345678)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| commitment | array | An array of integers listing the amount of cluster stake in lamports that has voted on the block at each depth from 0 to 32 |
| totalStake | integer | Total active stake in lamports |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "commitment": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 499999990000],
  "totalStake": 499999990000
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get block commitment: Invalid parameter: Slot 999999999999 is too large",
  "error": {
    "code": -32602,
    "message": "Invalid parameter: Slot 999999999999 is too large"
  }
}
```

## Related Tools

- [get_block](get_block.md)
- [get_block_height](get_block_height.md)
- [get_blocks](get_blocks.md) 