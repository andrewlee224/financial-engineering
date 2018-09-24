import pytest

import binomial


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

    assert price == 2.604077132966553
    assert early_exercise == 15


def test_american_put_k110(binomial_model):
    price, early_exercise = binomial_model.american_option(k=110, call=False)

    assert price == 12.359784797284911
    assert early_exercise == 5


if __name__ == '__main__':
    pytest.main()
