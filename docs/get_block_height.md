# getBlockHeight

Get the current block height of the Solana node.

## Description

This tool queries the Solana blockchain via RPC to retrieve the current block height of the connected Solana node according to the specified commitment level.

Commitment level determines the confirmation status of blocks:
- 'processed': The node has received and processed the block (fastest, least certain)
- 'confirmed': The block has received a supermajority of votes
- 'finalized': The block has been confirmed as final and won't be rolled back (slowest, most certain)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_block_height()

# With commitment level
response = get_block_height(commitment="finalized")
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| blockHeight | integer | The current block height |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "blockHeight": 143042878
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get block height: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [get_block](get_block.md)
- [get_block_commitment](get_block_commitment.md)
- [get_blocks](get_blocks.md)
- [get_latest_blockhash](get_latest_blockhash.md) 