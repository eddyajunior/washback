from app.core.exceptions import BusinessException, ValidationException
from app.infrastructure.database.models.company import Company
from app.infrastructure.database.models.user import User
from app.schemas.user import LoginRequest

from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token
)

class AuthService:

    def __init__(
            self,
            user_repository,
            company_repository
    ):
        self.user_repository = user_repository
        self.company_repository = company_repository

    def validate_user(self, email: str):
        return self.user_repository.get_by_email(email)

    def register_user(self, user: LoginRequest):
        existing_user = self.validate_user(user.email)

        if existing_user:
            raise ValidationException(
                "Email já cadastrado"
            )

        company = Company(
            name="Minha Empresa"
        )

        added_company = self.company_repository.create(company)

        new_user = User(
            email=user.email,
            hashed_password=hash_password(
                user.password
            ),
            company_id=added_company.id
        )

        added_user = self.user_repository.create(new_user)

        if added_user.id < 1:
            raise BusinessException(
                "Erro ao criar usuário",
                500
            )
            
        return True
    
    def authenticate_user(self, user: LoginRequest):
        db_user = self.user_repository.get_by_email(user.email)

        if not db_user:
            raise ValidationException(
                "Credenciais inválidas"
            )

        valid_password = verify_password(
            user.password,
            db_user.hashed_password
        )

        if not valid_password:
            raise ValidationException(
                "Credenciais inválidas"
            )

        token = create_access_token(
            {
                "sub": db_user.email,
                "company_id": db_user.company_id
            }
        )
        return token