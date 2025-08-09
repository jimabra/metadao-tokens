from solders.pubkey import Pubkey

AUTOCRAT_IDL = {
    Pubkey.from_string("meta3cxKzFBmWYgCVozmvCQAS3y9b3fGxrG9HkHL7Wi") : "autocrat_v0.json",
    Pubkey.from_string("metaX99LHn3A7Gr7VAcCfXhpfocvpMpqQ3eyp3PGUUq") : "autocrat_v1.json",
    Pubkey.from_string("metaRK9dUBnrAdZN6uUDKvxBVKW5pyCbPVmLtUZwtBp") : "autocrat_v2.json",
    Pubkey.from_string("autoQP9RmUNkzzKRXsMkWicDVZ3h29vvyMDcAYjCxxg") : "autocrat_v3.json",
    Pubkey.from_string("autowMzCbM29YXMgVG3T62Hkgo7RcyrvgQQkd54fDQL") : "autocrat_v4.json",
    Pubkey.from_string("auToUr3CQza3D4qreT6Std2MTomfzvrEeCC5qh7ivW5") : "autocrat_v5.json"
}

AUTOCRAT_INIT_PROP_ACCOUNT_COUNT = {
    Pubkey.from_string("meta3cxKzFBmWYgCVozmvCQAS3y9b3fGxrG9HkHL7Wi") : 11,
    Pubkey.from_string("metaX99LHn3A7Gr7VAcCfXhpfocvpMpqQ3eyp3PGUUq") : 11,
    Pubkey.from_string("metaRK9dUBnrAdZN6uUDKvxBVKW5pyCbPVmLtUZwtBp") : 11,
    Pubkey.from_string("autoQP9RmUNkzzKRXsMkWicDVZ3h29vvyMDcAYjCxxg") : 15,
    Pubkey.from_string("autowMzCbM29YXMgVG3T62Hkgo7RcyrvgQQkd54fDQL") : 18,
    Pubkey.from_string("auToUr3CQza3D4qreT6Std2MTomfzvrEeCC5qh7ivW5") : 21
}

AUTOCRAT_ACCOUNT_INDEX_NAMES = ["proposal", "quote_vault", "base_vault", "pass_amm_lp_mint", "fail_amm_lp_mint"]
AUTOCRAT_ACCOUNT_INDEX = {
    Pubkey.from_string("meta3cxKzFBmWYgCVozmvCQAS3y9b3fGxrG9HkHL7Wi") : [0, 3, 4],
    Pubkey.from_string("metaX99LHn3A7Gr7VAcCfXhpfocvpMpqQ3eyp3PGUUq") : [0, 3, 4],
    Pubkey.from_string("metaRK9dUBnrAdZN6uUDKvxBVKW5pyCbPVmLtUZwtBp") : [0, 3, 4],
    Pubkey.from_string("autoQP9RmUNkzzKRXsMkWicDVZ3h29vvyMDcAYjCxxg") : [0, 2, 3, 5, 6],
    Pubkey.from_string("autowMzCbM29YXMgVG3T62Hkgo7RcyrvgQQkd54fDQL") : [0, 3, 4, 6, 7],
    Pubkey.from_string("auToUr3CQza3D4qreT6Std2MTomfzvrEeCC5qh7ivW5") : [0, 4, 5, 7, 8]
}

VAULT_IDL = {
    Pubkey.from_string("vaU1tVLj8RFk7mNj1BxqgAsMKKaL8UvEUHvU3tdbZPe") : "vault_v0.json",
    Pubkey.from_string("vAuLTQjV5AZx5f3UgE75wcnkxnQowWxThn1hGjfCVwP") : "vault_v0.json", # weird undocumented vault_v2
    Pubkey.from_string("VAU1T7S5UuEHmMvXtXMVmpEoQtZ2ya7eRb7gcN47wDp") : "vault_v3.json",
    Pubkey.from_string("VLTX1ishMBbcX3rdBWGssxawAo1Q2X2qxYFYqiGodVg") : "vault_v4.json",
}

AMM_IDL = {
    Pubkey.from_string("AMM5G2nxuKUwCLRYTW7qqEwuoqCtNSjtbipwEmm2g8bH") : "amm_v3.json",
    Pubkey.from_string("AMMyu265tkBpRW21iGQxKGLaves3gKm2JcMUqfXNSpqD") : "amm_v4.json",
    Pubkey.from_string("AMMJdEiCCa8mdugg6JPF7gFirmmxisTfDJoSNSUi5zDJ") : "amm_v5.json"
}

LAUNCHPAD_IDL = {
    Pubkey.from_string("AfJJJ5UqxhBKoE3grkKAZZsoXDE9kncbMKvqSHGsCNrE") : "launchpad_v4.json",
    Pubkey.from_string("mooNhciQJi1LqHDmse2JPic2NqG2PXCanbE3ZYzP3qA") : "launchpad_v5.json"
}