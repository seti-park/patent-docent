An AI agent says it "remembers" you — architecture, or a slogan?
The independent claim is a five-step loop: query in, memory data from a datastore of your past interactions, both into a sequence model, answer out.
Memory is its own box, not a longer prompt.

So what sits in that box?
Not a transcript.
A memory object is a container: one or more memory values — a string, an image, audio — plus metadata such as a timestamp, the trigger that stored it, and a summary of the conversation it came from.

Who decides what gets stored?
A model does.
Cached inputs go to the model, which predicts whether anything is worth remembering, extracts that portion, and writes it as a memory value.
Your "remember this" is one trigger, and the write can run offline.

At query time the agent does not reread everything.
A recall cycle scores stored objects for relevance to the query, using embedding distance such as cosine similarity, and returns a top subset.
Values come ordered by timestamp, so the model sees recency.

Memories can be corrected.
New timestamped input is matched to a prior memory object and then either replaces it or updates it.
Aligned objects can be consolidated into one.
So contradicting information refines a memory instead of noisily overwriting it.

Can it forget?
"Forget that" deletes that information from the datastore.
"Forget this after three months" queues it for deletion, and objects past their expiration time are cleared in a maintenance cycle.
The same chat that builds the memory erases it.

What is the memory for?
The model first generates an analysis of your query against the memory data, and that analysis is never shown on screen.
The response itself can be an API call, so memory shapes what the agent does, not only what it says.

There are no benchmark numbers in this filing.
What it claims is structural: memory objects built from your own interactions, retrieved by relevance, corrected over time, and deleted when you say so.
That is an architecture on paper, not a slogan.

Published as WO2026-128750A1 on 2026-06-18, with a priority date of 2024-12-11.
Follow along if you want the next patent walked through like this.
