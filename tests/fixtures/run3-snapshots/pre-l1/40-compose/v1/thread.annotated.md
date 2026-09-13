---
run_id: gdm-wo2026128750a1-agent-memory-3
variant: v1
pen: { vendor: anthropic, model: opus-5, effort: high }
spec_version: 1
spec_digest: sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407
---

## T1 {slot: hook, fig: none}
An AI agent that "remembers" you: architecture, or marketing?[narrative]
The filing answers with a loop: a query arrives, memory data is pulled from a datastore of your past interactions, and both go into a sequence model.[M1,M2,M3,M4,M53,M117]
The model's output becomes the response.[M5,M6]

## T2 {slot: stop, fig: none}
So what is in that box?[narrative]
Not a transcript: each memory object is a container holding memory values — a string, an image, audio — plus metadata.[M3,M30,M54,M81]
The metadata can carry a timestamp, the trigger that stored it, and a summary of the interaction it came from.[M17,M68,M107,M118]

## T3 {slot: stop, fig: none}
Who decides what is stored?[narrative]
A model does: it reads cached inputs, predicts whether anything is worth keeping, extracts that portion, and stores it as a memory object.[M13,M14,M15,M16,M64,M65,M66,M67,M121]
"Remember this" is one trigger, and the write can happen offline, not at query time.[M19,M70,M112,M120]

## T4 {slot: stop, fig: none}
At query time the agent does not reread everything.[M12,M63]
It scores stored objects against the query by embedding distance, such as cosine similarity, and returns a top subset.[M26,M27,M28,M77,M78,M79]
The values it returns are ordered by timestamp, so the model sees what is recent.[M24,M75,M115,M119]

## T5 {slot: stop, fig: none}
Memories can also be corrected.[M43,M94]
New timestamped input is matched to a prior memory object, then either replaces it or updates it.[M39,M40,M42,M90,M91,M93,M125]
Objects that align can be consolidated into one, so a contradiction refines a memory instead of noisily overwriting it.[M36,M87,M109]

## T6 {slot: pivot, fig: none}
The decisive part: forgetting is claimed.[M20,M21]
"Forget that" deletes information from the datastore; "forget this after three months" queues it for deletion.[M22,M23,M71,M72,M73]
Expired objects are deleted during maintenance cycles, and the same chat is the surface for erasing it.[M74,M110,M111,M122]

## T7 {slot: stop, fig: none}
What is the memory for?[narrative]
First the model generates an analysis of the query against the memory data, never shown on screen.[M34,M35,M85,M86]
The final response can itself be an API call that makes a device act, so memory shapes what the agent does, not only what it says.[M44,M113]

## T8 {slot: landing, fig: none}
No benchmark numbers are claimed.[M116]
What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, erased on request.[M3,M12,M40,M21]
That is an architecture on paper, not a slogan.[narrative]

## T9 {slot: tail, fig: none}
Publication: WO2026-128750A1, priority 2024, published 2026.[M103,M104,M106]
Follow for the next patent walk-through.[narrative]
