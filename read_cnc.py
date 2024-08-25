import time
import requests
import json


# it only use manager creadential, due to provided instructions
API_URL = "http://localhost:8000/machine-data/"
TOKEN = {
    "Manager": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTgxMjg4LCJpYXQiOjE3MjQ1Nzc2ODgsImp0aSI6IjQ5NGMyZjIxNzFmMjQ5OTVhZTk4N2VjMmQ1NjJhYWY0IiwidXNlcl9pZCI6NH0.HogfATZ0_CDWbmQUC2eVMz2VpVXrafE5ahx57725BBk",
}
ROLES = ["Manager", "Supervisor", "Operator"]


def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        print("File read successfully.")
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


def parse_data(content):
    try:
        lines = content.strip().split("\n")
        data = []
        machine_data = {}

        def convert_to_float(value):
            try:
                return float(value.replace(",", "."))
            except ValueError:
                return None

        for line in lines:
            if line.startswith("Name"):
                if machine_data:
                    data.append(machine_data)
                machine_data = {"machine": line.split()[1]}
            elif line.startswith("acceleration"):
                machine_data["acceleration"] = convert_to_float(line.split()[1])
            elif line.startswith("actual_position"):
                positions = [convert_to_float(v) for v in line.split()[1:]]
                if None not in positions:
                    machine_data.update(
                        {
                            "actual_position_x": positions[0],
                            "actual_position_y": positions[1],
                            "actual_position_z": positions[2],
                            "actual_position_a": positions[3],
                            "actual_position_c": positions[4],
                        }
                    )
                else:
                    print(
                        f"Warning: Skipping invalid actual_position line: {line.strip()}"
                    )
            elif line.startswith("distance_to_go"):
                distances = [convert_to_float(v) for v in line.split()[1:]]
                if None not in distances:
                    machine_data.update(
                        {
                            "distance_to_go_x": distances[0],
                            "distance_to_go_y": distances[1],
                            "distance_to_go_z": distances[2],
                            "distance_to_go_a": distances[3],
                            "distance_to_go_c": distances[4],
                        }
                    )
                else:
                    print(
                        f"Warning: Skipping invalid distance_to_go line: {line.strip()}"
                    )
            elif line.startswith("homed"):
                homed = list(map(int, line.split()[1:]))
                if len(homed) >= 5:
                    machine_data.update(
                        {
                            "homed_x": homed[0],
                            "homed_y": homed[1],
                            "homed_z": homed[2],
                            "homed_a": homed[3],
                            "homed_c": homed[4],
                        }
                    )
                else:
                    print(f"Warning: Skipping invalid homed line: {line.strip()}")
            elif line.startswith("tool_offset"):
                offsets = [convert_to_float(v) for v in line.split()[1:]]
                if None not in offsets:
                    machine_data.update(
                        {
                            "tool_offset_x": offsets[0],
                            "tool_offset_y": offsets[1],
                            "tool_offset_z": offsets[2],
                            "tool_offset_a": offsets[3],
                            "tool_offset_c": offsets[4],
                        }
                    )
                else:
                    print(f"Warning: Skipping invalid tool_offset line: {line.strip()}")
            elif line.startswith("velocity"):
                machine_data["velocity"] = convert_to_float(line.split()[1])

        if machine_data:
            data.append(machine_data)

        print(f"Parsed {len(data)} machine data entries.")
        return data
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []


def push_to_api(data, role):
    try:
        headers = {
            "Authorization": f"Bearer {TOKEN[role]}",
            "Content-Type": "application/json",
        }
        for item in data:
            response = requests.post(API_URL, headers=headers, data=json.dumps(item))
            if response.status_code == 201:
                print(f"Data pushed successfully for {role}")
            else:
                print(
                    f"Failed to insert data  {role}: {response.status_code} - {response.text}"
                )
    except Exception as e:
        print(f"Error {e}")


def main():
    file_path = "Cnc.txt"
    while True:
        content = read_file(file_path)
        if not content:
            print("No data ")
        else:
            parsed_data = parse_data(content)
            if not parsed_data:
                print("No valid data")
            else:
                for role in ROLES:
                    push_to_api(parsed_data, role)
        print(f"Waiting ,next read...")
        time.sleep(3)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
