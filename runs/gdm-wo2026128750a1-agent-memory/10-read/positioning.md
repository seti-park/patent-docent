# 포지셔닝 (D5 ⑤)

## M147

- 배경 문제: Agent systems without a memory capability make the user re-enter the same information across turns and across sessions, and must interrupt with follow-up prompts whenever a request omits a detail the user believes it has already given. The specification's own examples are a calendar entry at a dentist during a lunch break, where neither the dentist nor the lunch interval can be resolved, and a request that omits a previously stated dietary restriction.
- 주장 효과: The specification asserts that an intelligently managed, dynamic interaction memory datastore lets the system begin execution from a single interaction where a traditional system would have to come back for details, avoiding the processing of additional inputs and the rendering of additional outputs for the task.
- 차이: No measurement is offered on either side. The stated difference is structural: context that the compared systems must re-solicit synchronously is instead retrieved from a user-specific store assembled out of prior interactions. The saving is argued in counts of interactions, not in time, tokens or cost.
- 인용: “Without a memory of useful context, traditional agent devices may require entry of the same information multiple times over the same or multiple sessions in order to perform the same or similar tasks.”
- 인용: “an example machine-learned agent system, leveraging a memory according to the present disclosure, can initiate execution with a single interaction”

## M148

- 배경 문제: The alternative the specification names is exposing the agent to external application programming interfaces that fetch context from third-party data sources. It argues three defects: such sources were never curated by the agent against this user's interactions, the agent cannot keep them fresh, and they bundle sensitive material with the useful material — the dietary restriction that lives inside a health or medical-communication application.
- 주장 효과: Memory grounded in what the user gave the agent directly over a history of interactions is asserted to give improved control over stored contextual information: the user can withhold, can permit a limited purpose, and can instruct the system to forget afterwards.
- 차이: Structural. The unit at which permission is granted moves from the data source to the individual memory object, replacing an all-or-nothing grant over a whole application with per-memory admission. No comparative figure of any kind is given, and the argument that the store stays fresher is asserted rather than demonstrated.
- 인용: “Under traditional approaches to enabling external data sources, the user may be faced with an all-or-nothing choice, which may be undesirable in some circumstances.”
- 인용: “The user can decline to provide information that the user does not wish to share, or the user can instruct the agent system to use the information for limited purposes and subsequently forget.”

## M149

- 배경 문제: Even when an external source holds the datum, it may not be contextualised for the particular interaction. The specification's illustration is a request to call Blake where the user has both a best friend and a dentist of that name: the contact list contains the answer and still cannot select it, so the system must interrupt to ask.
- 주장 효과: Interaction-derived memory is asserted to carry the disambiguating context a generic external source lacks, and thereby to avoid a class of interruption the specification describes in physiological terms — arrested auditory and visual attention, diverted gaze, interrupted utterance, and the switching cost of returning to the abandoned task.
- 차이: Structural, and unusually the delta is argued in human rather than computational currency. The switching cost is called a measurable interval, but no interval is measured; it is invoked as a category of harm the memory avoids, not as a quantity the memory reduces by some amount.
- 인용: “a user may have a best friend named Blake”
- 인용: “a switching cost can refer to a measurable interval of time required for the human brain to switch from performing any other task to the task of responding to the follow-up event”

## M150

- 배경 문제: Existing systems render configuration prompts at the moment a browser loads a web resource — typically for the data-handling parameters of an analytics system — and generally require the user to perceive and answer the prompt synchronously, at that moment, before the underlying content is usable.
- 주장 효과: The specification asserts that preferences parsed and stored at an earlier time let the agent answer such prompts asynchronously on the user's behalf in near real time, completing the task without initiating a synchronous interaction event when the task actually arises, and reducing the latency between the triggering event and the executed response.
- 차이: Structural, and this is the document's strongest stated delta: it claims the arrangement provides a mechanism for controlling a computing device that would not be possible without the datastore — a difference in kind rather than degree. It remains an assertion; no latency measurement accompanies it, and the sentence making the claim still uses the superseded term context datastore.
- 인용: “Generally, existing systems require synchronous perception of and response to the prompt (e.g., inputting a configuration parameter).”
- 인용: “In this manner, for instance, the task can be completed without initiating a synchronous interaction event at the time of the task performance.”
- 인용: “example implementations provide a mechanism for controlling a computing device that would not be possible if the machine-learned agent system did not implement an intelligently managed, dynamic context datastore as described herein”

