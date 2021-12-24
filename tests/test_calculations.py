import app

def test_add():
    print("testing add function")
    sum = app.calculations.add(13,8)
    assert sum == 21


test_add()