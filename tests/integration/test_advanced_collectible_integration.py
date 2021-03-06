from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import time
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_simple_collectible_integrations():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integrration testing")
    # Act
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(60)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
