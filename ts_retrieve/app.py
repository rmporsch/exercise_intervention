from chalice import Chalice, BadRequestError
import json
from pydantic import ValidationError
from chalicelib.schemas import RequestUserData, ResponseUserData
from chalicelib.data_download import S3, Settings
from chalicelib.data_interface import CSVData

DATA_FOLDER = "/tmp"

downloader = S3(Settings())
downloader.download(DATA_FOLDER)
interface = CSVData(DATA_FOLDER)


app = Chalice(app_name='ts_retrieve')


@app.route('/user/{user_id}')
def user_exists(user_id):
    users = interface.get_all_users()
    if user_id in users:
        return True
    return False


@app.route('/user')
def all_user():
    users = interface.get_all_users()
    return users


@app.route('/user/table/{table}')
def all_user(table):
    users = interface.get_all_users(table)
    return users


@app.route('/table')
def get_tables():
    return list(interface._data_types)


@app.route('/table/{table}')
def get_table_name(table):
    return interface.get_variable_names(table)

@app.route('/user/data', methods=['POST'])
def request_data():
    request = app.current_request.json_body
    try:
        request = RequestUserData(**request)
    except ValidationError as err:
        raise BadRequestError(str(err))
    if request.table is None:
        output = []
        for table in interface._data_types:
            data = interface.get_k_last(user=request.user_id, table=table, k=request.num_items, exclude_pred=True)
            output.extend(data)
        return_output = ResponseUserData(data=output, user_id=request.user_id)
        return json.loads(return_output.json())
    else:
        return_output = ResponseUserData(
            data=interface.get_k_last(user=request.user_id, table=request.table, k=request.num_items, exclude_pred=True),
            user_id=request.user_id
        )
        return json.loads(return_output.json())


@app.route("/user/prediction/{table}/{user}")
def get_latest_prediction(table, user):
    if table not in interface._data_types:
        raise BadRequestError("wrong table defined")
    if user not in interface.get_all_users(table):
        raise BadRequestError(f"User {user} not found in {table}")
    return_output = ResponseUserData(
        data=interface.get_latest_prediction(user=user, table=table),
        user_id=user
    )
    return json.loads(return_output.json())

