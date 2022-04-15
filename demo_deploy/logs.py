from gc import enable
from azureml.core import Workspace
from azureml.core.webservice import Webservice

ws = Workspace.from_config()

name = "demo-model-deploy"

service = Webservice(name=name, workspace=ws)

service.update(enable_app_insights=True)

logs = service.get_logs()

for line in logs.split("\n"):
    print(line)
