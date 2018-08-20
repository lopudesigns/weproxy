# -*- coding: utf-8 -*-
import json


import pytest


req = {"id": 1, "jsonrpc": "2.0", "method": "get_dynamic_global_properties"}

expected_eznode_response = {
    "id": "1",
    "result": {
        "average_block_size": 16112,
        "confidential_EUSD_supply": "0.000 EUSD",
        "confidential_supply": "0.000 ECO",
        "current_aslot": 19615022,
        "current_reserve_ratio": 1243817,
        "current_EUSD_supply": "8016379.428 EUSD",
        "current_supply": "263590437.017 ECO",
        "current_witness": "good-karma",
        "head_block_id": "012a58ebf2e150d2200da72acff4c6b272915e08",
        "head_block_number": 19552491,
        "id": 0,
        "last_irreversible_block_num": 19552476,
        "max_virtual_bandwidth": "1643338184785920000",
        "maximum_block_size": 65536,
        "num_pow_witnesses": 172,
        "participation_count": 128,
        "pending_rewarded_ESCOR": "298814345.817945 ESCOR",
        "pending_rewarded_ESCORvalueInECO": "145258.167 ECO",
        "recent_slots_filled": "340282366920938463463374607431768211455",
        "EUSD_interest_rate": 0,
        "EUSD_print_rate": 10000,
        "time": "2018-02-03T17:51:06",
        "total_pow": 514415,
        "total_ESCOR_reward_fund_ECO": "0.000 ECO",
        "total_ESCORreward2": "0",
        "total_ESCOR_fund_in_ECO": "195640068.504 ECO",
        "totalESCOR": "400228023408.017941 ESCOR",
        "virtual_supply": "265290623.534 ECO",
        "vote_power_reserve_rate": 10
    }
}


expected_response = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "average_block_size": 16112,
        "confidential_EUSD_supply": "0.000 EUSD",
        "confidential_supply": "0.000 ECO",
        "current_aslot": 19615022,
        "current_reserve_ratio": 1243817,
        "current_EUSD_supply": "8016379.428 EUSD",
        "current_supply": "263590437.017 ECO",
        "current_witness": "good-karma",
        "head_block_id": "012a58ebf2e150d2200da72acff4c6b272915e08",
        "head_block_number": 19552491,
        "id": 0,
        "last_irreversible_block_num": 19552476,
        "max_virtual_bandwidth": "1643338184785920000",
        "maximum_block_size": 65536,
        "num_pow_witnesses": 172,
        "participation_count": 128,
        "pending_rewarded_ESCOR": "298814345.817945 ESCOR",
        "pending_rewarded_ESCORvalueInECO": "145258.167 ECO",
        "recent_slots_filled": "340282366920938463463374607431768211455",
        "EUSD_interest_rate": 0,
        "EUSD_print_rate": 10000,
        "time": "2018-02-03T17:51:06",
        "total_pow": 514415,
        "total_ESCOR_reward_fund_ECO": "0.000 ECO",
        "total_ESCORreward2": "0",
        "total_ESCOR_fund_in_ECO": "195640068.504 ECO",
        "totalESCOR": "400228023408.017941 ESCOR",
        "virtual_supply": "265290623.534 ECO",
        "vote_power_reserve_rate": 10
    }
}


@pytest.mark.live
async def test_cache_response_middleware(test_cli):
    response = await test_cli.post('/', json=req)
    assert await response.json() == expected_eznode_response
    response = await test_cli.post('/', json=req)
    assert response.headers['x-jussi-cache-hit'] == 'eznode.database_api.get_dynamic_global_properties'


async def test_mocked_cache_response_middleware(mocked_app_test_cli):
    mocked_ws_conn, test_cli = mocked_app_test_cli
    mocked_ws_conn.recv.return_value = json.dumps(expected_response)
    response = await test_cli.post('/', json=req, headers={'x-jussi-request-id': '1'})
    assert 'x-jussi-cache-hit' not in response.headers
    assert await response.json() == expected_response

    response = await test_cli.post('/', json=req, headers={'x-jussi-request-id': '1'})
    assert response.headers['x-jussi-cache-hit'] == 'eznode.database_api.get_dynamic_global_properties'
    assert await response.json() == expected_response
