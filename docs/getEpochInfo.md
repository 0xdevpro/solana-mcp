# getEpochInfo

Get information about the current epoch.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about the current epoch, including the current slot, block height, and slots in the epoch.

You can specify the commitment level to determine the confirmation status of the data.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_epoch_info()

# With commitment level
response = get_epoch_info(commitment="finalized")
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| info | object | Epoch information |
| info.absoluteSlot | integer | The current slot |
| info.blockHeight | integer | The current block height |
| info.epoch | integer | The current epoch |
| info.slotIndex | integer | The current slot relative to the start of the current epoch |
| info.slotsInEpoch | integer | The number of slots in this epoch |
| info.transactionCount | integer | Total transaction count since genesis (if available) |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "info": {
    "absoluteSlot": 160329661,
    "blockHeight": 141479233,
    "epoch": 371,
    "slotIndex": 334661,
    "slotsInEpoch": 432000,
    "transactionCount": 126584541061
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get epoch info: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getEpochSchedule](getEpochSchedule.md)
- [getBlockHeight](getBlockHeight.md)
- [getSlot](getSlot.md)
- [getSlotLeader](getSlotLeader.md) 