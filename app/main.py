.venv\Scripts\Activate.ps1


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered budget recommendation assistant"
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


templates = Jinja2Templates(
    directory="app/templates"
)


app.include_router(
    auth.router
)

app.include_router(
    planners.router
)

app.include_router(
    history.router
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": settings.app_name,
        "ai_enabled": (
            settings.ai_enabled
            and bool(settings.gemini_api_key)
        ),
        "model": settings.gemini_model
    }


@app.get(
    "/",
    response_class=HTMLResponse
)
def home_page(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get(
    "/{page}",
    response_class=HTMLResponse
)
def pages(
    request: Request,
    page: str
):

    allowed = {

        "login":
            "login.html",

        "register":
            "register.html",

        "dashboard":
            "dashboard.html",

        "home-planner":
            "home_planner.html",

        "party-planner":
            "party_planner.html",

        "jewelry-planner":
            "jewelry_planner.html",

        "history":
            "history.html"
    }

    if page not in allowed:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request
            }
        )

    return templates.TemplateResponse(
        allowed[page],
        {
            "request": request
        }
    )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )