# getClusterNodes

Get information about the nodes in the Solana cluster.

## Description

This tool queries the Solana blockchain via RPC to retrieve information about the nodes in the cluster, including their public keys, gossip and RPC addresses, and software versions.

## Parameters

None

## Usage

```python
response = get_cluster_nodes()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| nodes | array | List of node information objects |
| nodes[].pubkey | string | Node public key (base-58 encoded) |
| nodes[].gossip | string | Gossip address (IP:port) or null if not advertised |
| nodes[].tpu | string | TPU address (IP:port) or null if not advertised |
| nodes[].rpc | string | RPC address (IP:port) or null if not advertised |
| nodes[].version | string | Software version or null if not advertised |
| nodes[].featureSet | integer | Feature set identifier or null if not advertised |
| nodes[].shredVersion | integer | Shred version or null if not advertised |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "nodes": [
    {
      "pubkey": "7FXJxGMJpQmG9RCn1Ngu7D8h94FpExuXQARJAujLYgFu",
      "gossip": "127.0.0.1:8001",
      "tpu": "127.0.0.1:8002",
      "rpc": "127.0.0.1:8003",
      "version": "1.14.10",
      "featureSet": 3090082321,
      "shredVersion": 30347
    },
    {
      "pubkey": "8FXJxGMJpQmG9RCn1Ngu7D8h94FpExuXQARJAujLYgFu",
      "gossip": "127.0.0.2:8001",
      "tpu": "127.0.0.2:8002",
      "rpc": "127.0.0.2:8003",
      "version": "1.14.10",
      "featureSet": 3090082321,
      "shredVersion": 30347
    }
  ]
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get cluster nodes: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getIdentity](getIdentity.md)
- [getHealth](getHealth.md)
- [getVoteAccounts](getVoteAccounts.md)
- [getBlockProduction](getBlockProduction.md) 