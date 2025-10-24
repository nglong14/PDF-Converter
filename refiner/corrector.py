from transformers import pipeline
import re

corrector_pipeline = pipeline("text2text-generation", model="bmd1905/vietnamese-correction")

def correct_text(text):
    # Split while keeping the separators
    sentences = re.split(r'([.!?]\s+)', text)
    
    # Reconstruct with punctuation and chunk every 2 sentences
    chunks = []
    current_chunk = ""
    sentence_count = 0
    
    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            current_chunk += sentences[i]
            if i + 1 < len(sentences):
                current_chunk += sentences[i + 1]
            sentence_count += 1
            
            if sentence_count == 2 or i >= len(sentences) - 2:
                chunks.append(current_chunk.strip())
                current_chunk = ""
                sentence_count = 0
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    corrected_chunks = []
    
    for chunk in chunks:
        if not chunk:
            continue
            
        corrected = corrector_pipeline(chunk, max_length=512)
        corrected_chunks.append(corrected[0]['generated_text'])
    
    return ' '.join(corrected_chunks)