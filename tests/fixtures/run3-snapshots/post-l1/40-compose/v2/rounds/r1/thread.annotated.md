---
run_id: gdm-wo2026128750a1-agent-memory-3
variant: v2
pen: { vendor: anthropic, model: opus-5, effort: xhigh }
spec_version: 1
spec_digest: sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407
---

## T1 {slot: hook, fig: none}
An AI agent says it "remembers" you — architecture, or a slogan?[narrative]
The independent claim is a five-step loop: query in, memory data from a datastore of your past interactions, both into a sequence model, answer out.[M1,M2,M3,M4,M5,M6]
Memory is its own box, not a longer prompt.[M53,M117]

## T2 {slot: stop, fig: none}
So what sits in that box?[narrative]
Not a transcript.[M107]
A memory object is a container: one or more memory values — a string, an image, audio — plus metadata such as a timestamp, the trigger that stored it, and a summary of the conversation it came from.[M17,M30,M68,M81,M118]

## T3 {slot: stop, fig: none}
Who decides what gets stored?[narrative]
A model does.[M13,M64]
Cached inputs go to the model, which predicts whether anything is worth remembering, extracts that portion, and writes it as a memory value.[M14,M15,M16,M65,M66,M67,M121]
Your "remember this" is one trigger, and the write can run offline.[M19,M70,M112,M120]

## T4 {slot: stop, fig: none}
At query time the agent does not reread everything.[M27,M78]
A recall cycle scores stored objects for relevance to the query, using embedding distance such as cosine similarity, and returns a top subset.[M12,M26,M28,M63,M77,M79]
Values come ordered by timestamp, so the model sees recency.[M24,M75,M115,M119]

## T5 {slot: stop, fig: none}
Memories can be corrected.[M40,M43]
New timestamped input is matched to a prior memory object and then either replaces it or updates it.[M39,M42,M90,M91,M93,M94]
Aligned objects can be consolidated into one.[M36,M87]
So contradicting information refines a memory instead of noisily overwriting it.[M109]

## T6 {slot: pivot, fig: none}
Can it forget?[narrative]
"Forget that" deletes that information from the datastore.[M20,M21,M71,M72]
"Forget this after three months" queues it for deletion, and objects past their expiration time are cleared in a maintenance cycle.[M22,M23,M73,M74,M110,M122]
The same chat that builds the memory erases it.[M111]

## T7 {slot: stop, fig: none}
What is the memory for?[narrative]
The model first generates an analysis of your query against the memory data, and that analysis is never shown on screen.[M34,M35,M85,M86]
The response itself can be an API call, so memory shapes what the agent does, not only what it says.[M44,M113]

## T8 {slot: landing, fig: none}
There are no benchmark numbers in this filing.[M116]
What it claims is structural: memory objects built from your own interactions, retrieved by relevance, corrected over time, and deleted when you say so.[M3,M12,M21,M40]
That is an architecture on paper, not a slogan.[M116]

## T9 {slot: tail, fig: none}
Published as WO2026-128750A1 on 2026-06-18, with a priority date of 2024-12-11.[M103,M104,M106]
Follow along if you want the next patent walked through like this.[narrative]
