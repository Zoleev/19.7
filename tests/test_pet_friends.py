from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Barbos', animal_type='dog', age='2', pet_photo='images\Moloko.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Lacky', 'dog', '2', 'images/Moloko.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Pop', animal_type='pit', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert len(my_pets['pets']) > 0, 'В профиле учетной записи отсутсвуют сведения о питомцах'
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_wo_photo_valid_data(name='None', animal_type='dog', age='1'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''


def test_add_photo_of_pet(pet_photo='images\Bigdog.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')


    assert len(my_pets['pets']) > 0, 'В профиле учетной записи отсутсвуют сведения о питомцах'
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] is not ''


def test_01_get_status_for_invalid_password(email=valid_email, password=invalid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    print(result)


def test_02_get_status_for_invalid_email(email=invalid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    print(result)


def test_03_get_status_for_empty_reg_fields(email='', password=''):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    print(result)


def test_04_add_new_pet_wo_photo_big_age(name='Roger', animal_type='buldog', age='100500'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['age'] != 0


def test_05_add_new_pet_wo_photo_negative_age(name='Minus', animal_type='dog', age='-3'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['age'] != 0


def test_06_add_new_pet_wo_photo_zero_age(name='Max', animal_type='dog', age=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['age'] is ''


def test_07_add_new_pet_wo_photo_alphabet_age(name='Tosha', animal_type='dog', age='mo'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['age'] is not ''


def test_08_add_new_pet_wo_photo_digi_breed(name='Proton', animal_type='123', age='6'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] is not ''


def test_09_add_new_pet_without_text_field(name='', animal_type='', age='', pet_photo='images/Moloko.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is not ''


def test_10_add_new_empty_pet(name='', animal_type='', age=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age