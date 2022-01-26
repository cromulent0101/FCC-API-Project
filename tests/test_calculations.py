import sys
import pytest
sys.path.append(".") # include parent directory in path
from app import calculations

@pytest.fixture
def zero_bank_account():
    return calculations.BankAccount()

@pytest.fixture
def bank_account():
    return calculations.BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (-1,-1,-2),
    (0,199999999999,199999999999),
    (0.0001,4.9999,5)
])
def test_add(num1,num2,expected):
    print("testing add function")
    sum = calculations.add(num1,num2)
    assert sum == expected

def test_subtract():
    assert calculations.subtract(13,8)==5

def test_multiply():
    assert calculations.multiply(13,8)==104

def test_divide():
    assert calculations.divide(24,8)==3

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55

@pytest.mark.parametrize("deposited, withdrew, expected",[
    (200,100,100),
    (1000,1,999)
])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(calculations.InsufficientFunds):
        bank_account.withdraw(200)

# test_add()
# test_subtract()
# test_multiply()
# test_divide()