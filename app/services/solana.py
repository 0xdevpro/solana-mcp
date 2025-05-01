"""
Solana blockchain service
"""
import requests
from typing import Optional, Dict, Any, List, Tuple, Union
from app.core.config import SOLANA_RPC_URL
from app.models.solana import (
    SolanaBalanceResponse, 
    SolanaAccountInfoResponse, 
    SolanaAccountData,
    SolanaBlockResponse,
    SolanaBlockCommitmentResponse,
    SolanaBlockHeightResponse,
    SolanaBlockProductionResponse,
    SolanaBlockProductionRange,
    SolanaBlocksResponse,
    SolanaBlockTimeResponse,
    SolanaClusterNodesResponse,
    SolanaClusterNodeInfo,
    SolanaEpochInfoResponse,
    SolanaEpochInfo,
    SolanaEpochScheduleResponse,
    SolanaEpochSchedule,
    SolanaFeeForMessageResponse,
    SolanaFirstAvailableBlockResponse,
    SolanaGenesisHashResponse,
    SolanaHealthResponse,
    SolanaHighestSnapshotSlotResponse,
    SolanaSnapshotSlotInfo,
    SolanaIdentityResponse,
    SolanaIdentityInfo,
    SolanaInflationGovernorResponse,
    SolanaInflationGovernor,
    SolanaInflationRateResponse,
    SolanaInflationRate,
    SolanaInflationRewardResponse,
    SolanaInflationRewardItem,
    SolanaLargestAccountsResponse,
    SolanaLargeAccount,
    SolanaLatestBlockhashResponse,
    SolanaBlockhashInfo,
    SolanaLeaderScheduleResponse,
    SolanaMaxRetransmitSlotResponse,
    SolanaMaxShredInsertSlotResponse,
    SolanaMinimumBalanceForRentExemptionResponse
)


def get_solana_balance(address: str) -> SolanaBalanceResponse:
    """
    Get the balance of a Solana wallet address in SOL.
    
    Args:
        address: The Solana wallet address to check
    
    Returns:
        SolanaBalanceResponse: The wallet balance information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [
            address
        ]
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBalanceResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
            
        # Convert lamports to SOL (1 SOL = 10^9 lamports)
        lamports = result["result"]["value"]
        sol_balance = lamports / 1_000_000_000
        
        return SolanaBalanceResponse(
            status="success",
            address=address,
            balance_lamports=lamports,
            balance_sol=sol_balance
        )
    
    except Exception as e:
        return SolanaBalanceResponse(
            status="error",
            message=f"Failed to get balance: {str(e)}"
        )


def get_account_info(address: str, encoding: str = "base58", data_slice: Optional[Dict[str, int]] = None) -> SolanaAccountInfoResponse:
    """
    Get all information associated with the account of provided Pubkey
    
    Args:
        address: The Solana account address to check
        encoding: Encoding format for Account data (base58, base64, base64+zstd, jsonParsed)
        data_slice: Optional slice of account data {offset: int, length: int}
    
    Returns:
        SolanaAccountInfoResponse: The account information
    """
    # Build RPC request params
    params = [address, {"encoding": encoding}]
    
    # Add dataSlice if provided
    if data_slice:
        params[1]["dataSlice"] = data_slice
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": params
    }
    
    print(f"payload{payload}")
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaAccountInfoResponse(
                status="error",
                address=address,
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Check if account exists (result.value will be null if not)
        if result["result"]["value"] is None:
            return SolanaAccountInfoResponse(
                status="success",
                address=address,
                value=None,
                message="Account not found"
            )
            
        # Parse account data
        account_data = result["result"]["value"]
        
        return SolanaAccountInfoResponse(
            status="success",
            address=address,
            value=SolanaAccountData(
                data=account_data["data"],
                executable=account_data["executable"],
                lamports=account_data["lamports"],
                owner=account_data["owner"],
                rentEpoch=account_data["rentEpoch"],
                space=account_data.get("space", 0)  # Some RPC nodes might not return space
            )
        )
        
    except Exception as e:
        return SolanaAccountInfoResponse(
            status="error",
            address=address,
            message=f"Failed to get account info: {str(e)}"
        )


def get_block(
    slot: int, 
    encoding: str = "json", 
    transaction_details: str = "full", 
    rewards: bool = True, 
    max_supported_transaction_version: Optional[int] = None
) -> SolanaBlockResponse:
    """
    Get information about a confirmed block
    
    Args:
        slot: The slot of the block to get
        encoding: Encoding format for transaction data (json, jsonParsed, base58, base64)
        transaction_details: Level of transaction detail to return (full, accounts, signatures, none)
        rewards: Whether to include rewards in the response
        max_supported_transaction_version: Filter for max transaction version
    
    Returns:
        SolanaBlockResponse: The block information
    """
    # Build RPC request params
    params = [
        slot, 
        {
            "encoding": encoding,
            "transactionDetails": transaction_details,
            "rewards": rewards
        }
    ]
    
    # Add maxSupportedTransactionVersion if provided
    if max_supported_transaction_version is not None:
        params[1]["maxSupportedTransactionVersion"] = max_supported_transaction_version
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlock",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlockResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse block data
        block_data = result["result"]
        if block_data is None:
            return SolanaBlockResponse(
                status="success",
                message="Block not found or not confirmed"
            )
            
        # Return block data
        return SolanaBlockResponse(
            status="success",
            **block_data
        )
        
    except Exception as e:
        return SolanaBlockResponse(
            status="error",
            message=f"Failed to get block: {str(e)}"
        )


def get_block_commitment(slot: int) -> SolanaBlockCommitmentResponse:
    """
    Get commitment for a particular block
    
    Args:
        slot: The slot to query commitment information for
    
    Returns:
        SolanaBlockCommitmentResponse: The block commitment information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockCommitment",
        "params": [slot]
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlockCommitmentResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse commitment data
        commitment_data = result["result"]
        
        return SolanaBlockCommitmentResponse(
            status="success",
            commitment=commitment_data.get("commitment"),
            totalStake=commitment_data.get("totalStake")
        )
        
    except Exception as e:
        return SolanaBlockCommitmentResponse(
            status="error",
            message=f"Failed to get block commitment: {str(e)}"
        )


