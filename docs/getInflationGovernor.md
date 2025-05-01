# getInflationGovernor

Get the inflation governor parameters from the Solana cluster.

## Description

This tool queries the Solana blockchain via RPC to retrieve the inflation governor parameters, which control how the inflation rate changes over time.

These parameters include the initial inflation rate, terminal inflation rate, rate of inflation reduction (taper), foundation inflation rate, and foundation term.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage
response = get_inflation_governor()

# With commitment level
response = get_inflation_governor(commitment="finalized")
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| inflationGovernor | object | The inflation governor parameters |
| inflationGovernor.initial | number | Initial inflation rate (percentage) |
| inflationGovernor.terminal | number | Terminal inflation rate (percentage) |
| inflationGovernor.taper | number | Rate of inflation reduction (percentage) |
| inflationGovernor.foundation | number | Foundation inflation rate (percentage) |
| inflationGovernor.foundationTerm | number | Foundation term in years |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success
```json
{
  "status": "success",
  "inflationGovernor": {
    "initial": 8.0,
    "terminal": 1.5,
    "taper": 0.15,
    "foundation": 3.0,
    "foundationTerm": 7.0
  }
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get inflation governor: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getInflationRate](getInflationRate.md)
- [getInflationReward](getInflationReward.md)
- [getEpochInfo](getEpochInfo.md) 