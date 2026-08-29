import sys
from src.extract import FINAL_MASTER_CSV, extract_hydrological_data
from src.hf_sync import upload_to_hf

def main():
  print("Starting Floodguard Lagos Data Pipeline...\n")

  # Step 1: Run extraction logic
  new_data_fetched = extract_hydrological_data(csv_path=FINAL_MASTER_CSV)

  # Step 2: Upload updated dataset to Hugging Face Hub
  if new_data_fetched:
    upload_to_hf(local_file_path=FINAL_MASTER_CSV)
  else:
    print("Skipping HF sync because no new records were fetched.")


if __name__ == "__main__":
  main()
