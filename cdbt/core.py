import json
import os
import re
import subprocess
import sys
import typing as t

import snowflake.connector as snow
from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv("../.env"))
load_dotenv(find_dotenv(".env"))


class Core:

    def __init__(self, test_mode=False):
        self._conn = None
        self._cur = None
        self._create_snowflake_connection()
        self.test_mode = test_mode
        self.dbt_ls_test_mode_output = None
        self.dbt_test_mode_command_check_value = None
        self.exclude_seed_snapshot = "resource_type:snapshot resource_type:seed"

        self.dbt_execute_command_output = ""

    def _create_snowflake_connection(self):
        self._conn = snow.connect(
            account=os.environ.get("DATACOVES__MAIN__ACCOUNT"),
            password=os.environ.get("DATACOVES__MAIN__PASSWORD"),
            schema=os.environ.get("DATACOVES__MAIN__SCHEMA"),
            user=os.environ.get("DATACOVES__MAIN__USER"),
            warehouse=os.environ.get("DATACOVES__MAIN__WAREHOUSE"),
            database=os.environ.get("DATACOVES__MAIN__DATABASE"),
            role=os.environ.get("DATACOVES__MAIN__ROLE"),
        )

        self._cur = self._conn.cursor()

    def dbt_ls_to_json(self, args):
        cmd = ["dbt", "ls", "--output", "json"]
        cmd = cmd + args
        try:
            if self.test_mode:
                output = self.dbt_ls_test_mode_output
            else:
                output = subprocess.run(
                    cmd, check=True, text=True, capture_output=True
                ).stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(e.stdout)
            print(" ".join(cmd))
            sys.exit(e.returncode)
        # The results come back with a few header lines that need to be removed, then a series of JSON string with a
        # format like: {"name": "active_patient_metrics", "resource_type": "model", "config":
        # {"materialized": "incremental"}} RE removes the header stuff and finds the json lines.
        json_lines = re.findall(r"^{.*$", output, re.MULTILINE)
        # Split lines and filter to get only JSON strings
        models_json = [json.loads(line) for line in json_lines]
        return models_json

    @staticmethod
    def execute_dbt_command_capture(command: str, args: t.List[str]) -> str:
        """
        Executes a DBT command and captures the output without streaming to the stdout.
        Args:
            command: The DBT command to run.
            args: A list of args to pass into the command.

        Returns:
            A string containing the results of the command.
        """
        cmd = ["dbt", command] + args
        try:
            output = subprocess.run(
                cmd, check=True, text=True, capture_output=True
            ).stdout
        except subprocess.CalledProcessError as e:
            print(f'Failure while running command: {" ".join(cmd)}')
            print(e.stderr)
            print(e.stdout)
            sys.exit(e.returncode)
        return output

    def get_file_path(self, model_name):
        # This will get the path of the model. note, that unit tests show up as models, so must be excluded via the folder.
        #
        args = [
            "--select",
            model_name,
            "--exclude",
            "path:tests/* resource_type:test",
            "--output-keys",
            "original_file_path",
        ]
        model_ls_json = self.dbt_ls_to_json(args)
        file_path = model_ls_json[0]["original_file_path"]
        return file_path

    @staticmethod
    def handle_cmd_line_error(e):
        print(f'Failure while running command: {" ".join(e.cmd)}')
        print(e.stderr)
        print(e.stdout)
        raise Exception(f"Failure while running command: {' '.join(e.cmd)}")
        # sys.exit(e.returncode)
