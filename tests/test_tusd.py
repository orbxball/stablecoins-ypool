# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")
from brownie import Wei, reverts
from useful_methods import genericStateOfVault, genericStateOfStrat
import brownie

def test_tusd(Vault, StrategyTUSDypool, tusd_whale, gov, tusd):
    # deploy tusd vault
    tusd_vault = gov.deploy(Vault, tusd, gov, gov, '', '')
    print(f'type of vault: {type(tusd_vault)} @ {tusd_vault}')

    # deploy tusd strategy
    tusd_strategy = gov.deploy(StrategyTUSDypool, tusd_vault)
    print(f'type of strategy: {type(tusd_strategy)} @ {tusd_strategy}')

    # activate the strategy from vault view
    tusd_vault.addStrategy(tusd_strategy, 2**64, 2**64, 1000, {'from': gov})
    print(f'credit of strategy: {tusd_vault.creditAvailable(tusd_strategy)}')

    # rm yvtusd's guestlist
    tusd_vault.setGuestList('0x0000000000000000000000000000000000000000', {'from': gov})
    print(f'yvtusd guest list: {tusd_vault.guestList()}')

    # approve tusd vault to use tusd
    tusd.approve(tusd_vault, 2**256-1, {'from': tusd_whale})

    # start deposit
    print('\n=== deposit 100 tusd ===')
    print(f'whale\'s tusd balance before deposit: {tusd.balanceOf(tusd_whale)/1e18}')
    deposit_amount = Wei('100 ether')
    tusd_vault.deposit(deposit_amount, {'from': tusd_whale})
    print(f'whale\'s tusd balance  after deposit: {tusd.balanceOf(tusd_whale)/1e18}')

    # start strategy
    print('\n=== harvest tusd ===')
    tusd_strategy.harvest({'from': gov})
    print('harvest done')

    print('\n=== tusd status ===')
    genericStateOfStrat(tusd_strategy, tusd, tusd_vault)
    genericStateOfVault(tusd_vault, tusd)

    # withdraw
    print('\n=== withdraw tusd ===')
    print(f'whale\'s tusd vault share: {tusd_vault.balanceOf(tusd_whale)/1e18}')
    tusd_vault.withdraw(Wei('1 ether'), {'from': tusd_whale})
    print(f'withdraw 1 share of tusd done')
    print(f'whale\'s tusd vault share: {tusd_vault.balanceOf(tusd_whale)/1e18}')
    
    # withdraw all
    print('\n=== withdraw all tusd ===')
    print(f'whale\'s tusd vault share: {tusd_vault.balanceOf(tusd_whale)/1e18}')
    tusd_vault.withdraw({'from': tusd_whale})
    print(f'withdraw all tusd')
    print(f'whale\'s tusd vault share: {tusd_vault.balanceOf(tusd_whale)/1e18}')

    # call tend
    print('\ncall tend')
    tusd_strategy.tend()
    print('tend done')

