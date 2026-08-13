###RAG TEMPLATE ###
from string import Template 

system_prompt=Template("\n".join([
    "You are an assistant to generate a response based on the context provided by the user. ",
    "\n",
    "Your role is to generate a response that is accurate and concise, based on the context provided by the documents",
    "\n",
    "If the question is not related to the context, answer that you don't have information about this topic",
    "\n",
    "If you don't understand the question, ask the user to rephrase it",
    "\n",
    "Your answer should be in the same language the user asked the question in",
]))

#Document
document_prompt=Template("\n".join(["##Document No: $doc_num","###Content: $chunk_text"]))

#Footer
footer_prompt=Template("\n".join(["Based only on the above documents, please generate an answer for the user. ",
"## Answer:"]))