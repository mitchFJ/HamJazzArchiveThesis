from sentence_transformers import SentenceTransformer

def save_model(model_name: str):
    """Loads any model from Hugginface model hub and saves it to disk."""
    model = SentenceTransformer(model_name)
    model.save("./model")

if __name__ == "__main__":
    save_model("all-MiniLM-L6-v2")