When an AI agent says it "remembers" you, is that architecture or marketing?
This filing claims a loop: your query plus memory data from a per-user datastore of objects built from your past interactions, into a sequence model, out as a response.

This datastore is not a transcript of your chats.
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.

A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.
That portion is written as a memory value in a memory object, and a trigger can start this pass offline, ahead of any query.

At query time the agent does not reread everything; it ranks stored objects by relevance to your query.
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.

Memories can be corrected: new timestamped input is matched to a prior memory object and either replaces it or updates it.
Aligned objects can be consolidated into one, so a later contradiction refines the memory instead of noisily overwriting it.

Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.
Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.

The model first produces an analysis of your query against the memory data, and those predictions are never shown.
The response that does appear can be an API call that makes a device act, so memory shapes what the agent does, not just what it says.

No performance numbers are given.
What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask.
That is a described architecture, not a slogan.

The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.
Follow along for the next patent walk-through.
