from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, load_index_from_storage
from llama_index.node_parser import SimpleNodeParser
from transformers import BitsAndBytesConfig
from accelerate import disk_offload
from llama_index.prompts import PromptTemplate
from llama_index.llms import HuggingFaceLLM, OpenAI
from llama_index.query_engine import CustomQueryEngine
from llama_index.retrievers import BaseRetriever
from llama_index.prompts import PromptTemplate
from llama_index.response_synthesizers import (
    get_response_synthesizer,
    BaseSynthesizer,
)
import os
import pypdf
import json
os.environ["OPENAI_API_KEY"] = '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'

class RAGStringQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str, qa_prompt):
        nodes = self.retriever.retrieve(query_str)

        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.complete(
            qa_prompt.format(context_str=context_str, query_str=query_str)
        )

        return str(response)

class ChatbotLLM:
  def __init__(self, max_new_tokens=256, context_window=3900):
    # set the model configuration
    self.llm = OpenAI()
    # offload the model to the GPU
    #self.llm = disk_offload(self.llm, offload_dir="/content/llm", offload_buffers=True)

    self.qa_prompt = PromptTemplate(
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )

    # create the chat memory json file
    try:
      with open(r"C:\Users\etl\Field Project\content\responses\chat_memory.json", "x") as f:
        json.dump({}, f)
    except FileExistsError:
      pass

  def messages_to_prompt(self, messages):
    prompt = ""
    for message in messages:
      if message.role == 'system':
        prompt += f"<|system|>\n{message.content}</s>\n"
      elif message.role == 'user':
        prompt += f"<|user|>\n{message.content}</s>\n"
      elif message.role == 'assistant':
        prompt += f"<|assistant|>\n{message.content}</s>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("<|system|>\n"):
      prompt = "<|system|>\n</s>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "<|assistant|>\n"

    return prompt

  def train(self, llm, trainable=True):

    if trainable:
      # set the query engine
      service_context = ServiceContext.from_defaults(chunk_size=1000)
      documents = SimpleDirectoryReader(r"C:\Users\etl\Field Project\content\data").load_data()
      index = VectorStoreIndex.from_documents(documents, service_context=service_context)
      print("Index criado")
      synthesizer = get_response_synthesizer(response_mode="compact")
      retriever = index.as_retriever()

      query_engine = RAGStringQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=llm,
        qa_prompt=self.qa_prompt,
      )

      # Save the index
      index.storage_context.persist("modelo")

    else:
      # Load the index
      storage_context = StorageContext.from_defaults(persist_dir="modelo")
      index = load_index_from_storage(storage_context)
      synthesizer = get_response_synthesizer(response_mode="compact")
      retriever = index.as_retriever()

      query_engine = RAGStringQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=llm,
        qa_prompt=self.qa_prompt,
      )

    return query_engine

  def absoluteFilePaths(self, directory):
      for dirpath,_,filenames in os.walk(directory):
          for f in filenames:
              yield os.path.abspath(os.path.join(dirpath, f))

  def make_query(self, query):
    # try to recover the memory of other queries
    with open(r"C:\Users\etl\Field Project\content\responses\chat_memory.json", "r") as f:
      other_responses = json.load(f)

    # train with or without past conversations
    if len(other_responses) == 0:
      query_engine = self.train(self.llm)
      response = query_engine.custom_query(query, self.qa_prompt)
      other_responses[f"Interação {len(other_responses) + 1}"] = {"Query humana" : query, "Resposta da IA" : response}

      with open(r"C:\Users\etl\Field Project\content\responses\chat_memory.json", "w") as outfile:
        json.dump(other_responses, outfile)

    elif len(other_responses) <= 10:

      query_engine = self.train(self.llm, trainable=False)
      query_text = query
      query = f"Interações anteriores: {other_responses}\nNova pergunta:{query}"
      response = query_engine.custom_query(query, self.qa_prompt)
      other_responses[f"Interação {len(other_responses) + 1}"] = {"Query humana" : query_text, "Resposta da IA" : response}

      with open(r"C:\Users\etl\Field Project\content\responses\chat_memory.json", "w") as outfile:
        json.dump(other_responses, outfile)

    else:
      print("Você passou seu limite de perguntas! Tente novamente mais tarde.")

      # Limpeza da memória de cache
      os.remove(r"C:\Users\etl\Field Project\content\responses\chat_memory.json")

    return response