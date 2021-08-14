from asymmetric import asymmetric as app

from programs import example

programs = dict(example=example)


@app.router("/", methods=["post"])
def index(program_name, run_id):
    program = programs[program_name]
    program.exec(run_id)
    return run_id
