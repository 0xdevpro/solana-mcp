"""
Solana data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Any, Dict


class SolanaBalanceResponse(BaseModel):
    """Response model for Solana balance queries"""
    status: str
    address: str = Field(None, description="The queried Solana wallet address")
    balance_lamports: int = Field(None, description="Balance in lamports")
    balance_sol: float = Field(None, description="Balance in SOL")
    message: str = Field(None, description="Error message if status is error")
    error: dict = Field(None, description="Error details if status is error")


class SolanaAccountData(BaseModel):
    """Model for account data in different encoding formats"""
    data: Union[List[str], dict] = Field(description="Account data in the specified encoding format")
    executable: bool = Field(description="Whether the account contains a program and is strictly read-only")
    lamports: int = Field(description="Number of lamports assigned to this account")
    owner: str = Field(description="Base-58 encoded Pubkey of the program this account has been assigned to")
    rentEpoch: int = Field(description="The epoch at which this account will next owe rent")
    space: int = Field(description="The data size of the account")


class SolanaAccountInfoResponse(BaseModel):
    """Response model for Solana account info queries"""
    status: str
    address: str = Field(None, description="The queried Solana account address")
    value: Optional[SolanaAccountData] = Field(None, description="Account information if found")
    message: str = Field(None, description="Error message if status is error")
    error: dict = Field(None, description="Error details if status is error")


class SolanaTransactionMeta(BaseModel):
    """Model for transaction metadata in block"""
    err: Optional[Any] = Field(None, description="Error if transaction failed, null if successful")
    fee: int = Field(description="Fee this transaction was charged")
    preBalances: List[int] = Field(description="List of balances for each account before transaction")
    postBalances: List[int] = Field(description="List of balances for each account after transaction")
    preTokenBalances: List[Dict] = Field(default=[], description="List of token balances before transaction")
    postTokenBalances: List[Dict] = Field(default=[], description="List of token balances after transaction")
    status: Optional[Dict] = Field(None, description="Transaction status")


class SolanaTransactionInBlock(BaseModel):
    """Model for transaction in block"""
    meta: SolanaTransactionMeta = Field(description="Transaction metadata")
    transaction: Dict = Field(description="Transaction details including signatures and account keys")
    version: Optional[int] = Field(None, description="Transaction version")


class SolanaBlockResponse(BaseModel):
    """Response model for Solana block queries"""
    status: str
    blockHeight: Optional[int] = Field(None, description="The block height")
    blockTime: Optional[int] = Field(None, description="The timestamp of this block")
    blockhash: Optional[str] = Field(None, description="The blockhash of this block")
    parentSlot: Optional[int] = Field(None, description="The slot index of this block's parent")
    previousBlockhash: Optional[str] = Field(None, description="The blockhash of this block's parent")
    transactions: Optional[List[SolanaTransactionInBlock]] = Field(None, description="An array of transactions and transaction statuses")
    rewards: Optional[List] = Field(None, description="Block rewards if requested")
    slot: Optional[int] = Field(None, description="The slot index of this block")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlocksResponse(BaseModel):
    """Response model for Solana blocks queries"""
    status: str
    blocks: Optional[List[int]] = Field(None, description="List of available block slot numbers")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlockCommitmentResponse(BaseModel):
    """Response model for block commitment queries"""
    status: str
    commitment: Optional[List[int]] = Field(None, description="Array of u64 integers, one for each confirmed block. Each integer is the total stake at that snapshort that voted for the block")
    totalStake: Optional[int] = Field(None, description="Total active stake, in lamports, of the current epoch")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlockHeightResponse(BaseModel):
    """Response model for block height queries"""
    status: str
    blockHeight: Optional[int] = Field(None, description="Current block height")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlockProductionRange(BaseModel):
    """Range of block production"""
    firstSlot: int = Field(description="First slot in the block production range (inclusive)")
    lastSlot: int = Field(description="Last slot in the block production range (inclusive)")


class SolanaBlockProductionEntry(BaseModel):
    """Block production entry for an identity"""
    slotsLeader: int = Field(description="Number of leader slots")
    slotsSkipped: int = Field(description="Number of leader slots that were skipped by this identity")


class SolanaBlockProductionResponse(BaseModel):
    """Response model for block production queries"""
    status: str
    byIdentity: Optional[Dict[str, SolanaBlockProductionEntry]] = Field(None, description="Block production per identity pubkey as base-58 string")
    range: Optional[SolanaBlockProductionRange] = Field(None, description="Range of slots queried")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlockTimeResponse(BaseModel):
    """Response model for block time queries"""
    status: str
    blockTime: Optional[int] = Field(None, description="The estimated production time, as Unix timestamp (seconds since the Unix epoch)")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaClusterNodeInfo(BaseModel):
    """Model for information about a cluster node"""
    pubkey: str = Field(description="Node public key, as base-58 encoded string")
    gossip: Optional[str] = Field(None, description="Gossip network address for the node")
    tpu: Optional[str] = Field(None, description="TPU network address for the node")
    rpc: Optional[str] = Field(None, description="JSON RPC network address for the node, null if not available")
    version: Optional[str] = Field(None, description="Software version of the node, null if not available")
    featureSet: Optional[int] = Field(None, description="The unique identifier of the node's feature set")
    shredVersion: Optional[int] = Field(None, description="The shred version of the node")


class SolanaClusterNodesResponse(BaseModel):
    """Response model for cluster nodes queries"""
    status: str
    nodes: Optional[List[SolanaClusterNodeInfo]] = Field(None, description="List of cluster node information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaEpochInfo(BaseModel):
    """Model for epoch information"""
    absoluteSlot: int = Field(description="The current slot")
    blockHeight: int = Field(description="The current block height")
    epoch: int = Field(description="The current epoch")
    slotIndex: int = Field(description="The current slot relative to the start of the current epoch")
    slotsInEpoch: int = Field(description="The number of slots in this epoch")
    transactionCount: Optional[int] = Field(None, description="Total transaction count since genesis")


class SolanaEpochInfoResponse(BaseModel):
    """Response model for epoch info queries"""
    status: str
    info: Optional[SolanaEpochInfo] = Field(None, description="Current epoch information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaEpochSchedule(BaseModel):
    """Model for epoch schedule"""
    slotsPerEpoch: int = Field(description="The number of slots in each epoch")
    leaderScheduleSlotOffset: int = Field(description="The number of slots before beginning of an epoch to calculate leader schedule for that epoch")
    warmup: bool = Field(description="Whether epochs start short and grow")
    firstNormalEpoch: int = Field(description="First normal-length epoch, log2(slotsPerEpoch) - log2(MINIMUM_SLOTS_PER_EPOCH)")
    firstNormalSlot: int = Field(description="MINIMUM_SLOTS_PER_EPOCH * (2.pow(firstNormalEpoch) - 1)")


class SolanaEpochScheduleResponse(BaseModel):
    """Response model for epoch schedule queries"""
    status: str
    schedule: Optional[SolanaEpochSchedule] = Field(None, description="Epoch schedule information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaFeeForMessageResponse(BaseModel):
    """Response model for fee for message queries"""
    status: str
    fee: Optional[int] = Field(None, description="Fee in lamports for the message")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaFirstAvailableBlockResponse(BaseModel):
    """Response model for first available block queries"""
    status: str
    firstAvailableBlock: Optional[int] = Field(None, description="First available block slot number")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaGenesisHashResponse(BaseModel):
    """Response model for genesis hash queries"""
    status: str
    genesisHash: Optional[str] = Field(None, description="Genesis hash as base-58 encoded string")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaHealthResponse(BaseModel):
    """Response model for health queries"""
    status: str
    healthy: Optional[bool] = Field(None, description="Indicates if the node is healthy or not")
    message: Optional[str] = Field(None, description="Error message if status is error or node is not healthy")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaSnapshotSlotInfo(BaseModel):
    """Model for snapshot slot information"""
    full: Optional[int] = Field(None, description="The highest full snapshot slot")
    incremental: Optional[int] = Field(None, description="The highest incremental snapshot slot based on full")


class SolanaHighestSnapshotSlotResponse(BaseModel):
    """Response model for highest snapshot slot queries"""
    status: str
    snapshotSlots: Optional[SolanaSnapshotSlotInfo] = Field(None, description="Highest snapshot slot information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaIdentityInfo(BaseModel):
    """Model for node identity information"""
    identity: str = Field(description="Node identity pubkey")


class SolanaIdentityResponse(BaseModel):
    """Response model for node identity queries"""
    status: str
    identity: Optional[SolanaIdentityInfo] = Field(None, description="Node identity information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaInflationGovernor(BaseModel):
    """Model for inflation governor settings"""
    initial: float = Field(description="Initial inflation rate in percentage")
    terminal: float = Field(description="Terminal inflation rate in percentage")
    taper: float = Field(description="Rate of inflation reduction per epoch")
    foundation: float = Field(description="Foundation inflation rate percentage")
    foundationTerm: float = Field(description="Duration in years of foundation pool inflation")


class SolanaInflationGovernorResponse(BaseModel):
    """Response model for inflation governor queries"""
    status: str
    governor: Optional[SolanaInflationGovernor] = Field(None, description="Inflation governor parameters")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaInflationRate(BaseModel):
    """Model for inflation rate information"""
    total: float = Field(description="Total inflation percentage")
    validator: float = Field(description="Inflation allocated to validators percentage")
    foundation: float = Field(description="Inflation allocated to Solana Foundation percentage")
    epoch: int = Field(description="Epoch for which the inflation rate is valid")


class SolanaInflationRateResponse(BaseModel):
    """Response model for inflation rate queries"""
    status: str
    inflation: Optional[SolanaInflationRate] = Field(None, description="Current inflation rate")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaInflationRewardItem(BaseModel):
    """Model for inflation reward item"""
    epoch: int = Field(description="The epoch in which the reward was distributed")
    effectiveSlot: int = Field(description="The effective slot in which the reward was distributed")
    amount: int = Field(description="Reward amount in lamports")
    postBalance: int = Field(description="Post balance of the account in lamports")
    commission: Optional[int] = Field(None, description="Vote account commission when the reward was distributed")


class SolanaInflationRewardResponse(BaseModel):
    """Response model for inflation reward queries"""
    status: str
    rewards: Optional[List[Optional[SolanaInflationRewardItem]]] = Field(None, description="List of inflation rewards, can contain None if an address is not found")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaLargeAccount(BaseModel):
    """Model for large account information"""
    address: str = Field(description="Account address as base-58 encoded string")
    lamports: int = Field(description="Balance in lamports")


class SolanaLargestAccountsResponse(BaseModel):
    """Response model for largest accounts queries"""
    status: str
    accounts: Optional[List[SolanaLargeAccount]] = Field(None, description="List of largest accounts")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaBlockhashInfo(BaseModel):
    """Model for blockhash information"""
    blockhash: str = Field(description="The blockhash as base-58 encoded string")
    lastValidBlockHeight: int = Field(description="Last valid block height for this blockhash")


class SolanaLatestBlockhashResponse(BaseModel):
    """Response model for latest blockhash queries"""
    status: str
    value: Optional[SolanaBlockhashInfo] = Field(None, description="Latest blockhash information")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaLeaderScheduleResponse(BaseModel):
    """Response model for leader schedule queries"""
    status: str
    schedule: Optional[Dict[str, List[int]]] = Field(None, description="Leader schedule as a map of validator identity pubkeys to their assigned slots")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaMaxRetransmitSlotResponse(BaseModel):
    """Response model for max retransmit slot queries"""
    status: str
    maxRetransmitSlot: Optional[int] = Field(None, description="Maximum slot that was retransmitted by the node")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaMaxShredInsertSlotResponse(BaseModel):
    """Response model for max shred insert slot queries"""
    status: str
    maxShredInsertSlot: Optional[int] = Field(None, description="Highest slot where shreds have been inserted")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaMinimumBalanceForRentExemptionResponse(BaseModel):
    """Response model for minimum balance for rent exemption queries"""
    status: str
    lamports: Optional[int] = Field(None, description="Minimum balance in lamports to be exempt from rent")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaMultipleAccountsResponse(BaseModel):
    """Response model for multiple accounts queries"""
    status: str
    value: Optional[List[Optional[SolanaAccountData]]] = Field(None, description="List of account information, can contain None if an address is not found")
    context: Optional[Dict] = Field(None, description="RPC response context")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaProgramAccount(BaseModel):
    """Model for program account information"""
    pubkey: str = Field(description="Account public key as base-58 encoded string")
    account: SolanaAccountData = Field(description="Account data")


class SolanaProgramAccountsResponse(BaseModel):
    """Response model for program accounts queries"""
    status: str
    accounts: Optional[List[SolanaProgramAccount]] = Field(None, description="List of program accounts")
    context: Optional[Dict] = Field(None, description="RPC response context if withContext was true")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaPerformanceSample(BaseModel):
    """Model for performance sample data"""
    slot: int = Field(description="Slot in which sample was taken")
    numTransactions: int = Field(description="Number of transactions in sample")
    numSlots: int = Field(description="Number of slots in sample")
    samplePeriodSecs: int = Field(description="Number of seconds in a sample window")


class SolanaRecentPerformanceSamplesResponse(BaseModel):
    """Response model for recent performance samples queries"""
    status: str
    samples: Optional[List[SolanaPerformanceSample]] = Field(None, description="List of recent performance samples")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error")


class SolanaPrioritizationFee(BaseModel):
    """Model for prioritization fee data"""
    slot: int = Field(description="Slot in which the fee was observed")
    prioritizationFee: int = Field(description="The per-compute-unit fee paid by at least one successfully landed transaction, specified in increments of micro-lamports (0.000001 lamports)")


class SolanaRecentPrioritizationFeesResponse(BaseModel):
    """Response model for recent prioritization fees queries"""
    status: str
    fees: Optional[List[SolanaPrioritizationFee]] = Field(None, description="List of recent prioritization fees")
    message: Optional[str] = Field(None, description="Error message if status is error")
    error: Optional[dict] = Field(None, description="Error details if status is error") 