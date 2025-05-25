# getRecentPerformanceSamples

Get recent performance samples from the Solana network.

## Description

This tool queries the Solana blockchain via RPC to retrieve recent performance metrics including transaction throughput and slot timing information. Performance samples provide insights into network health and transaction processing rates, which are useful for monitoring network conditions and performance analysis.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | int | No | None | Number of samples to return (max 720, default 720) |

## Usage Examples

### Basic Usage
```python
# Get recent performance samples (default 720 samples)
result = get_recent_performance_samples()
```

### With Custom Limit
```python
# Get last 100 performance samples
result = get_recent_performance_samples(limit=100)
```

### Get Latest Sample Only
```python
# Get only the most recent performance sample
result = get_recent_performance_samples(limit=1)
```

## Return Values

The tool returns a response object containing:

- **status**: "success" or "error"
- **samples**: List of performance sample objects
  - **slot**: Slot in which sample was taken
  - **numTransactions**: Number of transactions in sample
  - **numSlots**: Number of slots in sample
  - **samplePeriodSecs**: Number of seconds in a sample window
- **message**: Error message (if status is "error")
- **error**: Detailed error information (if status is "error")

## Example JSON Response

```json
{
  "status": "success",
  "samples": [
    {
      "slot": 123456789,
      "numTransactions": 1500,
      "numSlots": 60,
      "samplePeriodSecs": 60
    },
    {
      "slot": 123456729,
      "numTransactions": 1480,
      "numSlots": 60,
      "samplePeriodSecs": 60
    },
    {
      "slot": 123456669,
      "numTransactions": 1520,
      "numSlots": 60,
      "samplePeriodSecs": 60
    }
  ]
}
```

## Performance Metrics Explanation

### Transactions Per Second (TPS)
You can calculate TPS from the sample data:
```python
tps = sample["numTransactions"] / sample["samplePeriodSecs"]
```

### Slot Time
Average time per slot in the sample:
```python
avg_slot_time = sample["samplePeriodSecs"] / sample["numSlots"]
```

### Sample Analysis
```python
# Example analysis of performance samples
def analyze_performance(samples):
    for sample in samples:
        tps = sample["numTransactions"] / sample["samplePeriodSecs"]
        avg_slot_time = sample["samplePeriodSecs"] / sample["numSlots"]
        
        print(f"Slot: {sample['slot']}")
        print(f"TPS: {tps:.2f}")
        print(f"Average slot time: {avg_slot_time:.2f}s")
        print("---")
```

## Use Cases

### Network Health Monitoring
Monitor network performance over time to detect issues or degradation:
```python
# Get recent samples and check for performance drops
samples = get_recent_performance_samples(limit=10)
for sample in samples["samples"]:
    tps = sample["numTransactions"] / sample["samplePeriodSecs"]
    if tps < 1000:  # Alert if TPS drops below threshold
        print(f"Low TPS detected: {tps:.2f} at slot {sample['slot']}")
```

### Performance Trending
Analyze performance trends over time:
```python
# Get a larger sample for trend analysis
samples = get_recent_performance_samples(limit=200)
tps_values = []
for sample in samples["samples"]:
    tps = sample["numTransactions"] / sample["samplePeriodSecs"]
    tps_values.append(tps)

avg_tps = sum(tps_values) / len(tps_values)
print(f"Average TPS over {len(tps_values)} samples: {avg_tps:.2f}")
```

### Transaction Timing Optimization
Use performance data to optimize transaction timing:
```python
# Check current network performance before sending transactions
recent_sample = get_recent_performance_samples(limit=1)["samples"][0]
current_tps = recent_sample["numTransactions"] / recent_sample["samplePeriodSecs"]

if current_tps > 2000:
    print("Network performing well - good time to send transactions")
else:
    print("Network congested - consider waiting or increasing fees")
```

## Data Characteristics

- **Sample Period**: Typically 60 seconds per sample
- **Maximum Samples**: 720 (approximately 12 hours of data)
- **Update Frequency**: New samples are added approximately every minute
- **Data Retention**: Samples older than 720 periods are dropped

## Limitations

- Performance samples are estimates and may not reflect exact real-time conditions
- Sample periods may vary slightly based on network conditions
- Historical data is limited to the maximum sample count
- Performance can vary significantly during network upgrades or issues

## Error Handling

- Returns error status if RPC request fails
- Invalid limit values (> 720) may be adjusted by the RPC server
- Network issues may result in incomplete or missing samples

## Related Tools

- [get_health](get_health.md) - Check the health of the connected Solana node
- [get_cluster_nodes](get_cluster_nodes.md) - Get information about cluster nodes
- [get_recent_prioritization_fees](get_recent_prioritization_fees.md) - Get recent prioritization fees
- [get_epoch_info](get_epoch_info.md) - Get current epoch information 