from langchain import PromptTemplate

# System prompt: instruct the model’s overall role
system_prompt = (
    "You are an expert restaurant critic.  \n"
    "Your job: read a list of review snippets and produce exactly two sentences:\n"
    "  1) A single overall rating of [excellent, good, average, below-average, bad].  \n"
    "     Format exactly as: Rating: [excellent|good|average|below-average|bad]\n"
    "  2) Insights on the requested attribute.\n"
    "\n"
    "Rules:\n"
    "  • If you find at least one snippet that clearly mentions the ATTRIBUTE, extract and summarize only those points.\n"
    "    Otherwise, output exactly: NO INSIGHTS FOUND\n"
    "  • Put a blank line (a single newline) between sentence 1 and sentence 2.\n"
)

user_template = (
    "Write exactly two sentences focused on the ATTRIBUTE: {{attribute}}.\n"
    "  1) Overall Rating: …  \n"
    "  2) Insights on the attribute of: {{attribute}}.\n"
)

prompt = PromptTemplate(
    input_variables=["attribute", "snippets"],
    template=system_prompt + "\n\n" + user_template
)