# Solana MCP Server

A Python-based MCP Server for interacting with the Solana blockchain using FastMCP.

## Features

- Get Solana account balance using the `getBalance` RPC method
- Support for all Solana clusters (mainnet, devnet, testnet)
- Configurable commitment levels (finalized, confirmed, processed)
- Environment-based configuration

## Setup

### Prerequisites

- Python 3.11 or higher
- uv package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xdevpro/solana-mcp.git
   cd solana-mcp
   ```

2. Set up the environment:
   ```bash
   cp .env.example .env
   ```

3. Install dependencies using uv:
   ```bash
    uv venv
    source .venv/bin/activate
   uv pip install -e .
   ```
4. dev:
  ```bash
  fastmcp dev main.py
  ```

## Configuration

Configure the application by modifying the `.env` file:

```env
# Solana RPC endpoints
SOLANA_MAINNET_URL=https://api.mainnet-beta.solana.com

# MCP Server configuration
SERVER_HOST=0.0.0.0
#SERVER_PORT=3000
```

## Usage

### Running the Server

Start the MCP server:

```bash
uv run main.py
```

The server will start at `http://0.0.0.0:3000` (or as configured in your `.env` file).

### API Documentation

Once the server is running, you can access the auto-generated API documentation at:

```
http://localhost:3000/docs
```

## Available Tools

This MCP server provides the following Solana API tools:

### General
### Account Information
- [get_solana_balance](docs/get_solana_balance.md) - Get the SOL balance for a Solana wallet address
- [get_account_info](docs/get_account_info.md) - Get all information associated with a Solana account by its address
- [get_multiple_accounts](docs/get_multiple_accounts.md) - Get information for multiple Solana accounts at once
- [get_program_accounts](docs/get_program_accounts.md) - Get all accounts owned by a specific Solana program
- [get_largest_accounts](docs/get_largest_accounts.md) - Get the largest accounts on the Solana network
- [get_minimum_balance_for_rent_exemption](docs/get_minimum_balance_for_rent_exemption.md) - Get the minimum balance required for rent exemption for a data size

### Block Information
- [get_block](docs/get_block.md) - Get information about a confirmed block by slot number
- [get_block_commitment](docs/get_block_commitment.md) - Get commitment (confirmation status) information for a block
- [get_block_height](docs/get_block_height.md) - Get the current block height of the Solana node
- [get_block_production](docs/get_block_production.md) - Get recent block production information from the Solana network
- [get_blocks](docs/get_blocks.md) - Get a list of confirmed blocks between two slots
- [get_blocks_with_limit](docs/get_blocks_with_limit.md) - Get a list of confirmed blocks starting at a slot with a limit
- [get_block_time](docs/get_block_time.md) - Get the estimated production time of a block
- [get_first_available_block](docs/get_first_available_block.md) - Get the first available block in the Solana ledger
- [get_latest_blockhash](docs/get_latest_blockhash.md) - Get the latest blockhash
- [get_max_retransmit_slot](docs/get_max_retransmit_slot.md) - Get the max slot that has been retransmitted by the node
- [get_max_shred_insert_slot](docs/get_max_shred_insert_slot.md) - Get the highest slot where shreds have been inserted by the node

### Epoch & Schedule Information
- [get_epoch_info](docs/get_epoch_info.md) - Get information about the current epoch
- [get_epoch_schedule](docs/get_epoch_schedule.md) - Get epoch schedule information from the Solana cluster
- [get_leader_schedule](docs/get_leader_schedule.md) - Get the leader schedule for the current or a specific epoch

### Network & Node Information
- [get_cluster_nodes](docs/get_cluster_nodes.md) - Get information about the nodes in the Solana cluster
- [get_genesis_hash](docs/get_genesis_hash.md) - Get the genesis hash of the Solana cluster
- [get_health](docs/get_health.md) - Check the health of the connected Solana node
- [get_highest_snapshot_slot](docs/get_highest_snapshot_slot.md) - Get the highest snapshot slots available on the Solana node
- [get_identity](docs/get_identity.md) - Get the identity public key of the current Solana node
- [get_recent_performance_samples](docs/get_recent_performance_samples.md) - Get recent performance samples from the Solana network

### Transaction & Fee Information
- [get_fee_for_message](docs/get_fee_for_message.md) - Get the fee in lamports for a message
- [get_recent_prioritization_fees](docs/get_recent_prioritization_fees.md) - Get recent prioritization fees from the Solana network

### Inflation & Economics
- [get_inflation_governor](docs/get_inflation_governor.md) - Get the inflation governor parameters from the Solana cluster
- [get_inflation_rate](docs/get_inflation_rate.md) - Get the current inflation rate of the Solana network
- [get_inflation_reward](docs/get_inflation_reward.md) - Get inflation rewards for a list of Solana accounts

## Development

### Project Structure

```
solana-mcp/
├── .env                   # Environment configuration (not in git)
├── .env.example           # Example environment configuration
├── .gitignore
├── .python-version
├── app/                   # Application code
│   ├── __init__.py
│   ├── api/               # API endpoints and MCP tools
│   ├── models/            # Data models
│   ├── services/          # Business logic and RPC handling
│   └── core/              # Core configuration
├── docs/                  # Tool documentation
├── main.py                # Entry point
├── pyproject.toml         # Project dependencies
├── README.md
└── uv.lock                # uv lock file
```

## License

MIT