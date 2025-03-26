import json
from jsonschema import validate, ValidationError, SchemaError

def validate_json(json_path, schema_path):
    """
    Validate a JSON file against a given JSON schema.

    This function reads a JSON file and a schema file.
    It ensures that the JSON file conforms the schema.

    :param json_path: str
        The file path of the JSON file to be validated.
    :param schema_path: str
        The file path of the JSON schema file.

    :return: bool
        validation result
    """
    try:
        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)

        with open(schema_path, 'r') as schema_file:
            schema_data = json.load(schema_file)

        validate(instance=json_data, schema=schema_data)
        print("JSON is valid!")
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except SchemaError as e:
        print(f"Schema error: {e.message}")
    except OSError as e:
        print(f"OS error: {e}")
    return False


def check_keys_match(schema_file: str, parameters: dict):
    """
    Check if the keys in the JSON schema match the keys in the parameters.

    :param schema_file: Path to the schema JSON file
    :param parameters: dict containing the keys to check
    :returns: None, prints mismatches if any
    """
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    schema_required_keys = schema.get("required", [])
    missing_keys = []
    for key in schema_required_keys:
        if key not in parameters:
            missing_keys.append(key)

    if missing_keys:
        raise ValueError(f"Missing required keys: {missing_keys}")