import pytest

import binomial
import npv
import mortgage


DIGITS_PRECISION = 9


@pytest.fixture()
def binomial_model():
    T = .25
    S0 = 100
    r = 2e-2
    sigma = 30e-2
    c = 1e-2
    n = 15

    dp = binomial.convert_to_discrete(T, S0, r, sigma, c, n)

    return binomial.BinomialModel(dp.S0, dp.u_n, dp.d_n, dp.q_n, dp.R_n, dp.n)


def test_american_call_k110(binomial_model):
    price, early_exercise = binomial_model.american_option(k=110, call=True)

    assert round(price, DIGITS_PRECISION) == 2.604077133
    assert early_exercise == 15


def test_american_put_k110(binomial_model):
    price, early_exercise = binomial_model.american_option(k=110, call=False)

    assert round(price, DIGITS_PRECISION) == 12.359784797
    assert early_exercise == 5


def test_discount():
    assert npv.discount(0.05, 2) == pytest.approx(0.90703)


def test_npv():
    assert npv.npv(10000, 0.025, 10) == pytest.approx(7811.98401)


def test_mortgage_payment():
    assert mortgage.payment(
        150000, 0.04 / 12, 5 * 12) == pytest.approx(2762.4783)


if __name__ == '__main__':
    pytest.main()