## M151

- 배경 문제: The naive way to give a model memory is to prepend the raw history — an exhaustive record of prior interactions, a full transcript — to the query. The specification argues this is both expensive at inference time and, for a particular task, sometimes less reliable or accurate than a curated input.
- 주장 효과: Pre-processing interactions offline into structured, high-quality memory objects holding key features and metadata is asserted to reduce the runtime computational load, to lower latency by reducing the complexity of the inference task, and to move the curation work onto a time-shifted schedule away from peak demand.
- 차이: Structural, plus an unquantified scheduling claim. Both the accuracy assertion and the load assertion are stated without figures for either the transcript baseline or the curated alternative, so what is offered is a mechanism and a direction of effect, not a magnitude.
- 인용: “for obtaining an inference for a particular task can sometimes be less reliable or accurate than inputting clean, curated, and condensed data for the same query”
- 인용: “Example machine-learned agent systems can reduce a computational load at runtime through pre-processing and storage of high-quality memory data objects.”

## M152

- 배경 문제: The formal BACKGROUND section recites only what a machine-learned model is — a computer receives inputs, processes them with a parameterised model, obtains feedback, updates parameters, and is said to learn. It identifies no prior memory or context-management system and cites no document at all.
- 주장 효과: Every comparative assertion in the filing is instead made in the detailed description against a baseline the applicant characterises there: some traditional agent systems that lack a memory capability, and some possible alternative approaches that expose external data-source interfaces.
- 차이: The delta is defined against an applicant-drawn baseline rather than against identified art. The only external literature cited anywhere in the disclosure supports the generic model machinery — transformer, mixture-of-experts, tokenisation, the applicant's own Gemma, PaliGemma and Gemini papers — and none of it is offered as prior art for the memory mechanism. An examiner's characterisation of the closest art is therefore entirely unanticipated by the document.
- 인용: “A computer can receive input(s).”
- 인용: “some traditional agent systems that lack a memory capability may lead to interruptions or prompts to process additional inputs and render additional outputs to perform a task”

## M153

- 배경 문제: The filing does not position itself against a rival memory architecture. It positions the memory layer against its own model stack operated without one: the sequence processing model is treated throughout as a supplied component, reached through machine-learned model system(s) 118 and described generically at FIG. 12 to FIG. 17, and the surrounding platform, training and inference chapters are shared boilerplate rather than contributed matter.
- 주장 효과: The asserted contribution is the layer around that model — generating, curating, retrieving, updating and forgetting user-specific memory objects — so as to condition an otherwise unmodified sequence processing model on what the user said before.
- 차이: No change to model architecture, training or parameters is claimed. Claim 1 requires only that the model process an input data structure built from the query and the memory data, so the entire delta sits in what enters the prompt and in how that content is maintained between prompts. The timing supports the reading: priority 2024-12-11 from US provisional 63/730,845, PCT filing exactly one Paris year later on 2025-12-11, publication 2026-06-18 as WO2026-128750A1 — a memory-layer filing made from inside an established model programme rather than alongside a model result.
- 인용: “Machine-learned model system(s) 118 can manage and perform execution of one or more machine-learned models based on inputs received from machine-learned agent system 100.”
- 인용: “inputting, by the machine-learned agent system and to a machine-learned sequence processing model, an input data structure based on the query and the memory data”

## 출원인 관심 신호

_등재된 신호가 없다._
