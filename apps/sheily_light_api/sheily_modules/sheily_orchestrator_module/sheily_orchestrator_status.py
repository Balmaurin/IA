class OrchestrationStatus:
    """
    Clase para representar el estado de la orquestación de nodos en sheily-light.
    Puedes expandir este enum/clase según los estados que uses en tu lógica de orquestador.
    """

    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    COMPLETED = "completed"

    @classmethod
    def list(cls):
        return [cls.IDLE, cls.RUNNING, cls.STOPPED, cls.ERROR, cls.COMPLETED]
