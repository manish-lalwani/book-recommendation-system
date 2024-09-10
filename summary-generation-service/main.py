import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from llama3_deployment.pdf_processor import extract_text_from_pdf
from llama3_deployment.llm_integration import summarize_chunk, summarize_combined_chunks, summarize_reviews


app = FastAPI()

UPLOAD_DIR = "uploaded_books"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/generate-summary")
async def generate_summary_from_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF of the book, extract its content, and generate a summary using Llama3.
    """

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as f:
        f.write(await file.read())


    try:
        book_content = extract_text_from_pdf(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {str(e)}")


    chunk_size = 2000  # Adjust based on Llama3 context window
    chunks = [book_content[i:i + chunk_size] for i in range(0, len(book_content), chunk_size)]


    chunk_summaries = []
    try:
        for chunk in chunks:
            chunk_summary = await summarize_chunk(chunk)  # Summarize each chunk
            chunk_summaries.append(chunk_summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chunk summary: {str(e)}")


    combined_summaries = " ".join(chunk_summaries)
    try:
        final_summary = await summarize_combined_chunks(combined_summaries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating final summary: {str(e)}")

    return {"summary": final_summary}



@app.post("/generate-review-summary")
async def generate_review_summary(reviews: list[str]):
    """
    Accept a list of reviews for a book and generate an aggregated summary of the reviews.
    """

    combined_reviews = " ".join(reviews)

    try:
        review_summary = await summarize_reviews(combined_reviews, min_length=50, max_length=300)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating review summary: {str(e)}")

    return review_summary


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)