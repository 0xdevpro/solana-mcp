# getRecentPrioritizationFees

Get recent prioritization fees from the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve recent prioritization fees that have been paid to prioritize transactions in the network. Prioritization fees help transactions get processed faster during network congestion. If addresses are provided, returns fees for transactions that write-lock those accounts.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `addresses` | List[str] | No | None | Optional list of account addresses to get prioritization fees for |

## Usage Examples

### Basic Usage
```python
# Get recent prioritization fees for all transactions
result = get_recent_prioritization_fees()
```

### For Specific Accounts
```python
# Get prioritization fees for specific accounts
addresses = [
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
]
result = get_recent_prioritization_fees(addresses)
```

### For Token Operations
```python
# Get fees for token-related transactions
token_program = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
result = get_recent_prioritization_fees([token_program])
```

## Return Values

The tool returns a response object containing:

- **status**: "success" or "error"
- **fees**: List of prioritization fee objects
  - **slot**: Slot in which the fee was observed
  - **prioritizationFee**: The per-compute-unit fee paid by at least one successfully landed transaction, specified in increments of micro-lamports (0.000001 lamports)
- **message**: Error message (if status is "error")
- **error**: Detailed error information (if status is "error")

## Example JSON Response

```json
{
  "status": "success",
  "fees": [
    {
      "slot": 123456789,
      "prioritizationFee": 1000
    },
    {
      "slot": 123456788,
      "prioritizationFee": 1200
    },
    {
      "slot": 123456787,
      "prioritizationFee": 800
    },
    {
      "slot": 123456786,
      "prioritizationFee": 1500
    }
  ]
}
```

## Understanding Prioritization Fees

### Fee Units
- Fees are returned in **micro-lamports per compute unit**
- 1 micro-lamport = 0.000001 lamports
- 1 lamport = 0.000000001 SOL

### Fee Calculation
To calculate the total prioritization fee for a transaction:
```python
total_fee = prioritization_fee_per_cu * compute_units_used
```

Example:
```python
# If prioritization fee is 1000 micro-lamports per CU
# and transaction uses 200,000 compute units
prioritization_fee_per_cu = 1000  # micro-lamports
compute_units = 200000
total_fee_microlamports = prioritization_fee_per_cu * compute_units
total_fee_lamports = total_fee_microlamports / 1_000_000
print(f"Total prioritization fee: {total_fee_lamports} lamports")
```

## Use Cases

### Fee Estimation for Transactions
Use recent fees to estimate appropriate prioritization fees:
```python
def get_suggested_priority_fee():
    recent_fees = get_recent_prioritization_fees()
    if recent_fees["status"] == "success" and recent_fees["fees"]:
        fees = [fee["prioritizationFee"] for fee in recent_fees["fees"]]
        
        # Calculate percentiles for different priority levels
        fees.sort()
        
        # Conservative (25th percentile)
        conservative = fees[len(fees) // 4]
        
        # Moderate (50th percentile - median)
        moderate = fees[len(fees) // 2]
        
        # Aggressive (75th percentile)
        aggressive = fees[3 * len(fees) // 4]
        
        return {
            "conservative": conservative,
            "moderate": moderate,
            "aggressive": aggressive
        }
    return None
```

### Account-Specific Fee Analysis
Analyze fees for specific programs or accounts:
```python
# Check fees for token transfers
token_program = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
token_fees = get_recent_prioritization_fees([token_program])

if token_fees["status"] == "success":
    avg_fee = sum(fee["prioritizationFee"] for fee in token_fees["fees"]) / len(token_fees["fees"])
    print(f"Average prioritization fee for token operations: {avg_fee} micro-lamports/CU")
```

### Dynamic Fee Adjustment
Adjust fees based on network conditions:
```python
def get_dynamic_priority_fee(urgency="normal"):
    recent_fees = get_recent_prioritization_fees()
    
    if recent_fees["status"] != "success" or not recent_fees["fees"]:
        return 1000  # Default fallback
    
    fees = [fee["prioritizationFee"] for fee in recent_fees["fees"]]
    avg_fee = sum(fees) / len(fees)
    
    multipliers = {
        "low": 0.5,
        "normal": 1.0,
        "high": 1.5,
        "urgent": 2.0
    }
    
    return int(avg_fee * multipliers.get(urgency, 1.0))
```

## Fee Trends and Analysis

### Monitoring Fee Trends
```python
def analyze_fee_trends():
    fees_data = get_recent_prioritization_fees()
    
    if fees_data["status"] == "success":
        fees = fees_data["fees"]
        
        # Sort by slot (most recent first)
        fees.sort(key=lambda x: x["slot"], reverse=True)
        
        if len(fees) >= 10:
            recent_10 = fees[:10]
            older_10 = fees[-10:]
            
            recent_avg = sum(f["prioritizationFee"] for f in recent_10) / 10
            older_avg = sum(f["prioritizationFee"] for f in older_10) / 10
            
            trend = (recent_avg - older_avg) / older_avg * 100
            
            print(f"Recent average fee: {recent_avg:.2f} micro-lamports/CU")
            print(f"Trend: {trend:+.1f}% compared to earlier samples")
```

## Best Practices

### Setting Prioritization Fees
1. **Check Recent Fees**: Always check recent fees before setting your own
2. **Consider Urgency**: Higher fees for time-sensitive transactions
3. **Account for Network Conditions**: Increase fees during congestion
4. **Monitor Success Rates**: Track if your chosen fees result in successful inclusion

### Fee Optimization
```python
def optimize_priority_fee(target_success_rate=0.9):
    """
    Suggest a priority fee based on recent data and target success rate
    """
    recent_fees = get_recent_prioritization_fees()
    
    if recent_fees["status"] == "success" and recent_fees["fees"]:
        fees = sorted(fee["prioritizationFee"] for fee in recent_fees["fees"])
        
        # Use percentile based on target success rate
        index = int(len(fees) * target_success_rate)
        suggested_fee = fees[min(index, len(fees) - 1)]
        
        return suggested_fee
    
    return 1000  # Fallback
```

## Data Characteristics

- **Sample Size**: Returns recent fee observations (typically 150 slots)
- **Update Frequency**: Updated with each new slot
- **Fee Resolution**: Measured in micro-lamports per compute unit
- **Account Filtering**: When addresses provided, only fees from transactions affecting those accounts

## Limitations

- Fee data reflects past transactions, not current mempool conditions
- High variance in fees during network congestion
- Account-specific filtering may return fewer samples
- Fees can change rapidly during network events

## Error Handling

- Returns error status if RPC request fails
- Empty fee list may indicate no recent transactions with prioritization fees
- Invalid addresses will cause the entire request to fail

## Related Tools

- [get_fee_for_message](get_fee_for_message.md) - Get base fee for a specific message
- [get_recent_performance_samples](get_recent_performance_samples.md) - Get network performance metrics
- [get_health](get_health.md) - Check network health status
- [get_latest_blockhash](get_latest_blockhash.md) - Get the latest blockhash for transactions 