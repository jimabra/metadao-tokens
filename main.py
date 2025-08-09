from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import ENDPOINT
from solana.rpc.types import DataSliceOpts, MemcmpOpts
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from anchorpy import Program, Idl, Provider, Wallet
from pathlib import Path
import asyncio
import json

from constants import VAULT_IDL, AMM_IDL

# constant offset for AMM v3-v5
AMM_LP_MINT_OFFSET = 8+1+8
AMM_LP_SLICE = DataSliceOpts(offset=AMM_LP_MINT_OFFSET, length=32)

def get_program(program_id: Pubkey, provider: Provider, idl_path: Path):
    raw = idl_path.read_text()
    idl = Idl.from_json(raw)
    return Program(
        program_id=program_id,
        provider=provider,
        idl=idl
    )

async def get_amm_program_lp_mints(amm_program_id: Pubkey, connection: AsyncClient, program_map: dict[Pubkey, Program]):
    discriminator = program_map[amm_program_id].coder.accounts.acc_name_to_discriminator["Amm"]
    filters = [MemcmpOpts(offset=0, bytes=discriminator)]
    out = await connection.get_program_accounts(amm_program_id, data_slice=AMM_LP_SLICE, filters=filters)
    return [{"amm": str(acc.pubkey), "lp_mint": str(Pubkey.from_bytes(acc.account.data))} for acc in out.value]

async def get_vault_program_conditional_mints(vault_program_id: Pubkey, connection: AsyncClient, program_map: dict[Pubkey, Program]):
    all_vault_mints = []
    discriminator = program_map[vault_program_id].coder.accounts.acc_name_to_discriminator["ConditionalVault"]
    filters = [MemcmpOpts(offset=0, bytes=discriminator)]
    out = await connection.get_program_accounts(vault_program_id, encoding="jsonParsed", filters=filters)
    for acc in out.value:
        vault_program = program_map[acc.account.owner]
        vault_data = vault_program.coder.accounts.decode(acc.account.data)
        try:
            pass_mint = vault_data.conditional_on_finalize_token_mint
            fail_mint = vault_data.conditional_on_revert_token_mint
            result = {"vault": str(acc.pubkey), "pass_mint": str(pass_mint), "fail_mint": str(fail_mint)}
        except AttributeError:
            result = {"vault": str(acc.pubkey)}
            result.update({f"conditional_{i}_mint" : str(mint) for i, mint in enumerate(vault_data.conditional_token_mints)})
        all_vault_mints.append(result)
    return all_vault_mints

def write_output(data, slot):
    json_output = json.dumps(data, indent=2)
    with open('result/proposal_mints.json', 'w') as f:
        f.write(json_output)

    with open("result/all_mints.txt", 'w') as f:
        for item in data:
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
    for id, idl in {**VAULT_IDL, **AMM_IDL}.items():
        program_map[id] = get_program(id, provider, Path(f"idls/{idl}"))

    data = []
    for key in AMM_IDL:
        out = await get_amm_program_lp_mints(key, connection, program_map)
        data.extend(out)

    for key in VAULT_IDL:
        out = await get_vault_program_conditional_mints(key, connection, program_map)
        data.extend(out)

    slot = (await connection.get_slot()).value
    write_output(data, slot)

if __name__ == "__main__":
    asyncio.run(main())