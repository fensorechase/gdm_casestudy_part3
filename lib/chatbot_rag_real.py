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
        
        # TODO 1: Load the LLM model
        # Hint: Use Llama class with model_path and n_ctx parameters
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.llm = Llama(
            model_path="models/llama-2-7b-chat.Q2_K.gguf",
            n_ctx=2048,  # Context window
            n_threads=4,  # CPU threads
            verbose=False
        )
        # =============================================
        
        # TODO 2: Load the embedding model
        # Hint: Use SentenceTransformer with model name
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # =============================================
        
        # TODO 3: Load the FAISS index
        # Hint: Use faiss.read_index()
        # ========== STUDENTS IMPLEMENT THIS ==========
        self.index = faiss.read_index('rag/faiss_index.bin')
        # =============================================
        
        # TODO 4: Load the document texts
        # Hint: Use pickle.load()
        # ========== STUDENTS IMPLEMENT THIS ==========
        with open('rag/documents.pkl', 'rb') as f:
            self.documents = pickle.load(f)
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
        query_embedding = self.embedding_model.encode([query])
        # =============================================
        
        # TODO 6: Search FAISS index
        # Hint: Use self.index.search() - returns distances and indices
        # ========== STUDENTS IMPLEMENT THIS ==========
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            k
        )
        # =============================================
        
        # TODO 7: Retrieve the actual document texts
        # Hint: Use indices to get documents from self.documents
        # ========== STUDENTS IMPLEMENT THIS ==========
        retrieved_docs = [self.documents[idx] for idx in indices[0]]
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
            lang_instruction = "Answer in Malayalam."
        else:
            lang_instruction = "Answer in English."
        
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