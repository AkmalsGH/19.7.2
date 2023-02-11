from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_age
import os

pf = PetFriends()


# Тест №1
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    status = pf.get_api_key(email, password)
    assert status != 200

# Тест №2
def test_get_api_key_for_invalid_user(email=valid_email, password='123'):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

# Тест №3
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


# Тест №4
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боб", "собака", '1', "images/husky.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# Тест №5
def test_successful_update_self_pet_info(name='Федя', animal_type='лев', age='11'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    else:
        raise Exception("There is no my pets")

# Тест №6
def test_add_new_pet_no_photo_with_valid_data(name='Барсик', animal_type='cat', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''

# Тест №7
def test_add_new_pet_without_name(name='', animal_type='cat', age='2',
                                  pet_photo='images/cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

#Тест №8
def test_add_new_pet_without_photo(name='Барсик', animal_type='cat', age='2',
                                   pet_photo = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
    except TypeError:
        print('Нельзя добавить питомца без фото!')

#Тест №9
def test_add_new_pet_with_invalid_animal_type(name='Тузик', animal_type=12345, age='2',
                                              pet_photo='images/husky.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверный формат породы. Питомец не добавлен!')

#Тест №10
def test_add_new_pet_with_invalid_age(name='', animal_type='Кот',
                                      age='invalid_age', pet_photo='images/cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200