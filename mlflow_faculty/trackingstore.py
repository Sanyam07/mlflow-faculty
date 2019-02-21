# Copyright 2019 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from uuid import UUID

import faculty
from mlflow.store.abstract_store import AbstractStore
from mlflow.entities import ViewType, Experiment
from six.moves import urllib


class FacultyRestStore(AbstractStore):
    def __init__(self, store_uri, **_):
        parsed_uri = urllib.parse.urlparse(store_uri)
        if parsed_uri.scheme != "faculty":
            raise ValueError("Not a faculty URI: {}".format(store_uri))

        cleaned_path = parsed_uri.path.strip("/")
        try:
            self._project_id = UUID(cleaned_path)
        except ValueError:
            raise ValueError(
                "{} in given URI {} is not a valid UUID".format(
                    cleaned_path, store_uri
                )
            )

        self._client = faculty.client("experiment")

    def list_experiments(self, view_type=ViewType.ACTIVE_ONLY):
        """
        :param view_type: Qualify requested type of experiments.

        :return: a list of Experiment objects stored in store for requested
            view.
        """
        raise NotImplementedError()

    def create_experiment(self, name, artifact_location):
        """
        Creates a new experiment.
        If an experiment with the given name already exists, throws exception.

        :param name: Desired name for an experiment
        :param artifact_location: Base location for artifacts in runs. May be
            None.

        :return: experiment_id (integer) for the newly created experiment if
            successful, else None
        """
        try:
            faculty_experiment = self._client.create(
                self._project_id, name, artifact_location=artifact_location
            )
        except faculty.clients.base.HttpError:
            return None
        else:
            return faculty_experiment.id

    def get_experiment(self, experiment_id):
        """
        Fetches the experiment by ID from the backend store.

        :param experiment_id: Integer id for the experiment

        :return: A single :py:class:`mlflow.entities.Experiment` object if it
            exists, otherwise raises an exception.
        """
        faculty_experiment = self._client.get(
            os.getenv("FACULTY_PROJECT_ID"), experiment_id
        )

        return Experiment(
            faculty_experiment.id,
            faculty_experiment.name,
            faculty_experiment.artifact_location,
            "active" if faculty_experiment.deleted_at else "deleted",
        )

    def get_experiment_by_name(self, experiment_name):
        """
        Fetches the experiment by name from the backend store.

        :param experiment_name: Name of experiment

        :return: A single :py:class:`mlflow.entities.Experiment` object if it
            exists.
        """
        return super(FacultyRestStore, self).get_experiment_by_name(
            experiment_name
        )

    def delete_experiment(self, experiment_id):
        """
        Deletes the experiment from the backend store. Deleted experiments can
        be restored until permanently deleted.

        :param experiment_id: Integer id for the experiment
        """
        raise NotImplementedError()

    def restore_experiment(self, experiment_id):
        """
        Restore deleted experiment unless it is permanently deleted.

        :param experiment_id: Integer id for the experiment
        """
        raise NotImplementedError()

    def rename_experiment(self, experiment_id, new_name):
        """
        Update an experiment's name. The new name must be unique.

        :param experiment_id: Integer id for the experiment
        """
        raise NotImplementedError()

    def get_run(self, run_uuid):
        """
        Fetches the run from backend store

        :param run_uuid: Unique identifier for the run

        :return: A single :py:class:`mlflow.entities.Run` object if it exists,
            otherwise raises an exception
        """
        raise NotImplementedError()

    def update_run_info(self, run_uuid, run_status, end_time):
        """
        Updates the metadata of the specified run.

        :return: :py:class:`mlflow.entities.RunInfo` describing the updated
            run.
        """
        raise NotImplementedError()

    def create_run(
        self,
        experiment_id,
        user_id,
        run_name,
        source_type,
        source_name,
        entry_point_name,
        start_time,
        source_version,
        tags,
        parent_run_id,
    ):
        """
        Creates a run under the specified experiment ID, setting the run's
        status to "RUNNING" and the start time to the current time.

        :param experiment_id: ID of the experiment for this run
        :param user_id: ID of the user launching this run
        :param source_type: Enum (integer) describing the source of the run

        :return: The created Run object
        """
        raise NotImplementedError()

    def delete_run(self, run_id):
        """
        Deletes a run.
        :param run_id:
        """
        raise NotImplementedError()

    def restore_run(self, run_id):
        """
        Restores a run.
        :param run_id:
        """
        raise NotImplementedError()

    def log_metric(self, run_uuid, metric):
        """
        Logs a metric for the specified run
        :param run_uuid: String id for the run
        :param metric: :py:class:`mlflow.entities.Metric` instance to log
        """
        raise NotImplementedError()

    def log_param(self, run_uuid, param):
        """
        Logs a param for the specified run
        :param run_uuid: String id for the run
        :param param: :py:class:`mlflow.entities.Param` instance to log
        """
        raise NotImplementedError()

    def set_tag(self, run_uuid, tag):
        """
        Sets a tag for the specified run
        :param run_uuid: String id for the run
        :param tag: :py:class:`mlflow.entities.RunTag` instance to set
        """
        raise NotImplementedError()

    def get_metric_history(self, run_uuid, metric_key):
        """
        Returns all logged value for a given metric.

        :param run_uuid: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A list of float values logged for the give metric if logged,
            else empty list
        """
        raise NotImplementedError()

    def search_runs(self, experiment_ids, search_expressions, run_view_type):
        """ Returns runs that match the given list of search expressions within
        the experiments.  Given multiple search expressions, all these
        expressions are ANDed together for search.

        :param experiment_ids: List of experiment ids to scope the search
        :param search_expression: list of search expressions

        :return: A list of :py:class:`mlflow.entities.Run` objects that satisfy
            the search expressions
        """
        raise NotImplementedError()
