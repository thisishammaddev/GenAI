import warnings
# Silence the langchain-community sunset warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import TextLoader

loader = TextLoader("cricket.txt", encoding="utf-8")
documents = loader.load()

print(type(documents))
print(documents[0])
