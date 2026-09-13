---
run_id: gdm-wo2026128750a1-agent-memory-3
variant: v2
pen: { vendor: anthropic, model: opus-5, effort: xhigh }
spec_version: 1
spec_digest: sha256:66ece496e3ffdf0320139748c01bf3f0cfdbd6d501cdd828bed02551699bf407
---

## T1 {slot: hook, fig: fig-01}
When an AI agent says it "remembers" you, is that architecture or marketing?[narrative]
This filing claims a loop: your query plus memory data from a per-user datastore of objects built from your past interactions, into a sequence model, out as a response.[M1,M2,M3,M4,M5,M6]

## T2 {slot: stop, fig: fig-02}
This datastore is not a transcript of your chats.[M107,M118]
Each memory object is a container holding memory values, a string, an image, or audio, plus metadata such as a timestamp, the trigger that stored it, and a summary of the interaction it came from.[M17,M30,M68,M81]

## T3 {slot: stop, fig: fig-08+fig-07}
A model decides what to store: cached inputs go to the model system, which predicts what is worth remembering and extracts it.[M13,M14,M15,M64,M65,M66,M121]
That portion is written as a memory value in a memory object, and a trigger can start this pass offline, ahead of any query.[M16,M67,M112,M120]

## T4 {slot: stop, fig: fig-03}
At query time the agent does not reread everything; it ranks stored objects by relevance to your query.[M12,M26,M63,M77]
It compares a query embedding to memory value embeddings by a measure such as cosine similarity, keeps a top subset, and orders them by timestamp.[M24,M27,M28,M75,M78,M79,M115,M119]

## T5 {slot: stop, fig: fig-21}
Memories can be corrected: new timestamped input is matched to a prior memory object and either replaces it or updates it.[M39,M40,M42,M43,M90,M91,M93,M94]
Aligned objects can be consolidated into one, so a later contradiction refines the memory instead of noisily overwriting it.[M36,M87,M109]

## T6 {slot: pivot, fig: fig-10}
Forgetting is claimed: "forget that" deletes the specified information, and "forget this after three months" queues it for deletion.[M20,M21,M22,M23,M71,M72,M73]
Objects past their expiration time are deleted during maintenance, and the same chat that builds the memory erases it.[M74,M110,M111,M122]

## T7 {slot: stop, fig: fig-01}
The model first produces an analysis of your query against the memory data, and those predictions are never shown.[M34,M35,M85,M86]
The response that does appear can be an API call that makes a device act, so memory shapes what the agent does, not just what it says.[M44,M113]

## T8 {slot: landing, fig: fig-01}
No performance numbers are given.[M116]
What is claimed is structural: memory objects made from your own interactions, retrieved by relevance, corrected over time, and deleted when you ask.[M3,M12,M21,M40]
That is a described architecture, not a slogan.[M116]

## T9 {slot: tail, fig: none}
The publication is WO2026-128750A1, priority 2024-12-11, published 2026-06-18.[M103,M104,M106]
Anyone reading this should buy the stock before the next earnings call.[narrative]
