from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import ENDPOINT
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from anchorpy import Program, Idl, Provider, Wallet
from pathlib import Path
import asyncio
import based58
import json

from constants import AUTOCRAT_IDL, AUTOCRAT_INIT_PROP_ACCOUNT_COUNT, AUTOCRAT_ACCOUNT_INDEX_NAMES, AUTOCRAT_ACCOUNT_INDEX, VAULT_IDL, AMM_IDL

def get_program(program_id: Pubkey, provider: Provider, idl_path: Path):
    raw = idl_path.read_text()
    idl = Idl.from_json(raw)
    return Program(
        program_id=program_id,
        provider=provider,
        idl=idl
    )

def get_mints_from_vault_account(vault_account, program_map):
    vault_program = program_map[vault_account.owner]
    vault_data = vault_program.coder.accounts.decode(vault_account.data)
    try:
        pass_mint = vault_data.conditional_on_finalize_token_mint
        fail_mint = vault_data.conditional_on_revert_token_mint
        return pass_mint, fail_mint
    except AttributeError:
        return vault_data.conditional_token_mints

async def get_proposal_mints_from_ix(accs, autocrat_ix, autocrat_key, program_map, connection):
    data_bytes = based58.b58decode(bytes(autocrat_ix.data, encoding="utf-8"))
    init_proposal = False
    try:
        parsed_ix = program_map[autocrat_key].coder.instruction.parse(data_bytes)
        if parsed_ix.name == "initialize_proposal":
            init_proposal = True
    except:
        # handle unparsable garbage
        if len(autocrat_ix.accounts) == AUTOCRAT_INIT_PROP_ACCOUNT_COUNT[autocrat_key]: # should be limited to init proposal ixs
            init_proposal = True
        
    if not init_proposal:
        return

    result = {name : accs[autocrat_ix.accounts[i]] for name, i in zip(AUTOCRAT_ACCOUNT_INDEX_NAMES, AUTOCRAT_ACCOUNT_INDEX[autocrat_key])}

    vault_accounts_resp = await connection.get_multiple_accounts([result["quote_vault"], result["base_vault"]])

    quote_mints = get_mints_from_vault_account(vault_accounts_resp.value[0], program_map)
    if len(quote_mints) == 2:
        result["quote_pass_mint"], result["quote_fail_mint"] = quote_mints
    else:
        for i, mint in enumerate(quote_mints):
            result[f"quote_mint_{i}"] = mint

    base_mints = get_mints_from_vault_account(vault_accounts_resp.value[1], program_map)
    if len(base_mints) == 2:
        result["base_pass_mint"], result["base_fail_mint"] = base_mints
    else:
        for i, mint in enumerate(base_mints):
            result[f"base_mint_{i}"] = mint

    del result["quote_vault"]
    del result["base_vault"]
    return result

async def get_proposal_mints_from_txs(txs, autocrat_key, program_map, connection):
    fetched_proposal_mints = []
    for tx in txs:
        accs = tx.value.transaction.transaction.message.account_keys
        if autocrat_key not in accs:
            continue
        autocrat_account_index = accs.index(autocrat_key)
        accs.extend(tx.value.transaction.meta.loaded_addresses.writable)
        accs.extend(tx.value.transaction.meta.loaded_addresses.readonly)
        ixs = tx.value.transaction.transaction.message.instructions
        autocrat_ixs = [ix for ix in ixs if ix.program_id_index == autocrat_account_index]

        if not autocrat_ixs:
            continue

        for autocrat_ix in autocrat_ixs:
            proposal_mints = await get_proposal_mints_from_ix(accs, autocrat_ix, autocrat_key, program_map, connection)
            if proposal_mints is not None:
                fetched_proposal_mints.append(proposal_mints)
                
    return fetched_proposal_mints

def write_output(data, slot):
    processed_data = []
    for item in data:
        string_item = {key: str(value) for key, value in item.items()}
        processed_data.append(string_item)
    json_output = json.dumps(processed_data, indent=2)
    with open('result/proposal_mints.json', 'w') as f:
        f.write(json_output)

    with open("result/all_mints.txt", 'w') as f:
        for item in processed_data:
            for key, value in item.items():
                if key.endswith("mint"):
                    f.write(value + '\n')

    with open("result/context_slot.txt", "w") as f:
        f.write(str(slot))

async def main():
    url = ENDPOINT.https.mainnet_beta
    connection = AsyncClient(url)

    provider = Provider(connection, Wallet(Keypair.from_seed([0] * 32)))
    program_map : dict[Pubkey, Program] = dict()
    for id, idl in {**AUTOCRAT_IDL, **VAULT_IDL, **AMM_IDL}.items():
        program_map[id] = get_program(id, provider, Path(f"idls/{idl}"))

    data = []
    for autocrat_key in AUTOCRAT_IDL.keys():
        sigs_resp = await connection.get_signatures_for_address(autocrat_key)
        success_txs = [sig_resp for sig_resp in sigs_resp.value if sig_resp.err is None]
        txs = [await connection.get_transaction(sig_resp.signature, max_supported_transaction_version=0) for sig_resp in success_txs]
        mints_data = await get_proposal_mints_from_txs(txs, autocrat_key, program_map, connection)
        data.extend(mints_data)

    slot = (await connection.get_slot()).value
    write_output(data, slot)

if __name__ == "__main__":
    asyncio.run(main())