# getInflationRate

Get the current inflation rate of the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve the current inflation rate, including the total inflation and how it's divided between validators and the Solana Foundation.

This is useful for understanding the current tokenomics of the Solana network.

## Parameters

None

## Usage

```python
response = get_inflation_rate()
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| inflationRate | object | The current inflation rates |
| inflationRate.total | number | Total inflation rate (percentage) |
| inflationRate.validator | number | Validator inflation rate (percentage) |
| inflationRate.foundation | number | Foundation inflation rate (percentage) |
| inflationRate.epoch | number | Epoch for which the rate is valid |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "inflationRate": {
    "total": 6.5,
    "validator": 5.5,
    "foundation": 1.0,
    "epoch": 341
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get inflation rate: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getInflationGovernor](getInflationGovernor.md)
- [getInflationReward](getInflationReward.md)
- [getEpochInfo](getEpochInfo.md) 