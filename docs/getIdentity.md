# getIdentity

Get the identity public key of the current Solana node.

## Description

This tool queries the Solana blockchain via RPC to retrieve the identity public key of the node you are connected to. This is useful for verifying which validator you are communicating with.

## Parameters

None

## Usage

```python
response = get_identity()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| identity | object | Node identity information |
| identity.identity | string | Node identity public key as a base-58 encoded string |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "identity": {
    "identity": "9gZbPtbtHrs6C4dn9ULy9NQQrR7VkzXYgbxD1CK3pHpR"
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get identity: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getHealth](getHealth.md)
- [getClusterNodes](getClusterNodes.md)
- [getGenesisHash](getGenesisHash.md) 