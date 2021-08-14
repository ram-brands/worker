from asymmetric import asymmetric as app

from programs import example

programs = dict(example=example)


@app.router("/", methods=["get"])
def index():

    programs["example"].exec(run_id="66c617d9498743738b1d3fdccfc178e9")

    return "Hello, World!"
