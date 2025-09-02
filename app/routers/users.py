from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.service.service_users import UserService
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserBase, UserResponseUser, UserRequest
from core.log import log
from core.tools import paginator
from app.models.pagination import Pagination


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)   

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    if not user.name or not user.email or not user.age or not user.city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Preench todos os campos")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        city=user.city
    )
    data = user_service.insert_user(
        name=new_user.name,
        email=new_user.email,
        age=new_user.age,
        city=new_user.city
    )
    if not data:
        log.error("Erro ao criar usuário")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar user")
    else:
        log.info(f"Usuário {data.name} criado com sucesso")
    
    return data
    
@router.get("api/v1{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não achado")
    return user


@router.get("/api/v1", response_model=Pagination[UserResponse])
def get_all(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página (1-100)")
):
    user_service = UserService(db)
    results = user_service.get_all(page=page, page_size=page_size)

    pagination = paginator(
        items=results["data"],
        page=page,
        page_size=page_size,
        total=results["total_count"]
    )

    return pagination


@router.patch("/api/v1{user_id}", response_model= UserResponseUser, status_code=status.HTTP_200_OK )
def update_users(users_id: int, users: UserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    id = user_service.get_by_id(users_id)
    if not id:
        log.error(f"ID {users_id} não encontrado para atualização.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID não encontrado"
        )
    if id:
        log.info(f"ID {users_id} encontrado para atualização.")
        data = user_service.update(users_id, users)
        if not data:
            raise HTTPException(
                status_code=404,
                detail="ID não encontrado"
            )
        else:
            log.info(f"Atualização realizada com sucesso para o ID: {users_id}")
        
    return data

@router.put("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        data = user_service.delete(user_id)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID não encontrado"
            )
        else:
            log.info(f"Users com ID {user_id} deletado com sucesso.")

        return {"Deletado com sucesso"}
    
    except Exception as e:
        log.error(f"Erro ao deletar Users com ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar Users com ID {user_id}: {str(e)}"
        )


