"""
Test for the repository adapter.
"""
from auth.adapters.repository import UserRepository
from auth.domain.models import User


class TestRepository:

    def test_repository_does_save_user(self, user_repository: UserRepository):
        """
        Test that the repository can save a user.
        """
        # given
        user = User(username="test", password="test", email="valide@email.com")

        # when
        user_repository.save(user)

        # then
        assert user in user_repository.find_all()

    def test_repository_does_find_user_by_username(self, user_repository: UserRepository):
        """
        Test that the repository can find a user by its username.
        """
        # given
        username = "test"
        user = User(username=username, password="test", email="valid@email.com")
        user_repository.save(user)

        # when
        found_user = user_repository.find_by_username(username)

        # then
        assert found_user == user

    def test_repository_does_find_all_users(self, user_repository: UserRepository):
        """
        Test that the repository can find all users.
        """
        # given
        user1 = User(username="test1", password="test", email="test1@email.com")
        user2 = User(username="test2", password="test", email="test2@email.com")
        user_repository.save(user1)
        user_repository.save(user2)

        # when
        users = user_repository.find_all()

        # then
        assert user1, user2 in users

    def test_repository_does_delete_user(self, user_repository: UserRepository):
        """
        Test that the repository can delete a user.
        """
        # given
        user = User(username="test", password="test", email="valid@email.com")
        user_repository.save(user)

        # when
        user_repository.delete(user)

        # then
        assert user not in user_repository.find_all()

    def test_none_when_not_found(self,
                                 user_repository: UserRepository):
        """
        Test that the repository does not find a user by its username if it does
         not exist.
        """
        # when
        found_user = user_repository.find_by_username("a user that does "
                                                      "not exists")

        # then
        assert found_user is None
