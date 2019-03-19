import os

import faculty
from mlflow.tracking.context import RunContextProvider


FACULTY_ENV_TAGS = [
    ("FACULTY_PROJECT_ID", "mlflow.faculty.project.projectId"),
    ("FACULTY_SERVER_ID", "mlflow.faculty.server.serverId"),
    ("FACULTY_SERVER_NAME", "mlflow.faculty.server.name"),
    ("NUM_CPUS", "mlflow.faculty.server.cpus"),
    ("AVAILABLE_MEMORY_MB", "mlflow.faculty.server.memoryMb"),
    ("NUM_GPUS", "mlflow.faculty.server.gpus"),
    ("FACULTY_JOB_ID", "mlflow.faculty.job.jobId"),
    ("FACULTY_JOB_NAME", "mlflow.faculty.job.name"),
    ("FACULTY_RUN_ID", "mlflow.faculty.job.runId"),
    ("FACULTY_RUN_NUMBER", "mlflow.faculty.job.runNumber"),
    ("FACULTY_SUBRUN_ID", "mlflow.faculty.job.subrunId"),
    ("FACULTY_SUBRUN_NUMBER", "mlflow.faculty.job.subrunNumber"),
]

USER_ID_TAG = "mlflow.faculty.user.userId"


class FacultyRunContext(RunContextProvider):
    def __init__(self):
        self._user_id_cache = None

    @property
    def _user_id(self):
        if self._user_id_cache is None:
            client = faculty.client("account")
            self._user_id_cache = client.authenticated_user_id()
        return self._user_id_cache

    def in_context(self):
        return "FACULTY_PROJECT_ID" in os.environ

    def tags(self):
        tags = {}
        for environment_variable, tag_name in FACULTY_ENV_TAGS:
            try:
                tags[tag_name] = os.environ[environment_variable]
            except KeyError:
                pass
        try:
            tags[USER_ID_TAG] = self._user_id
        except Exception:
            pass
        return tags
