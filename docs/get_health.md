# getHealth

Check the health of the connected Solana node.

## Description

This tool queries the Solana blockchain via RPC to check if the node is healthy. This can be useful for monitoring the status of the node and ensuring that it is operational before sending transactions or queries.

## Parameters

None

## Usage

```python
response = get_health()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| healthy | boolean | Indicates if the node is healthy or not |
| message | string | Error message if status is "error" or node is not healthy |
| error | object | Error details if status is "error" |

## Example Response

### Healthy Node
```json
{
  "status": "success",
  "healthy": true
}
```

### Unhealthy Node
```json
{
  "status": "success",
  "healthy": false,
  "message": "Node is unhealthy: Validator exited. Restart required."
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get health: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [get_identity](get_identity.md)
- [get_cluster_nodes](get_cluster_nodes.md)
- [get_genesis_hash](get_genesis_hash.md) 