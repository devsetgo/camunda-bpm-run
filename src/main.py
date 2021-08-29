  
import httpx
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn
from api_calls.task_processing import get_process_id
from api_calls.history import get_assignment_history
from api_calls.tasks import get_process_instance_tasks
from starlette.responses import JSONResponse,PlainTextResponse

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='statics'), name='static')

base_url: str = "http://localhost:8080/engine-rest"
auth = ("admin", "rules")

@app.route('/')
async def homepage(request):
    proc_data=get_process_id()
    template = "index.html"
    context = {"request": request,'proc_data':proc_data}
    return templates.TemplateResponse(template, context)

@app.route('/process-instance/{processId}')
async def homepage(request):

    proc_id = request.path_params["processId"]
    url=f"{base_url}/process-instance/{proc_id}"
    r =httpx.get(url=url,auth=auth)
    proc_data =r.json()

    task_data= get_process_instance_tasks(proc_id)
    template = "process-instance.html"
    context = {"request": request,'proc_data':proc_data,'task_data':task_data}
    return templates.TemplateResponse(template, context)

@app.route('/get-def/{definitionId}', methods=['GET', 'POST'])
async def get_defintion(request):
    print(request.path_params['definitionId'])
    definitionId = request.path_params["definitionId"]
    url=f"{base_url}/process-definition/{definitionId}"
    r =httpx.get(url=url,auth=auth)
    d =r.json()
    name=d['id'].split(':')[0]
    name=name.replace('_',' ')
    name=f'{name.title()}:'
    return PlainTextResponse(name)

@app.route('/get-tasks-count/{processId}', methods=['GET', 'POST'])
async def get_task_count(request):
    # print(request.path_params['processId'])
    proc_id = request.path_params["processId"]
    r = httpx.get(
        url=f"{base_url}/task/count?processInstanceId={proc_id}",auth=auth
    )

    d =r.json()
    qty=d['count']
    print(qty)
    return PlainTextResponse(str(qty))

@app.route('/get-tasks/{processId}', methods=['GET', 'POST'])
async def get_tasks(request):
    # print(request.path_params['processId'])
    proc_id = request.path_params["processId"]
    r = httpx.get(
        url=f"{base_url}/task?processInstanceId={proc_id}",auth=auth
    )
    task_data =r.json()
    print("hi")

    template = "process-instance.html"
    context = {"request": request,'task_data':task_data}
    return templates.TemplateResponse(template, context)




@app.route('/tab/{id}', methods=['GET', 'POST'])
async def get_tabs(request):
    # print(request.path_params['processId'])
    proc_id = request.path_params["id"]
    data=[{"tab-name":proc_id}]
    return JSONResponse(data)

@app.route('/get-history/{processId}', methods=['GET'])
async def get_history(request):
    
    proc_id = request.path_params["processId"]
    history_data=get_assignment_history(proc_id)
    template = "history-user-op.html"
    context = {"request": request,'history_data':history_data, 'proc_id':proc_id}
    return templates.TemplateResponse(template, context)

@app.route('/get-comments/{processId}', methods=['GET'])
async def get_task_comments(request):
    
    proc_id = request.path_params["processId"]
    comment_data=get_assignment_history(proc_id)
    # history-comments.html
    template = "history-user-op.html"
    context = {"request": request,'comment_data':comment_data, 'proc_id':proc_id}
    return templates.TemplateResponse(template, context)



@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)