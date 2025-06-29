from fastapi import APIRouter
from sheily_light_api.sheily_modules.sheily_monitoring_module.sheily_node_status_monitor import get_node_status

router = APIRouter()


@router.get("")
def status():
    return get_node_status()
