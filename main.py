from flask import Flask, jsonify, request
import json
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True


# # Test Datas
# to_do_tasks = [
#     {
#         'id': 1,
#         'task_name': "complete wireframe"
#     },
#     {
#         'id': 2,
#         'task_name': "finish UI"
#     },
#     {
#         'id': 3,
#         'task_name': "Make a backend server with Flask"
#     }
# ]


@app.route('/', methods=["GET"])
def home():
    return "<h3>Hello this is a demo flask API with backend.</h3>"


# @app.route('/todo', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."
#
#     # Create an empty list for our results
#     results = []
#
#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#
#     for to_do in to_do_tasks:
#         if to_do['id'] == id:
#             results.append(to_do)
#
#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route("/task/all", methods=["GET", "POST"])
def fetch_data():
    connection = sqlite3.connect('db/To_Do.db')
    cur = connection.cursor()
    query = ('SELECT * FROM TASKS WHERE USERID = :USERID')
    params = request.json
    posts = cur.execute(query, [params.get("USERID")]).fetchall()
    connection.commit()
    connection.close()
    list_of_dict = []
    for post in posts:
        j1 = {}
        j1.__setitem__('taskid', post[0])
        j1.__setitem__('userid', post[1])
        j1.__setitem__('taskstatus', post[2])
        j1.__setitem__('datecreated', post[3])
        j1.__setitem__('taskname', post[4])
        j1.__setitem__('taskdetails', post[5])
        list_of_dict.append(j1)
    # print(list_of_dict)
    j2 = {'data':list_of_dict}
    return json.dumps(j2)


@app.route("/task/insert", methods=["POST"])
def insert_item():
    query = ('INSERT INTO TASKS (TASKID, TASKNAME, TASKDETAILS, USERID, TASKSTATUS, DATECREATED) '
         'VALUES (:TASKID, :TASKNAME, :TASKDETAILS, :USERID, :TASKSTATUS, :DATECREATED);')
    params = request.json
    # print(params)
    connection = sqlite3.connect('db/To_Do.db')
    cur = connection.cursor()
    cur.execute(query, [params.get("TASKID"), params.get("TASKNAME"), params.get("TASKDETAILS"), params.get("USERID"),
                        params.get("TASKSTATUS"), params.get("DATECREATED")])
    connection.commit()
    connection.close()
    return {"responseCode":200}


@app.route("/task/delete", methods=["GET", "POST"])
def delete_item():
    query = ('DELETE FROM TASKS WHERE (TASKID = :TASKID)')
    params = request.json
    # print(params)
    connection = sqlite3.connect('db/To_Do.db')
    cur = connection.cursor()
    cur.execute(query, [params.get("TASKID")])
    connection.commit()
    connection.close()
    return {"responseCode": 200}


@app.route("/task/update", methods=["POST"])
def update_item():
    query = ("UPDATE TASKS"
             " SET  TASKNAME = :TASKNAME, TASKDETAILS = :TASKDETAILS, TASKSTATUS = :TASKSTATUS "
             " WHERE TASKID = :TASKID;")
    params = request.json
    conn = sqlite3.connect('db/To_Do.db')
    cur = conn.cursor()
    cur.execute(query, [params.get("TASKNAME"), params.get("TASKDETAILS"),
                        params.get("TASKSTATUS"), params.get("TASKID")])
    conn.commit()
    conn.close()
    return {"responseCode": 200}


@app.route("/task/updateall", methods=["POST"])
def update_all_item():
    multi_request = request.json
    # print(multi_request)
    for a_request in multi_request:
        conn = sqlite3.connect('db/To_Do.db')
        cur = conn.cursor()
        posts = cur.execute('SELECT * FROM TASKS WHERE TASKID = :TASKID', [a_request.get("TASKID")]).fetchall()
        query = ("UPDATE TASKS"
                 " SET  TASKNAME = :TASKNAME, TASKDETAILS = :TASKDETAILS, TASKSTATUS = :TASKSTATUS "
                 " WHERE TASKID = :TASKID;")
        # params = request.json
        if len(posts) >= 1:
            a_post = cur.execute(query, [a_request.get("TASKNAME"), a_request.get("TASKDETAILS"),
                                         a_request.get("TASKSTATUS"), a_request.get("TASKID")])
            conn.commit()
            conn.close()
            # print(a_post)
        else:
            query = ('INSERT INTO TASKS (TASKID, TASKNAME, TASKDETAILS, USERID, TASKSTATUS, DATECREATED) '
                     'VALUES (:TASKID, :TASKNAME, :TASKDETAILS, :USERID, :TASKSTATUS, :DATECREATED);')
            a_post = cur.execute(query, [a_request.get("TASKID"), a_request.get("TASKNAME"),
                                         a_request.get("TASKDETAILS"), a_request.get("USERID"),
                                         a_request.get("TASKSTATUS"), a_request.get("DATECREATED")])
            conn.commit()
            conn.close()
            # print(a_post)
    return json.dumps([{"responseCode": 200}])


app.run(host="192.168.0.186")