def get_block_height(commitment: Optional[str] = None) -> SolanaBlockHeightResponse:
    """
    Get the current block height of the node
    
    Args:
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaBlockHeightResponse: The block height information
    """
    # Build RPC request params
    params = []
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockHeight",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlockHeightResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        return SolanaBlockHeightResponse(
            status="success",
            blockHeight=result["result"]
        )
        
    except Exception as e:
        return SolanaBlockHeightResponse(
            status="error",
            message=f"Failed to get block height: {str(e)}"
        )


def get_block_production(
    identity: Optional[str] = None,
    first_slot: Optional[int] = None,
    last_slot: Optional[int] = None,
    commitment: Optional[str] = None
) -> SolanaBlockProductionResponse:
    """
    Get the recent block production information
    
    Args:
        identity: Only return results for this validator identity (base-58 encoded)
        first_slot: Start slot of the block production range (inclusive)
        last_slot: End slot of the block production range (inclusive)
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaBlockProductionResponse: The block production information
    """
    # Build RPC request params
    params = []
    config = {}
    
    if identity:
        config["identity"] = identity
    
    if first_slot is not None and last_slot is not None:
        config["range"] = {
            "firstSlot": first_slot,
            "lastSlot": last_slot
        }
    
    if commitment:
        config["commitment"] = commitment
    
    if config:
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockProduction",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlockProductionResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse block production data
        production_data = result["result"]["value"]
        
        return SolanaBlockProductionResponse(
            status="success",
            byIdentity=production_data.get("byIdentity"),
            range=SolanaBlockProductionRange(**production_data.get("range"))
        )
        
    except Exception as e:
        return SolanaBlockProductionResponse(
            status="error",
            message=f"Failed to get block production: {str(e)}"
        )


def get_blocks(
    start_slot: int,
    end_slot: Optional[int] = None,
    commitment: Optional[str] = None
) -> SolanaBlocksResponse:
    """
    Get a list of confirmed blocks between two slots
    
    Args:
        start_slot: Start slot (inclusive)
        end_slot: End slot (inclusive), if None, the latest block will be used
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaBlocksResponse: The list of available blocks
    """
    # Build RPC request params
    params = [start_slot]
    
    # Add end_slot if provided
    if end_slot is not None:
        params.append(end_slot)
        
    # Add commitment config if provided
    if commitment:
        config = {"commitment": commitment}
        # If end_slot is not provided, we need to handle the RPC parameter order correctly
        if end_slot is None:
            params.append(None)  # Add a placeholder for end_slot
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlocks",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlocksResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse blocks data
        blocks = result["result"]
        
        return SolanaBlocksResponse(
            status="success",
            blocks=blocks
        )
        
    except Exception as e:
        return SolanaBlocksResponse(
            status="error",
            message=f"Failed to get blocks: {str(e)}"
        )


