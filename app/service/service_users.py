from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select, func
from core.log import log
from app.schemas.user import UserRequest, UserResponseUser
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def insert_user(self, name:str, email:str, age:int, city:str) -> User:
        try:
            new_user = User(name=name, email=email, age=age, city=city)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


    def get_by_id(self, user_id:int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            log.error(f"User with id {user_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado!")
        return user
    
    def get_all(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            
            if page < 1:
                page = 1
            if page_size < 1:
                page_size = 10
            if page_size > 100:
                page_size = 100

            
            query = select(User)
            offset = (page - 1) * page_size
            query = query.limit(page_size).offset(offset)
            results = self.db.scalars(query)

            
            count_query = select(func.count()).select_from(User)
            total_count = self.db.scalar(count_query)

            
            users_data = [
                UserResponseUser.model_validate({
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'city': user.city
                }) 
                for user in results.all()
            ]

            return {
                'data': users_data,
                'total_count': total_count
            }        
        except SQLAlchemyError as e:
            log.error(f"Erro ao processar ALL : {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar ALL : {str(e)}"
            )
        except Exception as e:
            log.error(f"Erro ao processar ALL : {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar ALL : {str(e)}"
            )


    def update(self, user_id:int, user:UserRequest) -> UserResponseUser:
        try:
            existing_user = self.db.get(User,user_id)
            if not existing_user:
                log.error(f"Users com ID {user_id} não encontrado para atualização.")
            
            if user.name is not None:
                existing_user.name = user.name
            if user.email is not None:
                existing_user.email = user.email
            if user.age is not None:
                existing_user.age = user.age
            if user.city is not None:
                existing_user.city = user.city
            if user.updated_at is not None:
                existing_user.updated_at = datetime.now()

            self.db.commit()
            self.db.refresh(existing_user)
            log.info(f"Users com ID {user_id} atualizado com sucesso.")
            return UserResponseUser.model_validate(existing_user.__dict__)
        except SQLAlchemyError as e:
            self.db.rollback()
            log.error(f"Erro ao atualizar Users com ID {user_id}: {str(e)}")
        except Exception as e:
            self.db.rollback()
            log.error(f"Erro ao atualizar Users com ID {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar Users com ID {user_id}: {str(e)}"
            )


    def delete(self, user_id: int):
        try:
            users = self.db.get(User, user_id)
            if not users:
                raise HTTPException(status_code=404, detail="Registro não encontrado")
            
            if hasattr(users, 'is_deleted') and users.is_deleted:
                raise HTTPException(status_code=400, detail="Registro já foi deletado")
            
            if hasattr(users, 'is_deleted'):
                users.is_deleted = True
                self.db.commit()
                self.db.refresh(users)
                return {"Registro deletado com sucesso"}
            

        except SQLAlchemyError as e:
                self.db.rollback()  # IMPORTANTE: Reverte a transação em caso de erro
                self.__logger.error(f"Erro ao deletar User com ID {user_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro de banco de dados ao deletar User com ID {user_id}"
                )

    


    
