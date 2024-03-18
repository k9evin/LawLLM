import json
import os
import logging

logging.basicConfig(level=logging.INFO)


def convert_format(original_file, target_file, is_grouped=False):
    """
    Convert the input JSON file to the desired format.

    Grouped example:
    [
        [
            {
                "input": "",
                "instruction": "假冒他人专利进行买卖算不算诈骗",
                "output": "假冒他人专利进行买..."
            },
        ]
    ]

    Ungrouped example:
    [
        {
            "input": "",
            "instruction": "假冒他人专利进行买卖算不算诈骗",
            "output": "假冒他人专利进行买..."
        },
    ]

    Args:
        original_file (str): The path to the original file.
        target_file (str): The path to the target file.
        is_grouped (bool, optional): Whether the input data is grouped or not. Defaults to False.
    """
    if not os.path.exists(original_file):
        logging.error(f"File {original_file} not found.")
        return

    try:
        with open(original_file, "r", encoding="utf-8") as file:
            input_data = json.load(file)
    except Exception as e:
        logging.error(f"Error reading file: {str(e)}")
        return

    output_data = []
    for group in input_data:
        items = group if is_grouped else [group]
        for item in items:
            try:
                corrected_item = {
                    "instruction": item["instruction"],
                    "input": item["input"],
                    "output": item["output"],
                }
                output_data.append(corrected_item)
            except KeyError as e:
                logging.error(f"Invalid data format: {str(e)}")
                return

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    try:
        with open(target_file, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error writing to file: {str(e)}")
        return

    logging.info(f"Format conversion completed. Data saved to {target_file}.")


if __name__ == "__main__":
    logging.info(f"Current Working Directory: {os.getcwd()}")

    # Modify to change different input file
    original_file_name = "legal_advice.json"

    BASE_DIR = os.getcwd()
    RAW_DATA_FOLDER = os.path.join(BASE_DIR, "data", "raw")
    PROCESSED_DATA_FOLDER = os.path.join(BASE_DIR, "data", "processed")
    original_file_path = os.path.join(RAW_DATA_FOLDER, original_file_name)
    target_file_path = os.path.join(PROCESSED_DATA_FOLDER, original_file_name)

    convert_format(original_file_path, target_file_path, is_grouped=True)
