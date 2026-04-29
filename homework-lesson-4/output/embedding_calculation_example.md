Embedding calculation — worked examples

Executive summary

This report explains how common vector embeddings are calculated and updated, with two worked numerical examples: (1) a one-step Word2Vec (skip-gram) forward/backward pass and parameter update on a tiny vocabulary, and (2) a TF–IDF document-vector example with cosine-similarity calculations. The Word2Vec example shows the hidden-layer extraction, softmax probability calculation, gradient computation, and a single-step SGD update (numerical values included). The TF–IDF example contrasts raw term-frequency similarity with IDF-weighted results to illustrate the effect of rare terms.

Background: what is an embedding

- An embedding is a dense numeric vector that represents an object (word, sentence, image, etc.) so that similar objects are close in vector space.
- Word2Vec (skip-gram and CBOW) produces word embeddings by training a neural model to predict context words; after training, the learned weight rows (center vectors) are used as embeddings.
- TF–IDF produces sparse vector representations of documents based on term frequency and inverse document frequency; these are commonly used as baseline "embeddings" for documents.

Worked example 1 — Word2Vec (skip-gram) single-update numeric walkthrough

Setup (toy model)

- Vocabulary V = {I, love, NLP, cats} with indices {0,1,2,3}.
- Embedding dimension N = 2.
- Center-word weight matrix W (rows = center vectors v_i):
  - v_I = [0.20, -0.10]
  - v_love = [0.00, 0.30]
  - v_NLP = [0.40, 0.10]
  - v_cats = [-0.20, 0.00]
- Context-word weight matrix W' (columns = context vectors u_j):
  - u_I = [0.10, 0.00]
  - u_love = [0.00, 0.20]
  - u_NLP = [0.30, 0.10]
  - u_cats = [-0.10, 0.05]
- Learning rate lr = 0.1.
- Training instance: center = "love" (index 1), true context = "NLP" (index 2).

Forward pass

1. Hidden vector h is the center-row from W (because input is one-hot):
   h = v_love = [0.00, 0.30].
2. Compute scores s_j = u_j · h for each context word j:
   - s_I = u_I · h = [0.10,0.00]·[0.00,0.30] = 0.0000
   - s_love = u_love · h = [0.00,0.20]·[0.00,0.30] = 0.0600
   - s_NLP = u_NLP · h = [0.30,0.10]·[0.00,0.30] = 0.0300
   - s_cats = u_cats · h = [-0.10,0.05]·[0.00,0.30] = 0.0150
3. Softmax probabilities p_j = exp(s_j) / sum_k exp(s_k):
   - exp(0.0000)=1.000000
   - exp(0.0600)=1.061836
   - exp(0.0300)=1.030455
   - exp(0.0150)=1.015113
   - sum ≈ 4.107404
   - p_I ≈ 1/4.107404 = 0.2434
   - p_love ≈ 1.061836/4.107404 = 0.2585
   - p_NLP ≈ 1.030455/4.107404 = 0.2508
   - p_cats ≈ 1.015113/4.107404 = 0.2472
4. Loss for this target (negative log-likelihood): L = -log p_true = -log p_NLP ≈ -log(0.2508) ≈ 1.383.

Backward pass (gradients)

Softmax + cross-entropy yields gradients on scores: g_j = p_j - t_j (where t_j is 1 for the true class, 0 otherwise).

- g_I = 0.2434 - 0 = +0.2434
- g_love = 0.2585 - 0 = +0.2585
- g_NLP = 0.2508 - 1 = -0.7492
- g_cats = 0.2472 - 0 = +0.2472

Gradients w.r.t. context vectors u_j: ∂L/∂u_j = g_j * h

- ∂L/∂u_I = 0.2434 * [0.0,0.3] = [0.0000, 0.07302]
- ∂L/∂u_love = 0.2585 * [0.0,0.3] = [0.0000, 0.07755]
- ∂L/∂u_NLP = -0.7492 * [0.0,0.3] = [0.0000, -0.22476]
- ∂L/∂u_cats = 0.2472 * [0.0,0.3] = [0.0000, 0.07416]

Gradient w.r.t. hidden vector h: ∂L/∂h = sum_j g_j * u_j

Compute each g_j * u_j:
- 0.2434 * u_I = [0.02434, 0.00000]
- 0.2585 * u_love = [0.00000, 0.05170]
- -0.7492 * u_NLP = [-0.22476, -0.07492]
- 0.2472 * u_cats = [-0.02472, 0.01236]
Sum => ∂L/∂h ≈ [-0.22514, -0.01086].

