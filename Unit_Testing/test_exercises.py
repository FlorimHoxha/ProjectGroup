from exercises import get_country_code, get_country_currency, get_country_currency_2

def mock_get_country_code():
    fake_countries_list = [
        {
            "name": "United Kingdom of Great Britain and Northern Ireland",
            "alpha3Code": "GBP"
        }
    ]
    return fake_countries_list

def test_get_country_code():
    # assemble
    expected = "GBP"

    # act
    result = get_country_code(
        mock_get_country_code,
        "United Kingdom of Great Britain and Northern Ireland"
    )

    # assert
    assert expected == result
    print("test passed")



def mock_get_country_currency():
    fake_countries_list = [
        {
            "name": "United Kingdom of Great Britain and Northern Ireland",
            "currencies": [{'code': 'GBP', 'name': 'British pound', 'symbol': '£'}]
        }
    ]
    return fake_countries_list

def test_get_country_currencies():
    # assemble
    expected = "GBP"

    # act
    result = get_country_currency(
        mock_get_country_currency,
        "United Kingdom of Great Britain and Northern Ireland"
    )

    # assert
    assert expected == result
    print("test passed")

test_get_country_code()
test_get_country_currencies()

def test_get_country_currencies_2():
    # assemble
    expected = "AFN"

    fake_countries_list = [
        {
            "name": "United Kingdom of Great Britain and Northern Ireland",
            "currencies": [{'code': 'GBP', 'name': 'British pound', 'symbol': '£'}]

        },
        {
            "name": "Afganista",
            "currencies": [{'code': 'AFN', 'name': 'Afghan afghani', 'symbol': '؋'}]

        }
    ]

    # act
    result = get_country_currency_2(
        fake_countries_list,
        "Afganistan"
    )

    # assert
    assert expected == result
    print("test passed test_get_country_currencies2")
test_get_country_currencies_2()