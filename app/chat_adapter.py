import os
import random

class ChatAdapter:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.system_prompt = "You are a helpful and motivating AI fitness coach. Keep answers concise."

    def respond(self, user_id, message):
        if self.api_key:
            return self._call_llm(message)
        else:
            return self._fallback_rules(message)

    def _call_llm(self, message):
        # Placeholder for OpenAI/LLM call
        # import openai
        # openai.api_key = self.api_key
        # response = openai.ChatCompletion.create(...)
        # return response.choices[0].message.content
        return f"[LLM Mock] I received your message: '{message}'. (LLM integration pending key)"

    def _fallback_rules(self, message):
        msg = message.lower()
        if "diet" in msg or "food" in msg or "eat" in msg:
            return "Focus on whole foods, plenty of vegetables, and lean proteins. Have you checked your diet plan today?"
        elif "workout" in msg or "exercise" in msg or "gym" in msg:
            return "Consistency is key! Even a 20-minute walk makes a difference. Try the workout plan I generated for you."
        elif "weight" in msg or "lose" in msg:
            return "Weight loss is a journey. Maintain a slight calorie deficit and stay active. You've got this!"
        elif "hello" in msg or "hi" in msg:
            return "Hello! I'm your AI Fitness Coach. How can I help you reach your goals today?"
        else:
            return "That's interesting! Tell me more about your fitness goals, or ask me about diet and workouts."

chat_adapter = ChatAdapter()
