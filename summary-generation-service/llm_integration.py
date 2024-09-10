import os
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


model_path = os.getenv("MODEL_PATH", "models/model_llama_cpp/codellama-13b-python.Q5_K_M.gguf")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path=model_path,
    n_ctx=2048,
    n_gpu_layers=0,
    callback_manager=callback_manager,
    verbose=True,
    repetition_penalty=1.2,
    top_k=10,
    top_p=0.95,
    temperature=0
)


chunk_summary_prompt_template = """
<s>[INST] <<SYS>>
You are tasked with generating a summary for a section of a book. This section is part of a larger document. Focus on summarizing the key points in this section without adding irrelevant details. 
Keep the summary concise but accurate. This is just a part of the book, not the whole.
<</SYS>>
Min length: {min_length}
Max length: {max_length}
Section Content: {context}
[/INST]
"""


combined_summary_prompt_template = """
<s>[INST] <<SYS>>
You are tasked with generating a summary for the entire book based on the summaries of its sections. 
This is a second-level summary, where you are asked to summarize the key points from the section summaries provided below. 
Focus on the overall themes and important information across the whole book.
<</SYS>>
Min length: {min_length}
Max length: {max_length}
Section Summaries: {context}
[/INST]
"""



review_summary_prompt_template = """
<s>[INST] <<SYS>>
You are tasked with summarizing the reviews for a book. The summary should aggregate the most common feedback from users, highlighting both positive and negative sentiments where applicable. 
Focus on capturing the overall experience and opinions of the reviewers without introducing any irrelevant details or hallucinations.
<</SYS>>
Min length: {min_length}
Max length: {max_length}
Reviews Content: {context}
[/INST]
"""


chunk_prompt = PromptTemplate(
    input_variables=["min_length", "max_length", "context"],
    template=chunk_summary_prompt_template
)

combined_prompt = PromptTemplate(
    input_variables=["min_length", "max_length", "context"],
    template=combined_summary_prompt_template
)

review_prompt = PromptTemplate(
    input_variables=["min_length", "max_length", "context"],
    template=review_summary_prompt_template
)


async def summarize_chunk(chunk_text: str):
    final_prompt = chunk_prompt.format(
        min_length=100,
        max_length=300,
        context=chunk_text
    )
    summary = await llm(final_prompt)
    return summary


async def summarize_combined_chunks(combined_summaries: str):
    final_prompt = combined_prompt.format(
        min_length=200,
        max_length=500,
        context=combined_summaries
    )
    final_summary = await llm(final_prompt)
    return final_summary


async def summarize_reviews(combined_reviews: str,min_length=20, max_length=300):

        final_prompt = review_prompt.format(
            min_length=min_length,
            max_length=max_length,
            context=combined_reviews
        )


        summary = await llm(final_prompt)
        return {"summary": summary}
