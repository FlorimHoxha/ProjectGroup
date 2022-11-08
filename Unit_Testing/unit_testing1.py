from example1_test import add_two_numbers

# def test_add_two_whole_numbers():
#     expected = 10
#     actual = add_two_numbers(5 , 5)
#     assert expected == actual
#     print("Test is successsful")
# test_add_two_whole_numbers()    


# def test_positive_to_negative_whole_numbers():
#     expected = 10
#     actual = add_two_numbers(5 , -5)
#     assert expected == actual
#     print("Test is successsful")
# test_positive_to_negative_whole_numbers()

# def test_two_float_numbers():
#     expected = 10
#     actual = add_two_numbers(5.0 , 5.0)
#     assert expected == actual
#     print("Test is successsful")
# test_two_float_numbers()

# def test_string_and_whole_numbers():
#     expected = 10
#     actual = add_two_numbers("String", 5)
#     assert expected == actual
#     print("Test is successsful")
# test_positive_to_negative_whole_numbers()

def test__two_strings():
    expected = ("String1String2")
    actual = add_two_numbers("String1", "String2")
    assert expected == actual
    print("Test is successsful")
test__two_strings()
