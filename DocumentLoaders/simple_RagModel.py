import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "rag_docs"
CHROMA_DIR = BASE_DIR / "chroma_db"
GEMINI_MODEL = os.getenv("GOOGLE_MODEL", "models/gemini-3.6-flash")


def load_documents() -> list:
	documents = []
	for file_path in sorted(DOCS_DIR.glob("*.txt")):
		loader = TextLoader(str(file_path), encoding="utf-8")
		documents.extend(loader.load())
	return documents


def build_retriever():
	os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

	raw_documents = load_documents()
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=400,
		chunk_overlap=80,
	)
	split_documents = splitter.split_documents(raw_documents)

	embeddings = HuggingFaceEmbeddings(
		model_name="sentence-transformers/all-MiniLM-L6-v2",
		model_kwargs={
			"device": "cpu",
		},
		encode_kwargs={
			"normalize_embeddings": True,
		},
	)

	vector_store = Chroma(
		collection_name="simple_rag_docs",
		embedding_function=embeddings,
		persist_directory=str(CHROMA_DIR),
	)

	vector_store.reset_collection()
	vector_store.add_documents(split_documents)

	return vector_store.as_retriever(search_kwargs={"k": 3})


def format_docs(documents) -> str:
	sections = []
	for doc in documents:
		source = Path(doc.metadata.get("source", "unknown")).name
		sections.append(f"Source: {source}\n{doc.page_content}")
	return "\n\n".join(sections)


def build_chain():
	load_dotenv()

	if not os.getenv("GOOGLE_API_KEY"):
		raise ValueError("Set GOOGLE_API_KEY in your environment or .env file before running this script.")

	retriever = build_retriever()
	prompt = ChatPromptTemplate.from_template(
		"""
You are a helpful RAG assistant.
Answer the question only from the provided context.
If the answer is not present in the context, say that the data does not contain the answer.

Context:
{context}

Question:
{question}
""".strip()
	)

	llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL)

	chain = (
		{
			"context": retriever | format_docs,
			"question": RunnablePassthrough(),
		}
		| prompt
		| llm
		| StrOutputParser()
	)
	return chain


def main() -> None:
	chain = build_chain()
	print(f"Loaded {len(list(DOCS_DIR.glob('*.txt')))} text files from {DOCS_DIR.name}.")
	print("Ask questions about the local knowledge base. Type 'exit' to stop.\n")

	while True:
		question = input("Question: ").strip()
		if question.lower() in {"exit", "quit"}:
			break
		if not question:
			continue

		answer = chain.invoke(question)
		print("\nAnswer:")
		print(answer)
		print()


if __name__ == "__main__":
	main()
