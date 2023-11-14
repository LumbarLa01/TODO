## To Do List

# rethink imports
import rethinkdb as r
from rethinkdb.errors import rqlRuntimeError

# rethink config
RDB_HOST = 'localhost'
RDB_PORT = 28015
TODO_DB = 'todo'

# db setup; only run once
def dbsetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(TODO_DB).run(connection)
        r.db(TODO_DB).table_create('todo').run(connection)
        print "Database setup completed"
    except RqlRuntimeError:
        print "Database already exists."
    finally:
        connection.close()
dbSetup()

# Open connection before each request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=TODO_DB)
    except RqlDriverError:
        abort(503, 'Database connection could not be established')

# Close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.route("/")
def index():
    form = TaskForm()
    selection = list(r.table('todos').run(g.rdb_conn))
    return render_template('index.html', form=form, tasks=selection)
