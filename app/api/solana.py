"""
Solana blockchain endpoints
"""
from typing import Optional, Dict, List
from pydantic import Field
from app.api import app
from app.services.solana import (
    get_solana_balance, 
    get_account_info,
    get_block,
    get_block_commitment,
    get_block_height,
    get_block_production,
    get_blocks,
    get_blocks_with_limit,
    get_block_time,
    get_cluster_nodes,
    get_epoch_info,
    get_epoch_schedule,
    get_fee_for_message,
    get_first_available_block,
    get_genesis_hash,
    get_health,
    get_highest_snapshot_slot,
    get_identity,
    get_inflation_governor,
    get_inflation_rate,
    get_inflation_reward,
    get_largest_accounts,
    get_latest_blockhash,
    get_leader_schedule,
    get_max_retransmit_slot,
    get_max_shred_insert_slot,
    get_minimum_balance_for_rent_exemption
)
from app.models.solana import (
    SolanaBalanceResponse, 
    SolanaAccountInfoResponse,
    SolanaBlockResponse,
    SolanaBlockCommitmentResponse,
    SolanaBlockHeightResponse,
    SolanaBlockProductionResponse,
    SolanaBlocksResponse,
    SolanaBlockTimeResponse,
    SolanaClusterNodesResponse,
    SolanaEpochInfoResponse,
    SolanaEpochScheduleResponse,
    SolanaFeeForMessageResponse,
    SolanaFirstAvailableBlockResponse,
    SolanaGenesisHashResponse,
    SolanaHealthResponse,
    SolanaHighestSnapshotSlotResponse,
    SolanaIdentityResponse,
    SolanaInflationGovernorResponse,
    SolanaInflationRateResponse,
    SolanaInflationRewardResponse,
    SolanaLargestAccountsResponse,
    SolanaLatestBlockhashResponse,
    SolanaLeaderScheduleResponse,
    SolanaMaxRetransmitSlotResponse,
    SolanaMaxShredInsertSlotResponse,
    SolanaMinimumBalanceForRentExemptionResponse
)


@app.tool(
    name="get_solana_balance",
    description="Get the SOL balance for a Solana wallet address.",
    tags={"solana", "balance", "crypto"}
)
def get_solana_balance_endpoint(
    address: str = Field(description="The Solana wallet address to check")
) -> dict:
    """
    Get the balance of a Solana wallet address in SOL.
    
    This tool will query the Solana blockchain via RPC to retrieve the current
    balance of the specified wallet address.
    """
    response = get_solana_balance(address)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_account_info",
    description="Get all information associated with a Solana account by its address.",
    tags={"solana", "account", "crypto"}
)
def get_account_info_endpoint(
    address: str = Field(description="The Solana account address to query, as base-58 encoded string"),
    encoding: str = Field(
        default="base58", 
        description="Encoding format for Account data (base58, base64, base64+zstd, jsonParsed)"
    ),
    data_slice_offset: Optional[int] = Field(
        default=None, 
        description="Byte offset to start reading account data (only for base58, base64, or base64+zstd encodings)"
    ),
    data_slice_length: Optional[int] = Field(
        default=None, 
        description="Number of bytes to return (only for base58, base64, or base64+zstd encodings)"
    )
) -> dict:
    """
    Get all information associated with the account of provided Pubkey.
    
    This tool queries the Solana blockchain via RPC to retrieve detailed account information
    including balance, owner, executable status, and data in the specified encoding format.
    
    For token accounts, program accounts, and other specialized account types, 
    use 'jsonParsed' encoding to receive structured data.
    """
    # Build data_slice dictionary if both offset and length are provided
    data_slice = None
    if data_slice_offset is not None and data_slice_length is not None:
        data_slice = {"offset": data_slice_offset, "length": data_slice_length}
    
    response = get_account_info(address, encoding, data_slice)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_block",
    description="Get information about a confirmed block by slot number.",
    tags={"solana", "block", "crypto"}
)
def get_block_endpoint(
    slot: int = Field(description="The slot of the block to query"),
    encoding: str = Field(
        default="json", 
        description="Encoding format for transaction data (json, jsonParsed, base58, base64)"
    ),
    transaction_details: str = Field(
        default="full", 
        description="Level of transaction detail to return (full, accounts, signatures, none)"
    ),
    rewards: bool = Field(
        default=True, 
        description="Whether to include rewards in the response"
    ),
    max_supported_transaction_version: Optional[int] = Field(
        default=None, 
        description="Filter for max transaction version"
    )
) -> dict:
    """
    Get information about a confirmed block.
    
    This tool queries the Solana blockchain via RPC to retrieve detailed information
    about a block at the specified slot, including transactions and their statuses.
    
    Use 'accounts' for transaction_details to get a faster response with account balance changes.
    Set rewards to False if you don't need validator rewards information.
    """
    response = get_block(
        slot, 
        encoding, 
        transaction_details, 
        rewards, 
        max_supported_transaction_version
    )
    return response.dict(exclude_none=True)


@app.tool(
    name="get_block_commitment",
    description="Get commitment (confirmation status) information for a block.",
    tags={"solana", "block", "crypto"}
)
def get_block_commitment_endpoint(
    slot: int = Field(description="The slot to query commitment information for")
) -> dict:
    """
    Get commitment information for a particular block.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    how much stake has voted for a block at the specified slot.
    """
    response = get_block_commitment(slot)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_block_height",
    description="Get the current block height of the Solana node.",
    tags={"solana", "block", "crypto"}
)
def get_block_height_endpoint(
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the current block height of the node.
    
    This tool queries the Solana blockchain via RPC to retrieve the current block height
    of the connected Solana node according to the specified commitment level.
    
    Commitment level determines the confirmation status of blocks:
    - 'processed': The node has received and processed the block (fastest, least certain)
    - 'confirmed': The block has received a supermajority of votes
    - 'finalized': The block has been confirmed as final and won't be rolled back (slowest, most certain)
    """
    response = get_block_height(commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_block_production",
    description="Get recent block production information from the Solana network.",
    tags={"solana", "block", "crypto", "validator"}
)
def get_block_production_endpoint(
    identity: Optional[str] = Field(
        default=None, 
        description="Only return results for this validator identity (base-58 encoded)"
    ),
    first_slot: Optional[int] = Field(
        default=None, 
        description="Start slot of the block production range (inclusive)"
    ),
    last_slot: Optional[int] = Field(
        default=None, 
        description="End slot of the block production range (inclusive)"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get information about recent block production by validators.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    which validators have produced and skipped blocks (leader slots) in the given
    range of slots.
    
    You can filter results to a specific validator identity, specify a range of slots,
    and choose the commitment level for confirmation status.
    """
    response = get_block_production(identity, first_slot, last_slot, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_blocks",
    description="Get a list of confirmed blocks between two slots.",
    tags={"solana", "block", "crypto"}
)
def get_blocks_endpoint(
    start_slot: int = Field(description="Start slot (inclusive)"),
    end_slot: Optional[int] = Field(
        default=None, 
        description="End slot (inclusive), if not provided, latest block will be used"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get a list of confirmed blocks between two slots.
    
    This tool queries the Solana blockchain via RPC to retrieve a list of confirmed
    blocks between the specified start and end slots.
    
    Note that not every slot produces a block, so there may be gaps in the sequence
    of block numbers returned.
    """
    response = get_blocks(start_slot, end_slot, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_blocks_with_limit",
    description="Get a list of confirmed blocks starting at a slot with a limit.",
    tags={"solana", "block", "crypto"}
)
def get_blocks_with_limit_endpoint(
    start_slot: int = Field(description="Start slot (inclusive)"),
    limit: int = Field(
        description="Maximum number of blocks to return (must be no more than 500,000)"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get a list of confirmed blocks starting at a slot with a limit.
    
    This tool queries the Solana blockchain via RPC to retrieve a list of confirmed
    blocks starting at the specified slot, up to the specified limit.
    
    Note that not every slot produces a block, so there may be gaps in the sequence
    of block numbers returned.
    """
    response = get_blocks_with_limit(start_slot, limit, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_block_time",
    description="Get the estimated production time of a block.",
    tags={"solana", "block", "crypto"}
)
def get_block_time_endpoint(
    slot: int = Field(description="The slot of the block to get the time for")
) -> dict:
    """
    Get the estimated production time of a block.
    
    This tool queries the Solana blockchain via RPC to retrieve the estimated
    production time of a block at the specified slot. The time is returned as a
    Unix timestamp (seconds since the Unix epoch).
    
    Returns null if the block is not available or not yet confirmed.
    """
    response = get_block_time(slot)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_cluster_nodes",
    description="Get information about the nodes in the Solana cluster.",
    tags={"solana", "network", "validator", "crypto"}
)
def get_cluster_nodes_endpoint() -> dict:
    """
    Get information about all the nodes participating in the cluster.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    the nodes in the cluster, including their public keys, gossip and RPC addresses,
    and software versions.
    """
    response = get_cluster_nodes()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_epoch_info",
    description="Get information about the current epoch.",
    tags={"solana", "epoch", "crypto"}
)
def get_epoch_info_endpoint(
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get information about the current epoch.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    the current epoch, including the current slot, block height, and slots in the epoch.
    
    You can specify the commitment level to determine the confirmation status of the data.
    """
    response = get_epoch_info(commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_epoch_schedule",
    description="Get epoch schedule information from the Solana cluster.",
    tags={"solana", "epoch", "crypto"}
)
def get_epoch_schedule_endpoint() -> dict:
    """
    Get epoch schedule information from the Solana cluster.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    the epoch schedule, including the number of slots in each epoch and other
    schedule-related parameters.
    """
    response = get_epoch_schedule()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_fee_for_message",
    description="Get the fee in lamports for a message.",
    tags={"solana", "fee", "transaction", "crypto"}
)
def get_fee_for_message_endpoint(
    message: str = Field(description="Base-64 encoded message to get the fee for"),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the fee in lamports for a message.
    
    This tool queries the Solana blockchain via RPC to retrieve the fee that would be
    charged for a transaction containing the given message.
    
    The message must be base-64 encoded, and should be properly formatted according to
    the Solana transaction message format (typically created by a Solana SDK).
    
    Returns null if the blockhash in the message has expired or is invalid.
    """
    response = get_fee_for_message(message, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_first_available_block",
    description="Get the first available block in the Solana ledger.",
    tags={"solana", "block", "crypto"}
)
def get_first_available_block_endpoint() -> dict:
    """
    Get the first available block in the Solana ledger.
    
    This tool queries the Solana blockchain via RPC to retrieve the slot number
    of the first available block in the ledger. This can be useful for determining
    the earliest point from which historical data can be retrieved.
    """
    response = get_first_available_block()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_genesis_hash",
    description="Get the genesis hash of the Solana cluster.",
    tags={"solana", "genesis", "crypto"}
)
def get_genesis_hash_endpoint() -> dict:
    """
    Get the genesis hash of the Solana cluster.
    
    This tool queries the Solana blockchain via RPC to retrieve the genesis hash,
    which is a unique identifier for the blockchain network. Different Solana clusters
    (mainnet, testnet, devnet) have different genesis hashes.
    
    This can be useful for verifying that you are connected to the expected network.
    """
    response = get_genesis_hash()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_health",
    description="Check the health of the connected Solana node.",
    tags={"solana", "health", "network", "crypto"}
)
def get_health_endpoint() -> dict:
    """
    Check the health of the connected Solana node.
    
    This tool queries the Solana blockchain via RPC to check if the node is healthy.
    This can be useful for monitoring the status of the node and ensuring that it
    is operational before sending transactions or queries.
    
    Returns a boolean indicating whether the node is healthy, and a message if the
    node is unhealthy.
    """
    response = get_health()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_highest_snapshot_slot",
    description="Get the highest snapshot slots available on the Solana node.",
    tags={"solana", "snapshot", "block", "crypto"}
)
def get_highest_snapshot_slot_endpoint() -> dict:
    """
    Get the highest snapshot slots available on the Solana node.
    
    This tool queries the Solana blockchain via RPC to retrieve information about
    the highest snapshot slots available on the node. Snapshots are used for fast
    startup of validators and for creating new validator nodes.
    
    Returns information about both full and incremental snapshots.
    """
    response = get_highest_snapshot_slot()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_identity",
    description="Get the identity public key of the current Solana node.",
    tags={"solana", "node", "identity", "crypto"}
)
def get_identity_endpoint() -> dict:
    """
    Get the identity public key of the current Solana node.
    
    This tool queries the Solana blockchain via RPC to retrieve the identity
    public key of the node you are connected to. This is useful for verifying
    which validator you are communicating with.
    """
    response = get_identity()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_inflation_governor",
    description="Get the inflation governor parameters from the Solana cluster.",
    tags={"solana", "inflation", "economics", "crypto"}
)
def get_inflation_governor_endpoint(
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the inflation governor parameters from the Solana cluster.
    
    This tool queries the Solana blockchain via RPC to retrieve the inflation
    governor parameters, which control how the inflation rate changes over time.
    
    These parameters include the initial inflation rate, terminal inflation rate,
    rate of inflation reduction (taper), foundation inflation rate, and foundation term.
    """
    response = get_inflation_governor(commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_inflation_rate",
    description="Get the current inflation rate of the Solana network.",
    tags={"solana", "inflation", "economics", "crypto"}
)
def get_inflation_rate_endpoint() -> dict:
    """
    Get the current inflation rate of the Solana network.
    
    This tool queries the Solana blockchain via RPC to retrieve the current
    inflation rate, including the total inflation and how it's divided between
    validators and the Solana Foundation.
    
    This is useful for understanding the current tokenomics of the Solana network.
    """
    response = get_inflation_rate()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_inflation_reward",
    description="Get inflation rewards for a list of Solana accounts.",
    tags={"solana", "inflation", "rewards", "staking", "crypto"}
)
def get_inflation_reward_endpoint(
    addresses: List[str] = Field(description="List of account addresses to query rewards for"),
    epoch: Optional[int] = Field(
        default=None, 
        description="Epoch to query rewards for (defaults to previous epoch)"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get inflation rewards for a list of Solana accounts.
    
    This tool queries the Solana blockchain via RPC to retrieve inflation reward
    information for the specified accounts, typically used for validator and stake accounts.
    
    For each address, returns information about rewards earned, including:
    - Epoch in which the reward was earned
    - Effective slot at which the reward was calculated
    - Amount of the reward in lamports
    - Post-reward balance of the account in lamports
    - Commission of vote accounts (if applicable)
    
    Returns null for addresses that are not found or did not receive rewards.
    """
    response = get_inflation_reward(addresses, epoch, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_largest_accounts",
    description="Get the largest accounts on the Solana network.",
    tags={"solana", "accounts", "balance", "crypto"}
)
def get_largest_accounts_endpoint(
    filter_opt: Optional[str] = Field(
        default=None, 
        description="Filter by account type: 'circulating' or 'nonCirculating'"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the largest accounts on the Solana network.
    
    This tool queries the Solana blockchain via RPC to retrieve a list of the
    largest accounts by balance. You can optionally filter to show only circulating
    or non-circulating accounts.
    
    This is useful for analyzing wealth distribution on the Solana network.
    """
    response = get_largest_accounts(filter_opt, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_latest_blockhash",
    description="Get the latest blockhash",
    tags={"solana", "block", "crypto"}
)
def get_latest_blockhash_endpoint(
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the latest blockhash
    """
    response = get_latest_blockhash(commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_leader_schedule",
    description="Get the leader schedule for the current or a specific epoch",
    tags={"solana", "block", "crypto"}
)
def get_leader_schedule_endpoint(
    slot: Optional[int] = Field(
        default=None, 
        description="Slot to get leader schedule for (defaults to current slot)"
    ),
    identity: Optional[str] = Field(
        default=None, 
        description="Filter results for this validator identity (base-58 encoded)"
    ),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the leader schedule for the current or a specific epoch
    """
    response = get_leader_schedule(slot, identity, commitment)
    return response.dict(exclude_none=True)


@app.tool(
    name="get_max_retransmit_slot",
    description="Get the max slot that has been retransmitted by the node",
    tags={"solana", "block", "crypto"}
)
def get_max_retransmit_slot_endpoint() -> dict:
    """
    Get the max slot that has been retransmitted by the node
    """
    response = get_max_retransmit_slot()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_max_shred_insert_slot",
    description="Get the highest slot where shreds have been inserted by the node",
    tags={"solana", "block", "crypto"}
)
def get_max_shred_insert_slot_endpoint() -> dict:
    """
    Get the highest slot where shreds have been inserted by the node
    """
    response = get_max_shred_insert_slot()
    return response.dict(exclude_none=True)


@app.tool(
    name="get_minimum_balance_for_rent_exemption",
    description="Get the minimum balance required for rent exemption for a data size",
    tags={"solana", "block", "crypto"}
)
def get_minimum_balance_for_rent_exemption_endpoint(
    data_size: int = Field(description="Size of data in bytes"),
    commitment: Optional[str] = Field(
        default=None, 
        description="The level of commitment (processed, confirmed, finalized)"
    )
) -> dict:
    """
    Get the minimum balance required for rent exemption for a data size
    """
    response = get_minimum_balance_for_rent_exemption(data_size, commitment)
    return response.dict(exclude_none=True)


# Create router for organization purposes
router = None  # No actual router is needed since FastMCP handles this 