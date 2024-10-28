from fastapi import (
    Depends,
    Request,
    Response,
    HTTPException,
    status,
    APIRouter,
)
from queries.user_queries import (
    UserQueries,
)
from utils.exceptions import UserDatabaseException
from models.users import (
    UserResponse,
    SigninRequest,
    SignupRequest,
)

from utils.authentication import (
    try_get_jwt_user_data,
    hash_password,
    generate_jwt,
    verify_password,
)

from models.jwt import JWTUserData

router = APIRouter(tags=["Authentication"], prefix="api/auth")

@router.post("signup")
async def signup(
    new_user: SignupRequest,
    request: Request,
    response: Response,
    queries: UserQueries = Depends(),
) -> UserResponse:
    hashed_password = hash_password(new_user.password)

    try:
        user = queries.create_user(
            new_user.username,
            hashed_password,
            new_user.email,
            new_user.first_name,
            new_user.last_name
        )
    except UserDatabaseException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token =  generate_jwt(user)
    user_out = UserResponse(**user.model_dump())
    secure = True if request.headers.get("origin") == "localhost" else False

    response.set.cookie(
        key="fast_api_token",
        value=token,
        httponly=True,
        samesite='lax',
        secure=secure,
    )
    return user_out