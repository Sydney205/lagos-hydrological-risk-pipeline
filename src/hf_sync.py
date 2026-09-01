import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, hf_hub_download

load_dotenv()

HF_REPO_ID = os.getenv("HF_REPO_ID", "Sydney205/lagos-hydrological-zone-data")


def get_hf_token() -> str | None:
  """Retrieve the Hugging Face token from environment variables."""
  return (
      os.getenv("HF_TOKEN")
  )


def upload_to_hf(local_file_path: str, repo_path: str = None) -> bool:
  """Uploads a local file to the configured Hugging Face dataset repo."""
  if not repo_path:
    repo_path = os.path.basename(local_file_path)

  token = get_hf_token()
  if not token:
    print("HF_TOKEN missing in environment. Skipping upload.")
    return False

  try:
    print(f"Syncing {local_file_path} to Hugging Face Hub ({HF_REPO_ID})...")
    api = HfApi()
    api.upload_file(
        path_or_fileobj=local_file_path,
        path_in_repo=repo_path,
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        token=token,
    )
    print(
        "Upload complete:"
        f" https://huggingface.co/datasets/{HF_REPO_ID}"
    )
    return True
  except Exception as e:
    print(f"Failed to sync with Hugging Face: {e}")
    return False


def download_from_hf(filename: str, local_dir: str = ".") -> str | None:
  """Downloads a dataset file from Hugging Face."""
  token = get_hf_token()
  try:
    print(f"Fetching {filename} from Hugging Face...")
    path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=filename,
        repo_type="dataset",
        token=token,
        local_dir=local_dir,
    )
    return path
  except Exception as e:
    print(f"Could not download {filename} from HF: {e}")
    return None
