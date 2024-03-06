from urllib.request import Request
from fastapi import Depends, HTTPException, APIRouter, status
from customers.models.customers_models import Customer, Token
from customers.schemmas.schemas import CustomerCreate, TokenCreate, CustomerResponse, CustomerModify
from customers.services.service import *
from sqlalchemy.orm import Session
from core.db import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/v1/customers",
    tags=["customers"],
    responses={404: {"description": "Not founds"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/customers/token")


def get_customer(db: Session, username: str):
    return db.query(Customer).filter(Customer.username == username).first()


def create_customer_token(db: Session, customer: Customer):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": customer.username}, expires_delta=access_token_expires
    )
    token = Token(customer_id=customer.id, access_token=access_token)
    # db.add(token)
    # db.commit()
    # db.refresh(token)
    return token


def create_customer(db: Session, customer):
    db_customer = Customer(username=customer.username, hashed_password=pwd_context.hash(customer.password),
                           is_active=customer.is_active,
                           is_superuser=customer.is_superuser)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, db_customer, customer):
    for key, value in customer.__dict__.items():
        if key == 'password' and value is not None:
            key = 'hashed_password'
            value = pwd_context.hash(value)
        setattr(db_customer, key, value)

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


async def get_current_super_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_customer(db, username=token_data.get("sub"))
        if not (user and user.is_active and user.is_superuser):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="need permission")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="need permission")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_customer(db, username=token_data.get("sub"))
        if not (user and user.is_active):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="need permission")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="need permission")


@router.post("/token", response_model=TokenCreate)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    customer = get_customer(db, username=form_data.username)
    if not customer or not verify_password(form_data.password, customer.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not customer.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Active User")

    token = create_customer_token(db, customer)
    return {"access_token": token.access_token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(current_user: Customer = Depends(get_current_user)) -> CustomerResponse:
    return current_user


@router.post("/users")
async def create_user(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = get_customer(db, customer.username)
    if db_customer:
        return update_customer(db=db, db_customer=db_customer, customer=customer)
    return create_customer(db=db, customer=customer)


@router.put("/users")
async def update_user(customer: CustomerModify, db: Session = Depends(get_db),
              current_user: Customer = Depends(get_current_user)) -> CustomerResponse:
    db_customer = get_customer(db, current_user.username)
    if db_customer:
        return update_customer(db=db, db_customer=db_customer, customer=customer)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not found")
