import os
from groq import Groq

class LlmAgent:
    def __init__(self, name, model, instruction, tools=None):
        self.name = name
        self.model_name = "llama-3.1-8b-instant"  # Fast Groq model
        self.instruction = instruction
        self.tools = tools or []
        
        # Initialize Groq client
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def run(self, prompt, max_retries=3):
        """Sends prompt to Groq's Llama model"""
        for attempt in range(max_retries):
            try:
                # Create chat completion
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.instruction},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                
                # Return a simple object with .text attribute for compatibility
                return GroqResponse(response.choices[0].message.content)
                
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    import time
                    wait_time = (attempt + 1) * 2
                    print(f"⚠️ Rate limit hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
                    
        return GroqResponse("Error: Max retries exceeded")

class GroqResponse:
    """Simple response wrapper for compatibility"""
    def __init__(self, text):
        self.text = text