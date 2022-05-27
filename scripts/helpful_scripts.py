from brownie import network, config, accounts, Contract, LinkToken, VRFCoordinatorMock
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache-local",
    "mainnet-fork",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the config
    if defined, otherwise it will deploy a mock version of this contract
    and return the mock contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying mock link token...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx
