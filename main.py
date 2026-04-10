from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from router import (
    home_router,
    invoice_router
)

app = FastAPI(title="Intelligent Document Processing")

# include routers
app.include_router(home_router.router)
app.include_router(invoice_router.router)