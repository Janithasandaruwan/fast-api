from app.calculations import add, BankAccount, InsufficientFunds
import pytest


@pytest.mark.parametrize("num1, num2, res", [(2,2,4),(5,4,9), (2,7,9)])
def test_add(num1, num2, res):
    print("Testing........")
    assert add(num1, num2) == res

@pytest.fixture()
def zero_bank_account():
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(100)


def test_bank_amount(zero_bank_account):
    #bank_account = BankAccount(100)
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    #bank_account = BankAccount(100)
    bank_account.withdraw(50)
    assert bank_account.balance == 50

def test_deposit(bank_account):
    #bank_account = BankAccount(100)
    bank_account.deposit(50)
    assert bank_account.balance == 150

def test_interest(bank_account):
    #bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 110

@pytest.mark.parametrize("deposit, withdraw, balance", [(200,100,100),(500,200,300), (800,200,600)])
def test_bank_transaction(zero_bank_account,deposit, withdraw, balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance

def test_insufficient_funds(bank_account):
    #Pytest expecting a exception
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)



