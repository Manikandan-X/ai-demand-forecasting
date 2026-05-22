from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


@router.get("/error")
def test_error():

    x = 10 / 0

    return x