import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import dao
from app import modelos
from app import config
import HtmlTestRunner

# Create a clean database
engine = create_engine(config.mysql_database_url)
Session = sessionmaker(autocommit=False, bind=engine)
modelos.Base.metadata.drop_all(engine)
modelos.Base.metadata.create_all(bind=engine)

class NoteDAOTest(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.note_dao = dao.NoteDAO(self.session)
        self.user_dao = dao.UserDAO(self.session)

    def tearDown(self):
        self.session.close()

    def test_create_note(self):
        # Create a user first
        user = self.user_dao.create_user('TestUser1', 'test1@example.com', 'password')

        # Create a note
        note = self.note_dao.create_note(user.id, 'This is a test note1')

        self.assertIsNotNone(note)
        self.assertEqual(note.description, 'This is a test note1')
        self.assertEqual(note.user_id, user.id)

    def test_get_all_notes(self):
        # Create a user and 2 notes
        user = self.user_dao.create_user('TestUser2', 'test2@example.com', 'password')
        self.note_dao.create_note(user.id, 'Note 2')
        self.note_dao.create_note(user.id, 'Note 3')

        notes = self.note_dao.get_all_notes()
        
        # two notes plus one note created aforementioned
        self.assertEqual(len(notes), 3)

    def test_get_note_by_id(self):
        # Create a note
        user = self.user_dao.create_user('TestUser3', 'test3@example.com', 'password')
        note = self.note_dao.create_note(user.id, 'Test Note')

        found_note = self.note_dao.get_note_by_id(note.id)

        self.assertEqual(found_note, note)

    def test_get_notes_by_user_id(self):
        # Create a user and multiple notes
        user = self.user_dao.create_user('TestUser4', 'test4@example.com', 'password')
        self.note_dao.create_note(user.id, 'Note A')
        self.note_dao.create_note(user.id, 'Note B')

        notes = self.note_dao.get_notes_by_user_id(user.id)

        self.assertEqual(len(notes), 2)

    def test_update_note(self):
        # Create a note
        user = self.user_dao.create_user('TestUser5', 'test5@example.com', 'password')
        note = self.note_dao.create_note(user.id, 'Original Note')

        updated_note = self.note_dao.update_note(note.id, 'Updated Note')

        self.assertEqual(updated_note.description, 'Updated Note')

    def test_delete_note(self):
        # Create a note
        user = self.user_dao.create_user('TestUser6', 'test6@example.com', 'password')
        note = self.note_dao.create_note(user.id, 'Note to Delete')

        deleted = self.note_dao.delete_note(note.id)

        self.assertTrue(deleted)

        found_note = self.note_dao.get_note_by_id(note.id)
        self.assertIsNone(found_note)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner())