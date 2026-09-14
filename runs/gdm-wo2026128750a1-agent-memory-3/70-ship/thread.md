When an AI agent says it "remembers" you, is that architecture or marketing?
Agents forget, so you re-enter the same details; the claim is a loop — query plus memory data from a datastore of your past interactions, into a sequence model, out as a response.

This datastore is not a transcript of your chats.
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.

A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.
It is stored as a memory value in a memory object, and one trigger is you asking the agent to remember your favorite architect.

Instead of rereading your whole history, the agent scores stored memory objects for relevance to your query.
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.

Memories are corrected: new timestamped input is matched to the prior memory object it concerns, which is then replaced or updated.
Aligned objects can merge, and a value kept with supporting interactions is refined by contradicting input, not overwritten.

Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.
A maintenance cycle deletes objects past their expiration time on its own, and the chat that builds the memory erases it.

The model first works through your query against the recalled memory data, and that working-out can stay off the screen.
What comes back can be an API call that makes a device act, so the memory shapes what the agent does, not only what it says.

No performance numbers are given.
What is claimed is structural: memory objects made from your interactions, some on your explicit request, retrieved by relevance, corrected over time, and deleted when you ask.
That is a described architecture, not a slogan.

The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.
Follow along for the next patent walk-through.
