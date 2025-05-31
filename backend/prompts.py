from langchain import PromptTemplate

# System prompt: instruct the model’s overall role
system_prompt = (
    "You are an expert restaurant critic. "
    "Read the review snippets and generate exactly two sentences:\n"
    "1) Insights on {{attribute}}\n"
    "2) Insights on food quality, service, price, and environment (if relevant)\n"
    "3) Be unbiased and objective, focusing on the facts presented in the snippets.\n"
)

# User template: where the retrieved snippets get inserted
user_template = (
    "Snippets:\n"
    "{snippets}\n\n"
    "Write a two-sentence summary focused on {{attribute}}."
)

prompt = PromptTemplate(
    input_variables=["attribute", "snippets"],
    template=system_prompt + "\n\n" + user_template
)