# getInflationReward

Get inflation rewards for a list of Solana accounts.

## Description

This tool queries the Solana blockchain via RPC to retrieve inflation reward information for the specified accounts, typically used for validator and stake accounts.

For each address, returns information about rewards earned, including:
- Epoch in which the reward was earned
- Effective slot at which the reward was calculated
- Amount of the reward in lamports
- Post-reward balance of the account in lamports
- Commission of vote accounts (if applicable)

Returns null for addresses that are not found or did not receive rewards.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| addresses | array of strings | Yes | List of account addresses to query rewards for |
| epoch | integer | No | Epoch to query rewards for (defaults to previous epoch) |
| commitment | string | No | The level of commitment (processed, confirmed, finalized) |

## Usage

```python
# Basic usage with a single address
response = get_inflation_reward(addresses=["Your_Account_Address"])

# Multiple addresses for a specific epoch
response = get_inflation_reward(
    addresses=["Account_Address_1", "Account_Address_2"],
    epoch=150,
    commitment="finalized"
)
```

## Return Value

Returns a JSON object with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| status | string | "success" or "error" |
| rewards | array | Array of reward objects, one per address requested |
| rewards[].epoch | integer | Epoch for which the reward was earned |
| rewards[].effectiveSlot | integer | The slot at which the reward was calculated |
| rewards[].amount | integer | Amount of the reward in lamports |
| rewards[].postBalance | integer | Post-reward balance in lamports |
| rewards[].commission | integer | Vote account commission (if applicable) |
| message | string | Error message if status is "error" |
| error | object | Error details if status is "error" |

## Example Response

### Success (Rewards Found)
```json
{
  "status": "success",
  "rewards": [
    {
      "epoch": 250,
      "effectiveSlot": 108000000,
      "amount": 3500000,
      "postBalance": 75300000000,
      "commission": 10
    },
    {
      "epoch": 250,
      "effectiveSlot": 108000000,
      "amount": 2700000,
      "postBalance": 15400000000,
      "commission": null
    }
  ]
}
```

### Success (No Rewards)
```json
{
  "status": "success",
  "rewards": [null, null]
}
```

### Error
```json
{
  "status": "error",
  "message": "Failed to get inflation reward: Connection refused",
  "error": {
    "code": -32000,
    "message": "Connection refused"
  }
}
```

## Related Tools

- [getInflationGovernor](getInflationGovernor.md)
- [getInflationRate](getInflationRate.md)
- [getEpochInfo](getEpochInfo.md) 