from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from .balance import calculate_balance
from .auth import register, login
from .filters import filter_transactions


router = APIRouter(prefix="/front", tags=["Front"])
templates = Jinja2Templates(directory="front/templates")

@router.get("/balance")
def get_balance(request: Request):
    return templates.TemplateResponse(name="Dashboard.html", context={"request": request})


@router.get("/comingin")
def entrance(request: Request):
    return templates.TemplateResponse(name="Entrance.html", context={"request": request})


@router.get("/register2")
def registration(request: Request):
    return templates.TemplateResponse(name="Registration.html", context={"request": request})

@router.get("/change")
def registration(request: Request):
    return templates.TemplateResponse(name="Change.html", context={"request": request})

@router.get("/delete")
def registration(request: Request):
    return templates.TemplateResponse(name="Delete.html", context={"request": request})
