from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app import dao
from app import modelos
from app import config
import unittest
import HtmlTestRunner

# Create a clean database
engine = create_engine(config.mysql_database_url)
Session = sessionmaker(autocommit=False, bind=engine)
modelos.Base.metadata.drop_all(engine)
modelos.Base.metadata.create_all(bind=engine)

class UserDAOTest(unittest.TestCase):
    def setUp(self):
        # Create a test database session
        self.session = Session()
        self.user_dao = dao.UserDAO(self.session)

    def tearDown(self):
        # Rollback any changes made during the tests
        # self.session.rollback() (TODO: deve ser removido porque cada operacao do DAO eh atomica, ou seja, cada operacao ja faz seu commit)
        self.session.close()

    def test_create_user(self):
        # Create a new user
        user = self.user_dao.create_user('TestUser1', 'test1@example.com', 'password')

        # Assert that the user was created successfully
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'TestUser1')
        self.assertEqual(user.email, 'test1@example.com')

    def test_get_all_users(self):
        # Create multiple users
        self.user_dao.create_user('TestUser2', 'test2@example.com', 'password2')
        self.user_dao.create_user('TestUser3', 'test3@example.com', 'password3')

        # Get all users
        users = self.user_dao.get_all_users()

        # Assert that the correct number of users is returned
        # o test case test_create_user salvou um usuario e este usuario ficou registrado
        self.assertEqual(len(users), 3)

    def test_get_user_by_id(self):
        # Create a user
        user = self.user_dao.create_user('TestUser4', 'test4@example.com', 'password4')

        # Get the user by ID
        found_user = self.user_dao.get_user_by_id(user.id)

        # Assert that the correct user is returned
        self.assertEqual(found_user, user)

    def test_get_user_by_username(self):
        # Create a user
        user = self.user_dao.create_user('TestUser5', 'test5@example.com', 'password5')

        # Get the user by username
        found_user = self.user_dao.get_user_by_username('TestUser5')

        # Assert that the correct user is returned
        self.assertEqual(found_user, user)

    def test_update_user(self):
        # Create a user
        user = self.user_dao.create_user('TestUser6', 'test6@example.com', 'password6')

        # Update the user's email
        updated_user = self.user_dao.update_user(user.id, 'new_email@example.com')

        # Assert that the email was updated
        self.assertEqual(updated_user.email, 'new_email@example.com')

    def test_delete_user(self):
        # Create a user
        user = self.user_dao.create_user('TestUser7', 'test7@example.com', 'password7')

        # Delete the user
        deleted = self.user_dao.delete_user(user.id)

        # Assert that the user was deleted
        self.assertTrue(deleted)

        # Try to get the deleted user
        found_user = self.user_dao.get_user_by_id(user.id)
        self.assertIsNone(found_user)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner())