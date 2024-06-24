# Using this instead of the default as it preserves the order of keys in the dictionary.
import os
import sys
from typing import Any
from typing import Dict

import pyperclip
from dotenv import find_dotenv
from dotenv import load_dotenv
from ruamel.yaml import YAML

from cdbt.ai_core import AiCore
from cdbt.main import ColdBoreCapitalDBT

load_dotenv(find_dotenv("../.env"))
load_dotenv(find_dotenv(".env"))

# Modify the dumper to not sort keys and to use ordered dict format


class SortYAML(AiCore):
    def __init__(self):
        super().__init__()
        self.yaml = YAML(typ="rt")
        self.yaml.preserve_quotes = True
        self.yaml.explicit_start = True

    def main(self, select: str):
        schema_file, table_name = self._get_schema_path_and_table(select)
        schema_data = self.read_yml(schema_file)
        db_columns = self.get_db_columns(table_name)
        updated_schema = self.reorganize_columns(schema_data, db_columns)
        self.save_yml_to_clipboard(updated_schema)

    def _get_schema_path_and_table(self, select: str):
        cbc = ColdBoreCapitalDBT()
        args = ["--select", select]
        ls_json = cbc.dbt_ls_to_json(args)
        schema_file = ls_json[0]["original_file_path"][:-3] + "yml"
        schema = os.environ.get("DEV_SCHEMA")
        if not schema:
            raise ValueError("DEV_SCHEMA environment variable is not set")
        database = os.environ.get("DEV_DATABASE")
        if not database:
            raise ValueError("DEV_DATABASE environment variable is not set")
        table_name = f"{database}.{schema}.{select}"
        print(f"Schema file: {schema_file}")
        print(f"Table name: {table_name}")
        return schema_file, table_name

    def read_yml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r") as stream:
            return self.yaml.load(stream)

    def save_yml_to_clipboard(self, data: Dict[str, Any]):
        # Convert yaml to string. This yaml class is a pain in the ass to get it to return a string. This is sort of
        # a hack where it will send the string data to the copy_to_clip function which saves it to the clipboard.
        # It honestly seems like the guy who wrote this class never considered any need beyond dumping to the stdout.
        self.yaml.dump(data, sys.stdout, transform=self.copy_to_clip)
        print("Sorted YAML schema copied to clipboard!")

    def copy_to_clip(self, string_yaml: str):
        # Remove the first line of the string
        str_lines = string_yaml.split("\n")
        string_yaml = "\n".join(str_lines[1:])
        pyperclip.copy(string_yaml)
        print("Sorted YAML schema copied to clipboard!")
        return string_yaml

    def get_db_columns(self, table_name: str) -> list:
        self._cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        return [desc[0].lower() for desc in self._cur.description]

    def reorganize_columns(
        self, schema_data: Dict[str, Any], db_columns: list
    ) -> Dict[str, Any]:
        if "models" not in schema_data or not schema_data["models"]:
            raise ValueError("YML schema does not contain any models")
        model = schema_data["models"][0]  # Assuming a single model for simplicity
        columns = model.get("columns", [])
        col_dict = {col["name"]: col for col in columns}

        sorted_columns = [col_dict[col] for col in db_columns if col in col_dict]

        model["columns"] = sorted_columns
        schema_data["models"][0] = model
        return schema_data


# # This is used to maintain the order of keys in the dictionary on write back to YAML
# def dict_representer(dumper, data):
#     return dumper.represent_dict(data.items())
# yaml.add_representer(OrderedDict, dict_representer)
# # Add a custom representer to handle normal dictionaries same as OrderedDicts
# yaml.add_representer(dict, dict_representer)
#
# # define a custom representer for strings
# def quoted_presenter(dumper, data):
#     return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
#
# yaml.add_representer(str, quoted_presenter)
#
# class CustomDumper(yaml.Dumper):
#     def represent_data(self, data):
#         if isinstance(data, str) and data.isdigit():
#             return self.represent_scalar('tag:yaml.org,2002:str', data, style="'")
#
#         return super(CustomDumper, self).represent_data(data)


if __name__ == "__main__":
    pass
