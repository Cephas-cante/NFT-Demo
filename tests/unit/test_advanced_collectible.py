from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_simple_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Act
    advanced_collectible, creating_tx = deploy_and_create()
    requestId = creating_tx.events["requestCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdBreed(0) == random_number % 3
