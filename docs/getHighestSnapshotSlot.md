# getHighestSnapshotSlot

Get the highest snapshot slots available on the Solana node.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about the highest snapshot slots available on the node. Snapshots are used for fast startup of validators and for creating new validator nodes.

Returns information about both full and incremental snapshots.

## Parameters

None

## Usage

```python
response = get_highest_snapshot_slot()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| snapshotSlots | object | Information about the highest snapshot slots |
| snapshotSlots.full | integer | The highest full snapshot slot, or null if no snapshots are available |
| snapshotSlots.incremental | integer | The highest incremental snapshot slot based on full, or null if no incremental snapshots are available |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success (Both Full and Incremental Snapshots)
```json
{
  "status": "success",
  "snapshotSlots": {
    "full": 160000000,
    "incremental": 160123456
  }
}
```

### Success (Only Full Snapshot)
```json
{
  "status": "success",
  "snapshotSlots": {
    "full": 160000000,
    "incremental": null
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get highest snapshot slot: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getSlot](getSlot.md)
- [getBlocks](getBlocks.md)
- [getBlockHeight](getBlockHeight.md) 