An AI agent that "remembers" you: architecture, or marketing?
The filing answers with a loop: a query arrives, memory data is pulled from a datastore of your past interactions, and both go into a sequence model.
The model's output becomes the response.

So what is in that box?
Not a transcript: each memory object is a container holding memory values — a string, an image, audio — plus metadata.
The metadata can carry a timestamp, the trigger that stored it, and a summary of the interaction it came from.

Who decides what is stored?
A model does: it reads cached inputs, predicts whether anything is worth keeping, extracts that portion, and stores it as a memory object.
"Remember this" is one trigger, and the write can happen offline, not at query time.

At query time the agent does not reread everything.
It scores stored objects against the query by embedding distance, such as cosine similarity, and returns a top subset.
The values it returns are ordered by timestamp, so the model sees what is recent.

Memories can also be corrected.
New timestamped input is matched to a prior memory object, then either replaces it or updates it.
Objects that align can be consolidated into one, so a contradiction refines a memory instead of noisily overwriting it.

The decisive part: forgetting is claimed.
"Forget that" deletes information from the datastore; "forget this after three months" queues it for deletion.
Expired objects are deleted during maintenance cycles, and the same chat is the surface for erasing it.

What is the memory for?
First the model generates an analysis of the query against the memory data, never shown on screen.
The final response can itself be an API call that makes a device act, so memory shapes what the agent does, not only what it says.

No benchmark numbers are claimed.
What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, erased on request.
That is an architecture on paper, not a slogan.

Publication: WO2026-128750A1, priority 2024, published 2026.
Follow for the next patent walk-through.
