# getGenesisHash

Get the genesis hash of the Solana cluster.

## Description

This tool queries the Solana blockchain via RPC to retrieve the genesis hash, which is a unique identifier for the blockchain network. Different Solana clusters (mainnet, testnet, devnet) have different genesis hashes.

This can be useful for verifying that you are connected to the expected network.

## Parameters

None

## Usage

```python
response = get_genesis_hash()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| genesisHash | string | The genesis hash as a base-58 encoded string |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "genesisHash": "5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d"
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get genesis hash: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getIdentity](getIdentity.md)
- [getHealth](getHealth.md)
- [getClusterNodes](getClusterNodes.md) 