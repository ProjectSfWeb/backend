import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

# Импортируй нужные сущности из своего проекта:
from models import Base, User
from schemas.user import UserCreate, UserLogin
from services.auth import register_user, login_user
from services.auth import hash_password


class TestRegisterUser(unittest.TestCase):
    def setUp(self):
        """
        Выполняется перед каждым тестом.
        Создаёт временную БД в оперативной памяти и таблицы.
        """
        self.engine = create_engine("sqlite:///:memory:")  # временная БД
        TestingSession = sessionmaker(bind=self.engine)
        self.session = TestingSession()
        Base.metadata.create_all(self.engine)  # создаёт таблицы

    def tearDown(self):
        """
        Выполняется после каждого теста.
        Закрывает сессию.
        """
        self.session.close()

    def test_successful_registration(self):
        """
        Проверяет, что новый пользователь корректно регистрируется.
        """
        user_data = UserCreate(
            username="newuser",
            password="secret123",
            email="newuser@example.com"
        )

        user = register_user(self.session, user_data)

        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertNotEqual(user.password_hash, "secret123")  # пароль должен быть захеширован
        self.assertTrue(user.password_hash)  # просто чтобы убедиться, что строка не пустая

    def test_duplicate_username(self):
        """
        Проверяет, что при повторной регистрации с тем же username — выбрасывается ошибка.
        """
        # сначала создаём пользователя напрямую
        existing_user = User(
            username="existing",
            password_hash=hash_password("123456"),
            email="exists@example.com"
        )
        self.session.add(existing_user)
        self.session.commit()

        # теперь пробуем зарегистрировать с тем же username
        user_data = UserCreate(
            username="existing",
            password="anotherpass",
            email="another@example.com"
        )

        with self.assertRaises(HTTPException) as context:
            register_user(self.session, user_data)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Username already taken")


class TestLoginUser(unittest.TestCase):
    def setUp(self):
        """
             Выполняется перед каждым тестом.
             Создаёт временную БД в оперативной памяти и таблицы.
             """
        self.engine = create_engine("sqlite:///:memory:")  # временная БД
        TestingSession = sessionmaker(bind=self.engine)
        self.session = TestingSession()
        Base.metadata.create_all(self.engine)  # создаёт таблицы


    def tearDown(self):
        """
               Выполняется после каждого теста.
               Закрывает сессию.
               """
        self.session.close()


    def test_login_success(self):
        # Добавляем пользователя
        user = User(
            username="testuser",
            password_hash=hash_password("testpass123"),
            email="test@example.com"
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        # Подготавливаем входные данные
        login_data = UserLogin(login="testuser", password="testpass123")

        # Выполняем вход
        token = login_user(self.session, login_data)

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)


    def test_login_wrong_password(self):
        user = User(
            username="testuser",
            password_hash=hash_password("correctpass"),
            email="test@example.com"
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        login_data = UserLogin(login="testuser", password="wrongpass")

        with self.assertRaises(Exception) as context:
            login_user(self.session, login_data)

        self.assertEqual(context.exception.status_code, 401)
