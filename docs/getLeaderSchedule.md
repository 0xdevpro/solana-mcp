# getLeaderSchedule

Get the leader schedule for the current or a specific epoch.

## Description

This tool queries the Solana blockchain via RPC to retrieve the leader schedule, which determines which validator is responsible for producing blocks at each slot.

You can query for the schedule at a specific slot, and optionally filter results to show only the slots for a particular validator identity. Without any parameters, it returns the leader schedule for the current epoch.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| slot | integer | No | Slot to get leader schedule for (defaults to current slot) |
| identity | string | No | Filter results for this validator identity (base-58 encoded) |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Get full leader schedule for current epoch
response = get_leader_schedule()

# Get schedule for a specific slot
response = get_leader_schedule(slot=123456789)

# Get schedule for a specific validator only
response = get_leader_schedule(identity="validator_identity_pubkey")

# Combining parameters
response = get_leader_schedule(
    slot=123456789,
    identity="validator_identity_pubkey",
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| schedule | object | Schedule as a map of validator identity to array of slots |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success (Full Schedule)
```json
{
  "status": "success",
  "schedule": {
    "9gZbPtbtHrs6C4dn9ULy9NQQrR7VkzXYgbxD1CK3pHpR": [
      0, 
      4, 
      8, 
      12
    ],
    "7vYe2KRUL2sbqSqbCn4UMoZnxy6vHqgQxHyXVbd3WBZe": [
      1, 
      5, 
      9, 
      13
    ],
    "83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri": [
      2, 
      6, 
      10, 
      14
    ],
    "6LKEobZYKcweSXfunfzRXSzfLRPTu6fZiS9GcXgNvSmC": [
      3, 
      7, 
      11, 
      15
    ]
  }
}
```

### Success (Filtered for Single Validator)
```json
{
  "status": "success",
  "schedule": {
    "9gZbPtbtHrs6C4dn9ULy9NQQrR7VkzXYgbxD1CK3pHpR": [
      0, 
      4, 
      8, 
      12
    ]
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get leader schedule: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getEpochInfo](getEpochInfo.md)
- [getClusterNodes](getClusterNodes.md)
- [getIdentity](getIdentity.md) 