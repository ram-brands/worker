from asymmetric import asymmetric as app


@app.router("/", methods=["get"])
def index():
    return "Hello, World!"
