from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, exceptions, schemas, InvalidPasswordException

from src.auth.database import User, get_user_db
from src.config import SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
            self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        """
        passport validation func that will ensure that password is strength enough
        :param password: passport typed by user
        :param user: user data
        :return:
        """
        SpecialSym = ['$', '@', '#', '%']

        if len(password) < 6:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

        if len(password) > 20:
            raise InvalidPasswordException(
                reason="length should be at least 6"
            )

        if not any(char.isdigit() for char in password):
            raise InvalidPasswordException(
                reason="length should be not be greater than 8"
            )

        if not any(char.isupper() for char in password):
            raise InvalidPasswordException(
                reason="Password should have at least one numeral"
            )

        if not any(char.islower() for char in password):
            raise InvalidPasswordException(
                reason="Password should have at least one uppercase letter"
            )

        if not any(char in SpecialSym for char in password):
            raise InvalidPasswordException(
                reason="Password should have at least one lowercase letter"
            )

        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