def get_blocks_with_limit(
    start_slot: int,
    limit: int,
    commitment: Optional[str] = None
) -> SolanaBlocksResponse:
    """
    Get a list of confirmed blocks starting at a slot with a limit
    
    Args:
        start_slot: Start slot (inclusive)
        limit: Maximum number of blocks to return (must be no more than 500,000)
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaBlocksResponse: The list of available blocks
    """
    # Build RPC request params
    params = [start_slot, limit]
    
    # Add commitment config if provided
    if commitment:
        config = {"commitment": commitment}
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlocksWithLimit",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlocksResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse blocks data
        blocks = result["result"]
        
        return SolanaBlocksResponse(
            status="success",
            blocks=blocks
        )
        
    except Exception as e:
        return SolanaBlocksResponse(
            status="error",
            message=f"Failed to get blocks with limit: {str(e)}"
        )


def get_block_time(slot: int) -> SolanaBlockTimeResponse:
    """
    Get the estimated production time of a block
    
    Args:
        slot: The slot of the block to get the time for
    
    Returns:
        SolanaBlockTimeResponse: The block time information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockTime",
        "params": [slot]
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaBlockTimeResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse block time data
        block_time = result["result"]
        
        # Block time may be null if the block is not available or not confirmed yet
        if block_time is None:
            return SolanaBlockTimeResponse(
                status="success",
                message="Block not found or not confirmed"
            )
            
        return SolanaBlockTimeResponse(
            status="success",
            blockTime=block_time
        )
        
    except Exception as e:
        return SolanaBlockTimeResponse(
            status="error",
            message=f"Failed to get block time: {str(e)}"
        )


def get_cluster_nodes() -> SolanaClusterNodesResponse:
    """
    Get information about all the nodes participating in the cluster
    
    Returns:
        SolanaClusterNodesResponse: The cluster nodes information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getClusterNodes",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaClusterNodesResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse cluster nodes data
        nodes_data = result["result"]
        nodes = []
        
        for node in nodes_data:
            nodes.append(SolanaClusterNodeInfo(
                pubkey=node["pubkey"],
                gossip=node.get("gossip"),
                tpu=node.get("tpu"),
                rpc=node.get("rpc"),
                version=node.get("version"),
                featureSet=node.get("featureSet"),
                shredVersion=node.get("shredVersion")
            ))
            
        return SolanaClusterNodesResponse(
            status="success",
            nodes=nodes
        )
        
    except Exception as e:
        return SolanaClusterNodesResponse(
            status="error",
            message=f"Failed to get cluster nodes: {str(e)}"
        )


def get_epoch_info(commitment: Optional[str] = None) -> SolanaEpochInfoResponse:
    """
    Get information about the current epoch
    
    Args:
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaEpochInfoResponse: The epoch information
    """
    # Build RPC request params
    params = []
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochInfo",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaEpochInfoResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse epoch info data
        epoch_info = result["result"]
        
        return SolanaEpochInfoResponse(
            status="success",
            info=SolanaEpochInfo(
                absoluteSlot=epoch_info["absoluteSlot"],
                blockHeight=epoch_info["blockHeight"],
                epoch=epoch_info["epoch"],
                slotIndex=epoch_info["slotIndex"],
                slotsInEpoch=epoch_info["slotsInEpoch"],
                transactionCount=epoch_info.get("transactionCount")
            )
        )
        
    except Exception as e:
        return SolanaEpochInfoResponse(
            status="error",
            message=f"Failed to get epoch info: {str(e)}"
        )


