When an AI agent says it "remembers" you, is that architecture or a marketing word?
This filing answers with a five-step loop, and step two reads a per-user store of memory objects built from your prior chats.
That store is drawn as a box of its own.

What the datastore holds is not a transcript.
Its unit is the memory object, a container holding one or more memory values: strings, images, or audio.
Beside each value sits metadata: a timestamp, the trigger that stored it, a summary of the interaction.

Who decides what the agent keeps?
A model does.
In a memory update cycle, cached inputs go to the model, which predicts what to remember, extracts it, and writes it as a memory object.
Saying "remember this" is one trigger, and the write can run offline.

Recall is not a reread of everything.
In the recall cycle, the agent scores stored objects against the query, comparing embeddings by a measure like cosine similarity.
Only a top subset comes back, ordered by timestamp so the model sees what is recent.

Memories can be corrected.
New input arrives with a timestamp, is matched to a prior memory object, and either replaces it or updates it.
Aligned objects can be consolidated into one, so new information refines a memory instead of noisily overwriting it.

Forgetting is claimed, not just remembering.
"Forget that" deletes the specified information from the datastore.
"Forget this after three months" queues it for deletion.
Expired objects are swept in maintenance, and the same chat erases what it built.

Before answering, the model can analyze your query against the recalled memory.
That analysis is not shown on screen.
The response itself can be an API call that makes a device act, so memory shapes what the agent does, not only what it says.

There are no benchmark numbers here.
The claimed difference is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask.
That is an architecture you can read, not a slogan.

The filing is WO2026-128750A1, with a 2024 priority and a 2026 publication.
Follow along for the next patent walk-through.
