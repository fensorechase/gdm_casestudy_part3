"""
Real RAG Chatbot with Llama 3.2 1B
Students will implement this during the lecture

SKELETON VERSION - Students fill in the TODOs
"""

from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np


class ChatbotRAG:
    """
    Real RAG chatbot using:
    - Llama 3.2 1B for text generation
    - FAISS for similarity search
    - sentence-transformers for embeddings
    """
    
    def __init__(self):
        """Initialize the chatbot components"""
        print("Loading RAG chatbot...")
        

        # TODO 1: Before starting, make sure you have run 'python setup_real_rag.py' to create the knowledge base and FAISS index!
        # Task: Load the language model (it's really a "small language model", but we might still call it an "LLM" for ease.)
        # Use the instructions under "Simple llama-cpp-python example code' at the following tutorial on HuggingFace: 
        #           https://huggingface.co/MaziyarPanahi/Llama-2-7b-chat-hf-function-calling-v2-GGUF#:~:text=Simple%20llama%2Dcpp%2Dpython%20example,about%20llamas.%22%20%7D%20%5D%20)
        # Hint: the Llama model file should be in your folder 'models/llama-2-7b-chat.Q2_K.gguf'.
        # Hint 2: Use Llama class with model_path and n_ctx parameters
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.llm = None
        # =============================================
        
        # TODO 2: Load the embedding model
        # We need an embedding model to convert the text from our "knowledge base" into vectors for similarity search (in particular, the vectors are 32-bit float arrays).
        # Hint: Use SentenceTransformer with model name "sentence-transformers/all-MiniLM-L6-v2"
        # Note: This is the same embedding model we used in the setup script 'setup_real_rag.py' -- take a look there if you need a reminder.
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.embedding_model = None
        # =============================================
        
        # TODO 3: Load the FAISS index.
        # FAISS is a library for efficient similarity search -- given a query (e.g., patient question), we use it to find relevant documents from our knowledge base.
        # Your FAISS index file should be in 'rag/faiss_index.bin'
        # Hint: Use faiss.read_index(), and you can call your index file 'rag/faiss_index.bin'
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.index = None
        # =============================================
        
        # TODO 4: Load the document texts -- you should have run 'python setup_real_rag.py' before this, so you should see a .pkl file in rag/ directory 
        # Hint: Use pickle.load()
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.documents = []
        # =============================================
        
        print(f"✓ RAG chatbot loaded with {len(self.documents)} knowledge chunks")
    
    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve relevant context from knowledge base
        
        Args:
            query: User's question
            k: Number of relevant chunks to retrieve
            
        Returns:
            Combined context string
        """
        # TODO 5: Embed the query
        # Hint: Use self.embedding_model.encode()
        # ========== STUDENTS IMPLEMENT THIS ==========
        query_embedding = None
        # =============================================
        
        # TODO 6: Search FAISS index
        # Hint: Use self.index.search() - returns distances and indices
        # ========== STUDENTS IMPLEMENT THIS ==========
        distances, indices = None
        # =============================================
        
        # TODO 7: Retrieve the actual document texts
        # Hint: Use indices to get documents from self.documents
        # ========== STUDENTS IMPLEMENT THIS ==========
        retrieved_docs = None
        # =============================================
        
        # Combine into context
        context = "\n\n".join(retrieved_docs)
        
        # If we have some retrieved context, print a snippet.
        if context: 
            print(f"Retrieved {k} context chunks for query.")
            print("Snipped of retrieved context:", context[:200] + "...")
        return context
    
    def generate_response(self, query: str, context: str, language: str = 'en') -> str:
        """
        Generate response using LLM with retrieved context
        
        Args:
            query: User's question
            context: Retrieved context from knowledge base
            language: 'en' or 'ml'
            
        Returns:
            Generated response
        """
        # TODO 8: Create the prompt
        # Hint: Include system instructions, context, and user query
        # ========== STUDENTS IMPLEMENT THIS ==========
        
        if language == 'ml':
            lang_instruction = "" # Write a brief instruction in this string to tell Llama to answer in Malayalam.
        else:
            lang_instruction = "" # Write a brief instruction in this string to tell Llama to answer in English.
        
        prompt = f"""You are a helpful assistant for pregnant women with gestational diabetes in Kerala, India.

Use this information to answer the question:
{context}

User question: {query}

{lang_instruction}

Provide a helpful, accurate answer based on the context above. If the context doesn't contain enough information, say so.

Answer:"""
        # =============================================
        
        # TODO 9: Generate response from LLM
        # Hint: Use self.llm() with max_tokens and stop parameters
        # ========== STUDENTS IMPLEMENT THIS ==========
        response = self.llm(
            prompt,
            max_tokens=256,
            stop=["User:", "\n\n\n"],
            temperature=0.7
        )
        # =============================================
        
        # Extract text from response
        answer = response['choices'][0]['text'].strip()
        return answer
    
    def get_response(self, user_message: str, language: str = 'en', region: str = 'Kerala') -> str:
        """
        Main method - retrieve context and generate response
        
        Args:
            user_message: User's question
            language: 'en' or 'ml'
            region: User's region (for context)
            
        Returns:
            Bot response
        """
        # TODO 10: Call retrieve_context()
        # ========== STUDENTS IMPLEMENT THIS ==========
        context = self.retrieve_context(user_message, k=3)
        # =============================================
        
        # TODO 11: Call generate_response()
        # ========== STUDENTS IMPLEMENT THIS ==========
        response = self.generate_response(user_message, context, language)
        # =============================================
        
        return response


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test the chatbot"""
    print("\n" + "="*60)
    print("Testing Real RAG Chatbot")
    print("="*60)
    
    # Initialize
    bot = ChatbotRAG()
    
    # Test questions
    test_questions = [
        ("Can I eat dosa for breakfast?", "en"),
        ("How much rice can I have?", "en"),
        ("Is fish curry good for GDM?", "en"),
        ("Tell me about coconut", "en"),
    ]
    
    for question, lang in test_questions:
        print(f"\nQ: {question}")
        print(f"A: {bot.get_response(question, lang)}")
        print("-" * 60)