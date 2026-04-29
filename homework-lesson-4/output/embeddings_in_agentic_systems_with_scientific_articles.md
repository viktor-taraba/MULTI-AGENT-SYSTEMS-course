Embeddings in Agentic Systems — Continued research (scientific articles)

Date: 2026-03-22

Executive summary

This continuation augments the prior engineer-focused brief with a curated set of scientific articles (peer-reviewed and preprints) that directly study embeddings for retrieval, policy/skill conditioning, and memory in agentic systems. Key findings reinforced by the literature:

- Retrieval + dense embeddings is a mature and effective pattern for augmenting agents (REALM, RAG, DPR). These papers formalize pretraining and dense-retrieval methods that power RAG-style augmentation used by modern agents.
- Policy- and skill-level latent embeddings (e.g., Disentangled Skill Embeddings, policy latent generation) provide compact representations for transfer, hierarchical RL, and behavior retrieval; they are an active research area with both theoretical formulations and algorithmic variants.
- Embedding-based policy retrieval at the behavior/policy level (policy memory banks, retrieval-augmented embodied agents) is an emerging direction for embodied/robotic agents and demonstrates improved sample efficiency and transfer across embodiments.

Annotated list of scientific articles (selected)

1) Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — Patrick Lewis et al., NeurIPS/ArXiv (2020)
- Link: https://arxiv.org/pdf/2005.11401.pdf
- Why it matters: Introduced a practical, end-to-end RAG formulation that combines pre-trained seq2seq generators with dense retrievers (using DPR). It formalizes marginalization over retrieved documents and shows how retrieval can be integrated into generation — the foundation for RAG agents and many production RAG systems.

2) Dense Passage Retrieval for Open-Domain Question Answering — Vladimir Karpukhin et al., arXiv (2020)
- Link: https://arxiv.org/pdf/2004.04906.pdf
- Why it matters: Presents DPR (dual-encoder dense retrieval), which demonstrated dense embedding retrieval outperforming BM25 on open-domain QA. DPR is a standard retriever used in RAG pipelines and in agent memory systems where retrieval precision affects downstream decisions.

3) REALM: Retrieval-Augmented Language Model Pre-Training — Kelvin Guu et al., ICML (2020)
- Link: https://proceedings.mlr.press/v119/guu20a/guu20a.pdf
- Why it matters: REALM shows how to integrate retrieval into pre-training (latent variable formulation) and train a retriever end-to-end from unsupervised language modeling objectives. It influenced subsequent pretraining strategies for retrieval-augmented models.

4) Disentangled Skill Embeddings for Reinforcement Learning — Janith C. Petangoda et al., arXiv (2019)
- Link: https://arxiv.org/pdf/1906.09223.pdf
- Why it matters: Proposes a variational multi-task RL framework that learns disentangled latent embeddings for dynamics and goals. Skill embeddings enable generalization across dynamics and goals and support hierarchical RL — a concrete instance of skill/policy embeddings for agentic systems.

5) Retrieval-Augmented Embodied Agents (RAEA) — Yichen Zhu et al., CVPR (2024)
- Link: https://openaccess.thecvf.com/content/CVPR2024/papers/Zhu_Retrieval-Augmented_Embodied_Agents_CVPR_2024_paper.pdf
- Why it matters: Demonstrates retrieval at the policy level: a policy memory bank stores multi-embodiment behavior fragments; a policy retriever finds relevant behavior/policy candidates and a policy generator integrates them for action prediction. This paper is a direct example of embeddings powering agentic memory in robotics.

6) Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG — Aditi Singh et al., arXiv (2025)
- Link: https://arxiv.org/pdf/2501.09136.pdf
- Why it matters: A recent survey that conceptualizes RAG as an agentic process; highlights agentic design patterns (reflection, planning, tool use) where retrieval is actively managed by agents. Useful for framing research directions and taxonomies.

7) Policy Generation from Latent Embeddings for Reinforcement Learning — Conference paper (Springer; proceedings)
- Link (PDF): https://link.springer.com/content/pdf/10.1007/978-3-031-46338-9_12.pdf
- Why it matters: Investigates generative models trained to produce policy parameters from latent embeddings — a direction that treats policies as generative objects in an embedding space, enabling conditional sampling of controllers/policies.

Additional related research and context papers

- Memory, episodic retrieval and embedding methods in RL and agents: literature on memory-augmented neural networks, episodic control, and experience replay often uses learned embeddings for similarity and retrieval. (See references cited within the RAEA and DSE papers.)
- Recent papers on unsupervised skill discovery, latent plan/trajectory embeddings, and foundation-model-guided skill discovery (2024–2025) are expanding the space of embedding types used by agents (trajectory, motor primitives, multimodal embeddings).

Key technical syntheses and implications for agent designers

- Retrieval precision drives downstream performance: improvements in dense retriever training (DPR, REALM pretraining techniques) map directly to more useful context for planners and LLM controllers.
- Multiple embedding spaces are often needed: text embeddings (SBERT/OpenAI-style), multimodal embeddings (CLIP-like), and policy/trajectory embeddings (transformer or contrastive encoders) each serve different agent modules; aligning or mapping between these spaces is an important engineering and research task.
- Policy/skill-level retrieval complements RAG: retrieving behavior fragments or latent skill vectors (rather than textual documents) reduces sample complexity in robotics and enables reuse and composition of behaviors across tasks and embodiments.
- Evaluation should be downstream-driven: retrieval metrics (recall@k) are necessary but not sufficient—agents need task-level metrics (success rate, safety constraints, cost, latency) to determine whether embedding choices help.

Practical next steps (research agenda)

- Replicate RAEA-style pipeline on a small multi-embodiment dataset: build a policy memory bank, learn behavior/trajectory embeddings, and measure transfer.
- Experiment with joint vs. separate embedding spaces for text, vision, and action: evaluate retrieval quality and how well retrieved candidates improve planning.
- Investigate embedding migration strategies for model upgrades: dual-indexing and progressive re-embedding to avoid catastrophic retrieval drift.
- Survey & benchmark recent unsupervised skill discovery and policy-generation-from-latent works (2023–2026) to identify methods with best transfer/sample-efficiency tradeoffs.

Sources

- Yichen Zhu et al., "Retrieval-Augmented Embodied Agents", CVPR 2024. PDF: https://openaccess.thecvf.com/content/CVPR2024/papers/Zhu_Retrieval-Augmented_Embodied_Agents_CVPR_2024_paper.pdf
- Aditi Singh et al., "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG", arXiv:2501.09136. PDF: https://arxiv.org/pdf/2501.09136.pdf
- Patrick Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS/ArXiv (2020). PDF: https://arxiv.org/pdf/2005.11401.pdf
- Vladimir Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering", arXiv (2020). PDF: https://arxiv.org/pdf/2004.04906.pdf
- Kelvin Guu et al., "REALM: Retrieval-Augmented Language Model Pre-Training", ICML (2020). PDF: https://proceedings.mlr.press/v119/guu20a/guu20a.pdf
- Janith C. Petangoda et al., "Disentangled Skill Embeddings for Reinforcement Learning", arXiv (2019). PDF: https://arxiv.org/pdf/1906.09223.pdf
- "Policy Generation from Latent Embeddings for Reinforcement Learning" (conference paper). PDF: https://link.springer.com/content/pdf/10.1007/978-3-031-46338-9_12.pdf
- LangChain RAG documentation (engineering guide): https://docs.langchain.com/oss/python/langchain/rag

(End of document)
