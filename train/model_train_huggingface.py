from huggingface_hub import Repository, login, HfApi, ModelCard, ModelCardData
from dotenv import load_dotenv
import os

from models import build_bidirec_lstm_model

load_dotenv()

if __name__ == "__main__":
    model = build_bidirec_lstm_model()
    local_hugface_dir = "model_repo"
    model_fname = os.path.join(local_hugface_dir, "test_model.keras")

    """login into hugging face"""
    HF_TOKEN = os.getenv("HF_TOKEN")
    login(HF_TOKEN)

    """clone repo"""
    repo_id = "DrMarcus24/stock-predictor"
    if not os.path.exists(local_hugface_dir):
        repo = Repository(
            local_dir=local_hugface_dir,  # creates local repo for you
            clone_from=repo_id,  # path to remote repo
            token=True,
        )  # use token from login function

    """save model"""
    model_fname = os.path.join(local_hugface_dir, "model.keras")
    model.save(model_fname)

    """commit model repo changes to hugging face"""
    api = HfApi()

    api.upload_folder(folder_path=local_hugface_dir, repo_id=repo_id, repo_type="model")

    """Create model card for front page of repo"""
    card_data = ModelCardData(language="en", library_name="tensorflow")
    card = ModelCard.from_template(
        card_data,
        model_id="stock-predictor-model",
        model_description="this model predicts the stock prices for [insert sotck ticker]",
        developers="Marcus Allen",
        repo="https://github.com/marcus-24/Stock-Predictor-Backend",
    )

    card.push_to_hub(repo_id)
