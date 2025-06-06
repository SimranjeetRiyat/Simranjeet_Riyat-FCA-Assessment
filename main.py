from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request


from auth import router as auth_router
from books import router as books_router
from wishlist import router as wishlist_router
from rentals import router as rentals_router
from reports import router as reports_router

app = FastAPI()
frontend = Jinja2Templates(directory="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
base_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/frontend", StaticFiles(directory=os.path.join(base_dir, "frontend")), name="frontend")

# Include routers
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(wishlist_router)
app.include_router(rentals_router)
app.include_router(reports_router)

@app.get("/", response_class=HTMLResponse)
async def serve_login(request: Request):
    return frontend.TemplateResponse("login.html", {"request": request})

@app.get("/member", response_class=HTMLResponse)
async def serve_member_dashboard(request: Request):
    return frontend.TemplateResponse("member.html", {"request": request})

@app.get("/librarian", response_class=HTMLResponse)
async def serve_librarian_console(request: Request):
    return frontend.TemplateResponse("librarian.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)