Gradient w.r.t. center-row v_love (because h equals that row): ∂L/∂v_love = ∂L/∂h.

Parameter updates (SGD with lr=0.1)

- Update center vector v_love := v_love - lr * ∂L/∂v_love
  - v_love_new = [0.00, 0.30] - 0.1 * [-0.22514, -0.01086] = [0.022514, 0.301086]

- Update context vectors u_j := u_j - lr * ∂L/∂u_j
  - u_I_new = [0.10, 0.00] - 0.1*[0.0000,0.07302] = [0.10, -0.007302]
  - u_love_new = [0.00, 0.20] - 0.1*[0.0000,0.07755] = [0.00, 0.192245]
  - u_NLP_new = [0.30, 0.10] - 0.1*[0.0000,-0.22476] = [0.30, 0.122476]
  - u_cats_new = [-0.10, 0.05] - 0.1*[0.0000,0.07416] = [-0.10, 0.042584]

Effect on similarity (illustrative)

- Cosine(v_love_initial, v_NLP) = (0*0.4 + 0.3*0.1) / (||v_love|| * ||v_NLP||) ≈ 0.2426
- Cosine(v_love_new, v_NLP) ≈ 0.3141

The cosine similarity increased after the update (the model moved v_love slightly closer to v_NLP), which matches the training signal that "NLP" is a context word for "love" in this instance.

Notes about practical Word2Vec training

- The plain softmax across all vocabulary items is expensive for large V; implementations use negative sampling or hierarchical softmax to approximate the gradient efficiently.
- After training, practitioners typically use the center-word vector matrix (rows of W) as the final word embeddings.
- Embeddings are learned by many stochastic updates; the example above shows one step to illustrate mechanics.

Worked example 2 — TF–IDF document vectors and cosine similarity

Corpus: two documents
- doc1: "I love cats"
- doc2: "I love NLP"

Vocabulary: {I, love, cats, NLP}

Raw term-frequency vectors (TF):
- doc1: [1, 1, 1, 0]
- doc2: [1, 1, 0, 1]

Cosine similarity on TF vectors:
- dot(doc1, doc2) = 1*1 + 1*1 + 1*0 + 0*1 = 2
- ||doc1|| = sqrt(1+1+1) = sqrt(3) ≈ 1.732; ||doc2|| = sqrt(3) ≈ 1.732
- cosine = 2 / (1.732*1.732) = 2/3 ≈ 0.6667

IDF (inverse document frequency) with N=2 documents:
- idf(I) = log(2/2) = 0
- idf(love) = log(2/2) = 0
- idf(cats) = log(2/1) = 0.6931
- idf(NLP) = log(2/1) = 0.6931

TF–IDF vectors (TF * IDF):
- doc1: [0, 0, 0.6931, 0]
- doc2: [0, 0, 0, 0.6931]

Cosine similarity on TF–IDF vectors:
- dot = 0 (no shared weighted terms)
- cosine = 0

Interpretation: raw TF shows a relatively high similarity because of the stop-like words "I" and "love". IDF downweights frequent terms and thus emphasizes rare, discriminative terms, producing zero similarity here because the two documents share only high-frequency (idf≈0) tokens.

Additional quick notes and common operations

- Sentence / document embeddings from word embeddings: common simple approach is to average word vectors or use weighted averages (e.g., by TF–IDF or Smooth Inverse Frequency). More advanced methods use transformer-based sentence encoders (e.g., SBERT).
- Similarity measure: cosine similarity is the most common (cosine = dot(a,b) / (||a||*||b||)).
- Analogy: with quality embeddings, vector arithmetic often reveals analogies: v(king) - v(man) + v(woman) ≈ v(queen).

Minimal pseudocode (skip-gram, single example)

1. x = one_hot(center_index)
2. h = W[center_index]
3. scores = W'_T dot h  # length |V|
4. p = softmax(scores)
5. loss = -log p[target_index]
6. g = p; g[target_index] -= 1
7. for j in 0..V-1: W'[:,j] -= lr * g[j] * h
8. W[center_index] -= lr * (sum_j g[j] * W'[:,j])

Sources

- Dive into Deep Learning (word2vec chapter): https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html
- "Word2Vec Tutorial Part I: The Skip-Gram Model" (Alex Minnaar / Chris McCormick-style tutorial): http://mccormickml.com/assets/word2vec/Alex_Minnaar_Word2Vec_Tutorial_Part_I_The_Skip-Gram_Model.pdf

