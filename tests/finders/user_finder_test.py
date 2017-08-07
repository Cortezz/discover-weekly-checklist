from tests.base import BaseTestCase
from app.finders.user_finder import UserFinder
from app.services.create_user_service import CreateUserService


class UserFinderTest(BaseTestCase):

    def test_find_user(self):
        create_user_service = CreateUserService("name", "email", "spotify_id")
        user = create_user_service.call()

        found_user = UserFinder.get_from_id(user.id)

        self.assertTrue(found_user)
        self.assertEquals(user.id, found_user.id)
