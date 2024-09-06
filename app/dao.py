from app.modelos import User
from app.modelos import Note
from sqlalchemy.exc import SQLAlchemyError

# DAO (Data Access Object) for User model
class UserDAO:
    def __init__(self, session):
        self.session = session                   

    def create_user(self, username, email, password):
        new_user = None
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            self.session.add(new_user)
            self.session.commit()
        except SQLAlchemyError as sqlerror:
            print(type(sqlerror))
            self.session.rollback()
            raise Exception(f'Erro ao inserir usuário: {str(sqlerror)}')
        return new_user

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_id(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def update_user(self, user_id, email):
        #user = self.session.query(User).get(user_id) TODO: deprecated
        user = self.session.get(User, user_id)
        if user:
            user.email = email
            self.session.commit()
            return user
        else:
            return None

    def delete_user(self, user_id):
        #user = self.session.query(User).get(user_id) TODO: deprecated
        user = self.session.get(User, user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        else:
            return False

# DAO (Data Access Object) for Note model
class NoteDAO:
    def __init__(self, session):
        self.session = session

    def create_note(self, user_id, description):
        new_note = None
        try:
            new_note = Note(description=description, user_id=user_id)
            self.session.add(new_note)
            self.session.commit()
        except SQLAlchemyError as sqlerror:
            print(type(sqlerror))
            self.session.rollback()
            raise Exception(f'Erro ao criar nota: {str(sqlerror)}')
        return new_note

    def get_all_notes(self):
        return self.session.query(Note).all()

    def get_note_by_id(self, note_id):
        return self.session.query(Note).filter_by(id=note_id).first()

    def get_notes_by_user_id(self, user_id):
        return self.session.query(Note).filter_by(user_id=user_id).all()

    def update_note(self, note_id, description):
        note = self.session.get(Note, note_id)
        if note:
            note.description = description
            self.session.commit()
            return note
        else:
            return None

    def delete_note(self, note_id):
        note = self.session.get(Note, note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
            return True
        else:
            return False