def get_epoch_schedule() -> SolanaEpochScheduleResponse:
    """
    Get epoch schedule information from this cluster
    
    Returns:
        SolanaEpochScheduleResponse: The epoch schedule information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochSchedule",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaEpochScheduleResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse epoch schedule data
        schedule = result["result"]
        
        return SolanaEpochScheduleResponse(
            status="success",
            schedule=SolanaEpochSchedule(
                slotsPerEpoch=schedule["slotsPerEpoch"],
                leaderScheduleSlotOffset=schedule["leaderScheduleSlotOffset"],
                warmup=schedule["warmup"],
                firstNormalEpoch=schedule["firstNormalEpoch"],
                firstNormalSlot=schedule["firstNormalSlot"]
            )
        )
        
    except Exception as e:
        return SolanaEpochScheduleResponse(
            status="error",
            message=f"Failed to get epoch schedule: {str(e)}"
        )


def get_fee_for_message(message: str, commitment: Optional[str] = None) -> SolanaFeeForMessageResponse:
    """
    Get the fee for a message
    
    Args:
        message: Base-64 encoded message
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaFeeForMessageResponse: The fee information for the message
    """
    # Build RPC request params
    params = [message]
    
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getFeeForMessage",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaFeeForMessageResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse fee data - could be null if the blockhash in the message has expired
        fee = result["result"]["value"]
        
        if fee is None:
            return SolanaFeeForMessageResponse(
                status="success",
                message="Blockhash in the message has expired or is invalid"
            )
            
        return SolanaFeeForMessageResponse(
            status="success",
            fee=fee
        )
        
    except Exception as e:
        return SolanaFeeForMessageResponse(
            status="error",
            message=f"Failed to get fee for message: {str(e)}"
        )


def get_first_available_block() -> SolanaFirstAvailableBlockResponse:
    """
    Get the first available block in the ledger
    
    Returns:
        SolanaFirstAvailableBlockResponse: The first available block information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getFirstAvailableBlock",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaFirstAvailableBlockResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse first available block data
        first_available_block = result["result"]
        
        return SolanaFirstAvailableBlockResponse(
            status="success",
            firstAvailableBlock=first_available_block
        )
        
    except Exception as e:
        return SolanaFirstAvailableBlockResponse(
            status="error",
            message=f"Failed to get first available block: {str(e)}"
        )


def get_genesis_hash() -> SolanaGenesisHashResponse:
    """
    Get the genesis hash of the cluster
    
    Returns:
        SolanaGenesisHashResponse: The genesis hash information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getGenesisHash",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaGenesisHashResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse genesis hash data
        genesis_hash = result["result"]
        
        return SolanaGenesisHashResponse(
            status="success",
            genesisHash=genesis_hash
        )
        
    except Exception as e:
        return SolanaGenesisHashResponse(
            status="error",
            message=f"Failed to get genesis hash: {str(e)}"
        )


def get_health() -> SolanaHealthResponse:
    """
    Get the health of the node
    
    Returns:
        SolanaHealthResponse: The node health information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getHealth",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Special case: Health API returns error when the node is unhealthy
        if "error" in result:
            error_msg = result["error"]["message"]
            # Check if the error is specifically about the node being unhealthy
            if "Node is unhealthy" in error_msg:
                return SolanaHealthResponse(
                    status="success",
                    healthy=False,
                    message=error_msg
                )
            # Otherwise it's a real error
            return SolanaHealthResponse(
                status="error",
                message=f"RPC error: {error_msg}",
                error=result["error"]
            )
        
        # If we reach here, the node is healthy
        return SolanaHealthResponse(
            status="success",
            healthy=True
        )
        
    except Exception as e:
        return SolanaHealthResponse(
            status="error",
            message=f"Failed to get health: {str(e)}"
        )


def get_highest_snapshot_slot() -> SolanaHighestSnapshotSlotResponse:
    """
    Get the highest snapshot slot available
    
    Returns:
        SolanaHighestSnapshotSlotResponse: The highest snapshot slot information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getHighestSnapshotSlot",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaHighestSnapshotSlotResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse highest snapshot slot data
        snapshot_slots = result["result"]
        
        return SolanaHighestSnapshotSlotResponse(
            status="success",
            snapshotSlots=SolanaSnapshotSlotInfo(
                full=snapshot_slots.get("full"),
                incremental=snapshot_slots.get("incremental")
            )
        )
        
    except Exception as e:
        return SolanaHighestSnapshotSlotResponse(
            status="error",
            message=f"Failed to get highest snapshot slot: {str(e)}"
        )


def get_identity() -> SolanaIdentityResponse:
    """
    Get the identity pubkey for the current node
    
    Returns:
        SolanaIdentityResponse: The node identity information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getIdentity",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaIdentityResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse identity data
        identity_data = result["result"]
        
        return SolanaIdentityResponse(
            status="success",
            identity=SolanaIdentityInfo(
                identity=identity_data["identity"]
            )
        )
        
    except Exception as e:
        return SolanaIdentityResponse(
            status="error",
            message=f"Failed to get identity: {str(e)}"
        )


def get_inflation_governor(commitment: Optional[str] = None) -> SolanaInflationGovernorResponse:
    """
    Get the inflation governor parameters
    
    Args:
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaInflationGovernorResponse: The inflation governor parameters
    """
    # Build RPC request params
    params = []
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getInflationGovernor",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaInflationGovernorResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse inflation governor data
        governor_data = result["result"]
        
        return SolanaInflationGovernorResponse(
            status="success",
            governor=SolanaInflationGovernor(
                initial=governor_data["initial"],
                terminal=governor_data["terminal"],
                taper=governor_data["taper"],
                foundation=governor_data["foundation"],
                foundationTerm=governor_data["foundationTerm"]
            )
        )
        
    except Exception as e:
        return SolanaInflationGovernorResponse(
            status="error",
            message=f"Failed to get inflation governor: {str(e)}"
        )


def get_inflation_rate() -> SolanaInflationRateResponse:
    """
    Get the specific inflation values for the current epoch
    
    Returns:
        SolanaInflationRateResponse: The current inflation rate
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getInflationRate",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaInflationRateResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse inflation rate data
        inflation_data = result["result"]
        
        return SolanaInflationRateResponse(
            status="success",
            inflation=SolanaInflationRate(
                total=inflation_data["total"],
                validator=inflation_data["validator"],
                foundation=inflation_data["foundation"],
                epoch=inflation_data["epoch"]
            )
        )
        
    except Exception as e:
        return SolanaInflationRateResponse(
            status="error",
            message=f"Failed to get inflation rate: {str(e)}"
        )


def get_inflation_reward(
    addresses: List[str],
    epoch: Optional[int] = None,
    commitment: Optional[str] = None
) -> SolanaInflationRewardResponse:
    """
    Get inflation reward for a list of addresses
    
    Args:
        addresses: List of account addresses to query
        epoch: Epoch for which to calculate inflation rewards (defaults to previous epoch)
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaInflationRewardResponse: The inflation rewards for the given addresses
    """
    # Build RPC request params
    params = [addresses]
    
    # Create config object if needed
    config = {}
    if epoch is not None:
        config["epoch"] = epoch
    if commitment:
        config["commitment"] = commitment
    
    if config:
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getInflationReward",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaInflationRewardResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse inflation reward data
        reward_data = result["result"]
        rewards = []
        
        for reward in reward_data:
            if reward is None:
                rewards.append(None)
            else:
                rewards.append(SolanaInflationRewardItem(
                    epoch=reward["epoch"],
                    effectiveSlot=reward["effectiveSlot"],
                    amount=reward["amount"],
                    postBalance=reward["postBalance"],
                    commission=reward.get("commission")
                ))
        
        return SolanaInflationRewardResponse(
            status="success",
            rewards=rewards
        )
        
    except Exception as e:
        return SolanaInflationRewardResponse(
            status="error",
            message=f"Failed to get inflation reward: {str(e)}"
        )


def get_largest_accounts(
    filter_opt: Optional[str] = None,
    commitment: Optional[str] = None
) -> SolanaLargestAccountsResponse:
    """
    Get the largest accounts on the network
    
    Args:
        filter_opt: Filter results by account type ("circulating" or "nonCirculating")
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaLargestAccountsResponse: The largest accounts information
    """
    # Build RPC request params
    params = []
    
    # Create config object if needed
    config = {}
    if filter_opt:
        config["filter"] = filter_opt
    if commitment:
        config["commitment"] = commitment
    
    if config:
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLargestAccounts",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaLargestAccountsResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse largest accounts data
        accounts_data = result["result"]["value"]
        accounts = []
        
        for account in accounts_data:
            accounts.append(SolanaLargeAccount(
                address=account["address"],
                lamports=account["lamports"]
            ))
        
        return SolanaLargestAccountsResponse(
            status="success",
            accounts=accounts
        )
        
    except Exception as e:
        return SolanaLargestAccountsResponse(
            status="error",
            message=f"Failed to get largest accounts: {str(e)}"
        )


def get_latest_blockhash(commitment: Optional[str] = None) -> SolanaLatestBlockhashResponse:
    """
    Get the latest blockhash
    
    Args:
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaLatestBlockhashResponse: The latest blockhash information
    """
    # Build RPC request params
    params = []
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLatestBlockhash",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaLatestBlockhashResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse latest blockhash data
        value = result["result"]["value"]
        
        return SolanaLatestBlockhashResponse(
            status="success",
            value=SolanaBlockhashInfo(
                blockhash=value["blockhash"],
                lastValidBlockHeight=value["lastValidBlockHeight"]
            )
        )
        
    except Exception as e:
        return SolanaLatestBlockhashResponse(
            status="error",
            message=f"Failed to get latest blockhash: {str(e)}"
        )


def get_leader_schedule(
    slot: Optional[int] = None,
    identity: Optional[str] = None,
    commitment: Optional[str] = None
) -> SolanaLeaderScheduleResponse:
    """
    Get the leader schedule for the current or a specific epoch
    
    Args:
        slot: Slot to get leader schedule for (defaults to current slot)
        identity: Filter results for this validator identity (base-58 encoded)
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaLeaderScheduleResponse: The leader schedule information
    """
    # Build RPC request params
    params = []
    
    # Add slot if provided
    if slot is not None:
        params.append(slot)
    
    # Create config object if needed
    config = {}
    if identity:
        config["identity"] = identity
    if commitment:
        config["commitment"] = commitment
    
    if config:
        # If slot wasn't provided but we have config, add null for slot
        if slot is None:
            params.append(None)
        params.append(config)
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLeaderSchedule",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaLeaderScheduleResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse leader schedule data
        schedule = result["result"]
        
        # Handle case where schedule might be null
        if schedule is None:
            return SolanaLeaderScheduleResponse(
                status="success",
                message="No leader schedule found for the given parameters"
            )
        
        return SolanaLeaderScheduleResponse(
            status="success",
            schedule=schedule
        )
        
    except Exception as e:
        return SolanaLeaderScheduleResponse(
            status="error",
            message=f"Failed to get leader schedule: {str(e)}"
        )


def get_max_retransmit_slot() -> SolanaMaxRetransmitSlotResponse:
    """
    Get the max slot that has been retransmitted by the node
    
    Returns:
        SolanaMaxRetransmitSlotResponse: The max retransmit slot information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMaxRetransmitSlot",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaMaxRetransmitSlotResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse max retransmit slot data
        max_retransmit_slot = result["result"]
        
        return SolanaMaxRetransmitSlotResponse(
            status="success",
            maxRetransmitSlot=max_retransmit_slot
        )
        
    except Exception as e:
        return SolanaMaxRetransmitSlotResponse(
            status="error",
            message=f"Failed to get max retransmit slot: {str(e)}"
        )


def get_max_shred_insert_slot() -> SolanaMaxShredInsertSlotResponse:
    """
    Get the highest slot where shreds have been inserted by the node
    
    Returns:
        SolanaMaxShredInsertSlotResponse: The max shred insert slot information
    """
    # Build RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMaxShredInsertSlot",
        "params": []
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaMaxShredInsertSlotResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse max shred insert slot data
        max_shred_insert_slot = result["result"]
        
        return SolanaMaxShredInsertSlotResponse(
            status="success",
            maxShredInsertSlot=max_shred_insert_slot
        )
        
    except Exception as e:
        return SolanaMaxShredInsertSlotResponse(
            status="error",
            message=f"Failed to get max shred insert slot: {str(e)}"
        )


def get_minimum_balance_for_rent_exemption(
    data_size: int,
    commitment: Optional[str] = None
) -> SolanaMinimumBalanceForRentExemptionResponse:
    """
    Get the minimum balance required for rent exemption for a data size
    
    Args:
        data_size: Size of data in bytes
        commitment: The level of commitment (processed, confirmed, finalized)
    
    Returns:
        SolanaMinimumBalanceForRentExemptionResponse: The minimum balance information
    """
    # Build RPC request params
    params = [data_size]
    
    if commitment:
        params.append({"commitment": commitment})
    
    # Build full RPC request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMinimumBalanceForRentExemption",
        "params": params
    }
    
    # Send request to Solana RPC node
    try:
        response = requests.post(SOLANA_RPC_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            return SolanaMinimumBalanceForRentExemptionResponse(
                status="error",
                message=f"RPC error: {result['error']['message']}",
                error=result["error"]
            )
        
        # Parse minimum balance data
        lamports = result["result"]
        
        return SolanaMinimumBalanceForRentExemptionResponse(
            status="success",
            lamports=lamports
        )
        
    except Exception as e:
        return SolanaMinimumBalanceForRentExemptionResponse(
            status="error",
            message=f"Failed to get minimum balance for rent exemption: {str(e)}"
        ) 