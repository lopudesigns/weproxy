# -*- coding: utf-8 -*-
import json


import pytest


req = {"id": 1, "jsonrpc": "2.0", "method": "get_dynamic_global_properties"}

expected_node_response = {
    "id": "1",
    "result": {
        "average_block_size": 16112,
        "confidential_TSD_supply": "0.000 TSD",
        "confidential_supply": "0.000 TME",
        "current_aslot": 19615022,
        "current_reserve_ratio": 1243817,
        "current_TSD_supply": "8016379.428 TSD",
        "current_supply": "263590437.017 TME",
        "current_witness": "good-karma",
        "head_block_id": "012a58ebf2e150d2200da72acff4c6b272915e08",
        "head_block_number": 19552491,
        "id": 0,
        "last_irreversible_block_num": 19552476,
        "max_virtual_bandwidth": "1643338184785920000",
        "maximum_block_size": 65536,
        "num_pow_witnesses": 172,
        "participation_count": 128,
        "pending_rewarded_SCORE": "298814345.817945 SCORE",
        "pending_rewarded_SCOREvalueInTME": "145258.167 TME",
        "recent_slots_filled": "340282366920938463463374607431768211455",
        "TSD_interest_rate": 0,
        "TSD_print_rate": 10000,
        "time": "2018-02-03T17:51:06",
        "total_pow": 514415,
        "totalSCORE_reward_fund_TME": "0.000 TME",
        "totalSCOREreward2": "0",
        "totalTMEfundForSCORE": "195640068.504 TME",
        "totalSCORE": "400228023408.017941 SCORE",
        "virtual_supply": "265290623.534 TME",
        "vote_power_reserve_rate": 10
    }
}


expected_response = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "average_block_size": 16112,
        "confidential_TSD_supply": "0.000 TSD",
        "confidential_supply": "0.000 TME",
        "current_aslot": 19615022,
        "current_reserve_ratio": 1243817,
        "current_TSD_supply": "8016379.428 TSD",
        "current_supply": "263590437.017 TME",
        "current_witness": "good-karma",
        "head_block_id": "012a58ebf2e150d2200da72acff4c6b272915e08",
        "head_block_number": 19552491,
        "id": 0,
        "last_irreversible_block_num": 19552476,
        "max_virtual_bandwidth": "1643338184785920000",
        "maximum_block_size": 65536,
        "num_pow_witnesses": 172,
        "participation_count": 128,
        "pending_rewarded_SCORE": "298814345.817945 SCORE",
        "pending_rewarded_SCOREvalueInTME": "145258.167 TME",
        "recent_slots_filled": "340282366920938463463374607431768211455",
        "TSD_interest_rate": 0,
        "TSD_print_rate": 10000,
        "time": "2018-02-03T17:51:06",
        "total_pow": 514415,
        "totalSCORE_reward_fund_TME": "0.000 TME",
        "totalSCOREreward2": "0",
        "totalTMEfundForSCORE": "195640068.504 TME",
        "totalSCORE": "400228023408.017941 SCORE",
        "virtual_supply": "265290623.534 TME",
        "vote_power_reserve_rate": 10
    }
}


@pytest.mark.live
async def test_cache_response_middleware(test_cli):
    response = await test_cli.post('/', json=req)
    assert await response.json() == expected_node_response
    response = await test_cli.post('/', json=req)
    assert response.headers['x-jussi-cache-hit'] == 'node.database_api.get_dynamic_global_properties'


async def test_mocked_cache_response_middleware(mocked_app_test_cli):
    mocked_ws_conn, test_cli = mocked_app_test_cli
    mocked_ws_conn.recv.return_value = json.dumps(expected_response)
    response = await test_cli.post('/', json=req, headers={'x-jussi-request-id': '1'})
    assert 'x-jussi-cache-hit' not in response.headers
    assert await response.json() == expected_response

    response = await test_cli.post('/', json=req, headers={'x-jussi-request-id': '1'})
    assert response.headers['x-jussi-cache-hit'] == 'node.database_api.get_dynamic_global_properties'
    assert await response.json() == expected_response
