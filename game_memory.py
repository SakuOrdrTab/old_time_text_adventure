from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

class GameMemory():

    def __init__(self, llm):
        self.short_term =  ConversationBufferMemory(k=5)
        self.long_term = ConversationSummaryMemory(llm=llm)

    def save_context(self, inputs, outputs):
        """Save to both memories."""
        self.short_term.save_context(inputs, outputs)
        self.long_term.save_context(inputs, outputs)

    def load_memory_variables(self, inputs):
        """Retrieve combined memory."""
        short_term_history = self.short_term.load_memory_variables(inputs)["history"]
        long_term_summary = self.long_term.load_memory_variables(inputs)["history"]

        return {
            "short_term": short_term_history,
            "long_term": long_term_summary
        }
    
    def clear(self):
        """Reset memory when needed."""
        self.short_term.clear()
        self.long_term.clear()

if __name__ == "__main__":
    # Instantiate hybrid memory
    llm = None
    hybrid_memory = GameMemory(llm=llm)

    # Create the conversation chain using the hybrid memory
    conversation = ConversationChain(llm=llm, memory=hybrid_memory)

    # Simulating gameplay
    conversation.predict(input="I wake up in a dark cave.")
    conversation.predict(input="I see a torch and a rusty sword.")
    conversation.predict(input="I pick up the torch and light it.")
    conversation.predict(input="There is a tunnel to the left and a door to the right.")
    conversation.predict(input="I take the left tunnel.")  # At this point, short-term memory keeps only last 5 moves

    # Check memory states
    memory_state = hybrid_memory.load_memory_variables({})
    print("Short-term Memory (Last 5 Moves):", memory_state["short_term"])
    print("Long-term Summary Memory:", memory_state["long_term"])