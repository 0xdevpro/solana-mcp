# getMaxShredInsertSlot

Get the highest slot where shreds have been inserted by the Solana node.

## Description

This tool queries the Solana blockchain via RPC to retrieve the maximum slot at which shreds have been inserted by the node. Shreds are pieces of blocks that are propagated throughout the network.

This is primarily useful for validators and node operators to monitor data handling on their nodes.

## Parameters

None

## Usage

```python
response = get_max_shred_insert_slot()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| maxShredInsertSlot | integer | The highest slot where shreds have been inserted |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "maxShredInsertSlot": 123456789
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get max shred insert slot: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getMaxRetransmitSlot](getMaxRetransmitSlot.md)
- [getSlot](getSlot.md)
- [getHighestSnapshotSlot](getHighestSnapshotSlot.md) 