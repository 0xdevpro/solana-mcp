# getMaxRetransmitSlot

Get the max slot that has been retransmitted by the Solana node.

## Description

This tool queries the Solana blockchain via RPC to retrieve the maximum slot that has been retransmitted or replayed by the node. This is primarily useful for validators and node operators to monitor the state of their node.

## Parameters

None

## Usage

```python
response = get_max_retransmit_slot()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| maxRetransmitSlot | integer | The maximum slot that has been retransmitted |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "maxRetransmitSlot": 123456789
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get max retransmit slot: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getMaxShredInsertSlot](getMaxShredInsertSlot.md)
- [getSlot](getSlot.md)
- [getHighestSnapshotSlot](getHighestSnapshotSlot.md) 