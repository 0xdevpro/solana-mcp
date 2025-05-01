# getBlockProduction

Get recent block production information from the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about which validators have produced and skipped blocks (leader slots) in the given range of slots.

You can filter results to a specific validator identity, specify a range of slots, and choose the commitment level for confirmation status.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| identity | string | No | Only return results for this validator identity (base-58 encoded) |
| first_slot | integer | No | Start slot of the block production range (inclusive) |
| last_slot | integer | No | End slot of the block production range (inclusive) |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage (gets recent production info)
response = get_block_production()

# Filter by validator identity
response = get_block_production(identity="YOUR_VALIDATOR_PUBKEY")

# Specify a slot range
response = get_block_production(first_slot=12345678, last_slot=12345778)

# Combined parameters
response = get_block_production(
    identity="YOUR_VALIDATOR_PUBKEY",
    first_slot=12345678, 
    last_slot=12345778,
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| range | object | Information about the slot range |
| range.firstSlot | integer | First slot in the range (inclusive) |
| range.lastSlot | integer | Last slot in the range (inclusive) |
| byIdentity | object | Map of validator identities to their block production (object keys are base-58 encoded identities) |
| byIdentity.*.leader_slots | integer | Number of slots this validator was assigned as leader |
| byIdentity.*.blocks_produced | integer | Number of blocks the validator produced in this range |
| average | object | Average block production information |
| average.leader_slots | integer | Total leader slots in the range |
| average.blocks_produced | integer | Total blocks produced in the range |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "range": {
    "firstSlot": 12345678,
    "lastSlot": 12345778
  },
  "byIdentity": {
    "validator1Pubkey": {
      "leader_slots": 50,
      "blocks_produced": 48
    },
    "validator2Pubkey": {
      "leader_slots": 30,
      "blocks_produced": 25
    }
  },
  "average": {
    "leader_slots": 80,
    "blocks_produced": 73
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get block production: Invalid slot range",
  "error": {
    "code": -32602,
    "message": "Invalid slot range"
  }
}
```

## Related Tools

- [get_block](get_block.md)
- [get_leader_schedule](get_leader_schedule.md)
- [get_cluster_nodes](get_cluster_nodes.md) 