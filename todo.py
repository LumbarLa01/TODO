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

## Finalizing the form

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = TaskForm()
        if form.validate_on_submit():
        r.table('todos').insert({"name":form.label.data}).run(g.rdb_conn)
        return redirect(url_for('index'))
    selection = list(r.table('todos').run(g.rdb_conn))
    return render_template('index.html', form = form, tasks = selection)


## Add these to do list items manually
conn = rethink.connect(db='todo')
rethinkdb.table('todos').insert({'name':'sail to the moon'}).run(conn)
{u'errors': 0, u'deleted': 0, u'generated_keys': [u'c5562325-c5a1-4a78-8232-c0de4f500aff'], u'unchanged': 0, u'skipped': 0, u'replaced': 0, u'inserted': 1}
rethinkdb.table('todos').insert({'name':'jump in the ocean'}).run(conn)
{u'errors': 0, u'deleted': 0, u'generated_keys': [u'0a3e3658-4513-48cb-bc68-5af247269ee4'], u'unchanged': 0, u'skipped': 0, u'replaced': 0, u'inserted': 1}
rethinkdb.table('todos').insert({'name':'think of another todo'}).run(conn)
{u'errors': 0, u'deleted': 0, u'generated_keys': [u'b154a036-3c3b-47f4-89ec-cb9f4eff5f5a'], u'unchanged': 0, u'skipped': 0, u'replaced': 0, u'inserted': 1}
