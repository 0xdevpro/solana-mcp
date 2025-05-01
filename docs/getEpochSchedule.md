# getEpochSchedule

Get epoch schedule information from the Solana cluster.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about the epoch schedule, including the number of slots in each epoch and other schedule-related parameters.

## Parameters

None

## Usage

```python
response = get_epoch_schedule()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| schedule | object | Epoch schedule information |
| schedule.slotsPerEpoch | integer | The number of slots in an epoch |
| schedule.leaderScheduleSlotOffset | integer | The number of slots before the beginning of an epoch to calculate a leader schedule for that epoch |
| schedule.warmup | boolean | Whether this epoch schedule uses a warmup rate during the first several epochs |
| schedule.firstNormalEpoch | integer | The first epoch with the full number of slotsPerEpoch |
| schedule.firstNormalSlot | integer | The first slot of the first normal epoch |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "schedule": {
    "slotsPerEpoch": 432000,
    "leaderScheduleSlotOffset": 432000,
    "warmup": true,
    "firstNormalEpoch": 14,
    "firstNormalSlot": 590832
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get epoch schedule: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getEpochInfo](getEpochInfo.md)
- [getLeaderSchedule](getLeaderSchedule.md)
- [getSlot](getSlot.md) 