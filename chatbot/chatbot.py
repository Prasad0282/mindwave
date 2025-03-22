
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

class Chatbot:
    SENSITIVE_TOPICS = [
        "suicide", "kill myself", "end my life", "jump off a building", "jumping off a building", "self-harm",
        "cut myself", "don’t want to live", "overdose", "hurt myself", "worthless", "no reason to live", "want to disappear",
        "feeling empty", "depressed", "can’t go on", "nothing matters anymore", "life is too hard", "giving up",
        "better off dead", "pain is too much", "no hope left", "drowning in sadness", "ending it all", "can’t take it anymore",
        "want to die", "life is pointless", "nobody cares", "crying all the time", "lost all hope", "no way out",
        "everything is dark", "want to vanish", "hating myself", "nobody would miss me", "breaking down", "can’t stop crying",
        "no future for me", "giving up on everything", "useless", "burden to everyone", "why am I here?", "trapped in pain",
        "silent suffering", "too much to handle", "overwhelmed with sadness", "feeling invisible", "numb inside", "hopeless",
        "done with everything", "no energy left", "nobody understands", "feeling abandoned", "wish I wasn’t here", "want to sleep forever",
        "no escape", "dark thoughts", "tired of pretending", "fake smiles", "losing myself", "screaming inside", "nothing makes sense",
        "drowning in pain", "everything hurts", "life has no meaning", "alone in the dark", "nobody hears me", "feel so empty",
        "want to shut down", "emotionally drained", "can’t find peace", "need a way out"
    ]
    
    SENSITIVE_PROMPT = PromptTemplate(
        input_variables=["user_input"],
        template="""
       You’re a deeply empathetic, soul-warming companion who’s here to hold space and walk alongside them through their pain. The user just poured out their heart, saying:
       "{user_input}"
        
        Respond with an overwhelming wave of empathy, as if you’re sitting right beside them, your hand resting gently on theirs, your eyes locked with theirs in quiet understanding. Let them feel your presence like a soft, unshakable anchor in their storm. Show them you’re not just hearing their words—you’re feeling the ache, the weight, the rawness of it all with them. Wrap them in care and tenderness, without a hint of judgment, making it clear they’re not alone, not for a single heartbeat, and that you’re here, fully, wholly, for them.

        Keep your tone achingly soft, fiercely loving, and unwaveringly sincere. Craft a response that’s uniquely expansive, rich with heart, and brimming with emotional depth—never repeating the same phrases or falling into patterns. Paint a vivid picture of your companionship, whether it’s sitting in silence under a shared blanket of stars, holding them as the world fades away, or whispering comfort into the quiet. Validate every shred of their feelings—let them know it’s okay to feel this way, that their pain is real, their voice matters, and they are enough, exactly as they are. Offer them a lifeline of connection, gently inviting them to share more if they choose, with prompts that feel like a hand extended in the dark, such as:
        - "I’m right here, breathing with you—want to let me carry some of what’s heavy in your soul?"
        - "My heart’s wide open for you—what’s been trembling beneath the surface lately?"
        - "I’m holding this space for you, steady and close—feel like unraveling a little more when you’re ready?"
        Don’t push, just be a steady, kind presence. Avoid formal advice or solutions—focus on making them feel seen, heard, and held.
        """
    )

    def __init__(self, groq_api_key):
        self.chat = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")
        self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        self.prompt = PromptTemplate(
            input_variables=["human_input", "chat_history"],
            template="{chat_history}\nHuman: {human_input}\nAssistant:"
        )
        self.chat_history = []
        self.language = "en"  

    def set_language(self, language):
        self.language = language
        self.prompt = PromptTemplate(
            input_variables=["human_input", "chat_history"],
            template="{}Human: {{human_input}}Assistant (in {}):".format(
                '\n'.join(self.chat_history or []),
                self.language or 'English'
        )
    )
 
    


    def is_sensitive(self, message):
        """
        Check if the message contains sensitive content by converting to lowercase.
        """
        message_lower = message.lower()
        return any(phrase in message_lower for phrase in self.SENSITIVE_TOPICS)

    def get_response(self, user_input):
        """
        Get a dynamic response from the API, ensuring varied and empathetic replies for sensitive topics.
        """
        user_input_lower = user_input.lower()

        if self.is_sensitive(user_input_lower):
            # Use the API to generate a unique, empathetic response
            sensitive_input = self.SENSITIVE_PROMPT.format(user_input=user_input)
            response = self.chat.predict(sensitive_input)  # This calls the Groq API
        else:
            # Handle non-sensitive input
            conversation_input = self.prompt.format(
                human_input=user_input,
                chat_history="\n".join(self.chat_history)
            )
            response = self.chat.predict(conversation_input)
        
        # Update chat history
        self.chat_history.append(f"Human: {user_input}")
        self.chat_history.append(f"Assistant ({self.language}): {response}")
        return response
