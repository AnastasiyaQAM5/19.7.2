from api import PetFriends
from settings import *


class TestPetFriends:
    def setup_method(self):
        self.pf = PetFriends()

    def test_get_API_keyForValidUser(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_getAllPetsWithValidKey(self, filter=''):  # filter available values : my_pets
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_addNewPetWithValidData(self, name='Барбоскин', animal_type='двортерьер', age='4',
                                    pet_photo='tests/image/1200px-Stray_kitten_Rambo002.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successfulDeleteSelfPet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "tests/image/1200px-Stray_kitten_Rambo002.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = myPets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in myPets.values()

    def test_successfulUpdateSelfPetInfo(self, name='Мурзик', animal_type='Котэ', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    # test for new methods

    def test_CreatePetSimple(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.create_pet_simple(auth_key, "simple", "new", "3")

        assert status == 200

    def test_SetPhoto(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "tests/image/1200px-Stray_kitten_Rambo002.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = myPets['pets'][0]['id']
        status, result = self.pf.set_photo(auth_key, pet_id, 'tests/image/1200px-Stray_kitten_Rambo002.jpg')

        assert status == 200



    #add tests
    def test_addNewPetWithNonValidPhoto(self, name='Барбоскин', animal_type='двортерьер', age='4',
                                    pet_photo='images/cat1.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == -1
        assert result == "Fail"

    def test_SetPhotoWithInvalidId(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.set_photo(auth_key, "non_valid_id", 'tests/image/1200px-Stray_kitten_Rambo002.jpg')

        assert status == 500 or status == -2

    def test_addNewPetWithNullableValidData(self, name=None,
                                      animal_type=None, age=None,
                                    pet_photo='tests/image/1200px-Stray_kitten_Rambo002.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['age'] == ''

    def test_addNewPetWithHugeData(self, name='234234234326874wedfgjdsfbvhjhdsbvihbsddiovsdfiofuvnoiefbvoijsdfvboisdbfvoijbsdviobsdfoivjbsdfiovjboisdffvbiojsdfjbvoisdfvbiosdbfviobsdfviobsdviojbsdoifvjbsdfoijjvbiosdfjvjbiosjdfjvbiojsdfvbiojsdfv',
                                      animal_type='dfjgdflgjdflkgjfdlkgjfdlkgjlfdkgjldfkgjlfdkjlfkdgjfdlgjdflkjglfdkjfdlkjfdlkjglkjdflkjdflkjdglkjflkjfdlkjfdlkjfglfgjlkfdglkdfjlkfdgjfdkjlfdlkjjklfgjklfgjlkfjklgiurogbr9437g349bevvmisvpivm',
                                    age='ue9gwuvnew8ofvbuwenv90mwdimweidvniefjvnoicniojnsdcvondfoivndpofvnoisdjfnvoisdfnvoijsdnfoivnsofivnmoidsfnviosdfnviojnsdfviojnsdfiov',
                                    pet_photo='tests/image/1200px-Stray_kitten_Rambo002.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_addNewPetWithEmptyData(self, name='',
                                      animal_type='',
                                    age='',
                                    pet_photo='tests/image/1200px-Stray_kitten_Rambo002.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name


    def test_successfulDeletePetWithInvalidId(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, _ = self.pf.delete_pet(auth_key, "invalid")

        assert status == 200

    def test_get_API_keyForInValidUser(self):
        status, result = self.pf.get_api_key('invalid_email', 'invalid_password')
        assert status == 403

    def test_getAllPetsWithInValidKey(self, filter='another_pets'):  # filter available values : my_pets
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 500