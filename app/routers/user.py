


from fastapi import APIRouter
import app.constants as con


router = APIRouter()


@router.get("/", tags=["users"])
def read_users():
    print(con.db.base)
    return [{"username": "sub"}, {"username": "Bar"}]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}