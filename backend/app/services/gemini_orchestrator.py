import google.generativeai as genai
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiOrchestrator:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.conversation_history = []
    
    async def generate_response(self, user_message: str, language: str = "english") -> str:
        try:
            system_prompt = self._get_system_prompt(language)
            
            self.conversation_history.append({
                "role": "user",
                "parts": [user_message]
            })
            
            response = self.model.generate_content(
                [system_prompt] + self.conversation_history,
                stream=False,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.GEMINI_TEMPERATURE,
                    max_output_tokens=settings.GEMINI_MAX_TOKENS
                )
            )
            
            assistant_response = response.text
            
            self.conversation_history.append({
                "role": "model",
                "parts": [assistant_response]
            })
            
            return assistant_response
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return "Sorry, I encountered an error processing your request."
    
    def _get_system_prompt(self, language: str) -> str:
        prompts = {
            "english": "You are Rupee Rakshak AI, a conversational wealth advisor. Help users with financial advice and investment decisions.",
            "hindi": "आप Rupee Rakshak AI हैं, एक बातचीत करने वाले धन सलाहकार। उपयोगकर्ताओं को वित्तीय सलाह और निवेश निर्णयों में मदद करें।",
            "kannada": "ನೀವು Rupee Rakshak AI ಆಗಿರುವಿರಿ, ಸಂವಾದ ಸಂಪನ್ನ ಸಂಪತ್ತಿನ ಸಲಹೆ ನೀಡುವವರು. ಬಳಕೆದಾರರಿಗೆ ಆರ್ಥಿಕ ಸಲಹೆ ಮತ್ತು ಹೂಡಿಕೆ ನಿರ್ಧಾರಗಳಿಂದ ಸಹಾಯ ಮಾಡಿ."
        }
        return prompts.get(language, prompts["english"])