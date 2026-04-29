# Step-by-step example of embedding calculation (Skip-gram Word2Vec)

This document walks through a compact, numerical, step-by-step example of how the skip-gram Word2Vec model computes embeddings and updates weights for a single (center, context) training pair using a full softmax objective (suitable for small vocabularies). It also briefly explains the negative-sampling alternative.

---

## 1) Problem setup and notation

- Vocabulary (V = 4): ["I", "like", "cats", "dogs"] with indices 0..3.
- Embedding dimension (D) = 2.
- Input-to-hidden weight matrix W_in (shape V x D): each row is the embedding for a word (used as "center" embeddings).
- Hidden-to-output weight matrix W_out (shape D x V): columns are the output vectors for each vocabulary word.
- Model: For a center word c and candidate output word w, score_j = v_c^T u_j where v_c is W_in[c] (1 x D) and u_j is column j of W_out (D x 1). Softmax over scores gives probability that j is in the context.
- Learning rate (alpha) = 0.1 for the example.

Initial weights (chosen small for clarity):

W_in =
[ [0.20, 0.10],   # index 0: "I"
  [0.00, 0.30],   # index 1: "like"
  [0.40, 0.20],   # index 2: "cats"  <-- center word in this example
  [0.10, -0.20] ] # index 3: "dogs"

W_out =
[ [ 0.30,  0.10, -0.20,  0.00],   # first row (D=2)
  [ 0.00,  0.20,  0.40, -0.10] ]  # second row

Center word: "cats" (index 2). True context word for this training example: "like" (index 1).

---

## 2) Forward pass: compute scores and softmax probabilities

1. Hidden (embedding for center):
   v_c = W_in[2] = [0.40, 0.20]

2. Scores for all vocabulary words: scores = v_c dot W_out (1 x V)

   - score_0 = 0.40*0.30 + 0.20*0.00 = 0.12
   - score_1 = 0.40*0.10 + 0.20*0.20 = 0.04 + 0.04 = 0.08
   - score_2 = 0.40*(-0.20) + 0.20*0.40 = -0.08 + 0.08 = 0.00
   - score_3 = 0.40*0.00 + 0.20*(-0.10) = -0.02

   scores = [0.12, 0.08, 0.00, -0.02]

3. Softmax probabilities (p_j = exp(score_j) / sum_k exp(score_k)):

   - exp(scores) ≈ [1.1275, 1.0833, 1.0000, 0.9802]
   - sum ≈ 4.1910

   Probabilities:
   - p_0 ≈ 1.1275 / 4.1910 = 0.2690
   - p_1 ≈ 1.0833 / 4.1910 = 0.2585
   - p_2 ≈ 1.0000 / 4.1910 = 0.2386
   - p_3 ≈ 0.9802 / 4.1910 = 0.2339

   p = [0.2690, 0.2585, 0.2386, 0.2339]

4. Loss for this positive (center, context) pair (cross-entropy):
   - target is index 1 ("like"); loss L = -log(p_1) ≈ -log(0.2585) ≈ 1.351

---

## 3) Backpropagation: gradients

Define vector of errors at output (dScores) as: dScores = p - y where y is one-hot for the true context.

- y = [0, 1, 0, 0]
- dScores = [0.2690, 0.2585 - 1 = -0.7415, 0.2386, 0.2339]
          ≈ [ 0.2690, -0.7415, 0.2386, 0.2339 ]

Gradients for W_out (shape D x V):
- For each vocabulary index j, grad W_out[:, j] = v_c * dScores[j]

Compute per-column:
- grad_col0 = [0.40 * 0.2690, 0.20 * 0.2690] = [0.1076, 0.0538]
- grad_col1 = [0.40 * (-0.7415), 0.20 * (-0.7415)] = [-0.2966, -0.1483]
- grad_col2 = [0.40 * 0.2386, 0.20 * 0.2386] = [0.0954, 0.0477]
- grad_col3 = [0.40 * 0.2339, 0.20 * 0.2339] = [0.0936, 0.0468]

So dW_out ≈
[ [ 0.1076, -0.2966,  0.0954,  0.0936],
  [ 0.0538, -0.1483,  0.0477,  0.0468] ]

Gradient for W_in row corresponding to the center word (index 2):
- dHidden = sum_j dScores[j] * u_j  (where u_j is W_out column j)

W_out columns (u_j):
- u_0 = [0.30, 0.00]
- u_1 = [0.10, 0.20]
- u_2 = [-0.20, 0.40]
- u_3 = [0.00, -0.10]

Compute dHidden:
- term0 = 0.2690 * [0.30, 0.00] = [ 0.0807 , 0.0000 ]
- term1 = -0.7415 * [0.10, 0.20] = [-0.07415, -0.14830]
- term2 = 0.2386 * [-0.20, 0.40] = [-0.04772, 0.09544]
- term3 = 0.2339 * [0.00, -0.10] = [ 0.00000, -0.02339]

Sum:
- dHidden_x ≈ 0.0807 - 0.07415 - 0.04772 + 0 = -0.04117
- dHidden_y ≈ 0 - 0.14830 + 0.09544 - 0.02339 = -0.07625

So dW_in[2] = dHidden ≈ [-0.04117, -0.07625]. All other rows in dW_in are zero for this single pair because input is one-hot.

---

## 4) Parameter update (one SGD step)

Using learning rate alpha = 0.1,

- W_out_new = W_out - alpha * dW_out

  Example updates (first column, first row):
  - W_out[0,0] new = 0.30 - 0.1*0.1076 = 0.30 - 0.01076 = 0.28924

  You can apply this to all entries; for illustration, update W_out and W_in[2]:

- W_in[2] new = W_in[2] - alpha * dW_in[2]
  - W_in[2]_new = [0.40, 0.20] - 0.1 * [-0.04117, -0.07625]
                = [0.40 + 0.00412, 0.20 + 0.00763]
                ≈ [0.40412, 0.20763]

After the update the center embedding has shifted slightly so it will produce different scores next time it sees similar contexts.

---

## 5) Short note on Negative Sampling (practical for large vocabularies)

- Full softmax computes scores across all V entries (expensive when V is large). Negative sampling turns the multi-class problem into multiple binary classification tasks.
- For a positive pair (c, o) and K negative samples {n1..nK}, the negative-sampling loss is:
  L = -log(σ(u_o^T v_c)) - sum_{k=1..K} log(σ(-u_{n_k}^T v_c))
  where σ(x) is the sigmoid function.
- Gradients only involve the output vectors of the positive and the sampled negatives (K+1 columns), dramatically reducing cost.

Numeric sketch (K=2): if u_o^T v_c = 0.08 and u_n^T v_c = -0.05 for a negative sample, then
- σ(0.08) ≈ 0.5199, -log(σ(0.08)) ≈ 0.653
- σ(-(-0.05)) = σ(0.05) ≈ 0.5125, -log(σ(0.05)) ≈ 0.668
Gradients computed via (σ(x)-1) or σ(x) depending on positive/negative term and applied only to those few vectors.

---

## 6) Practical notes and tips

- The presented numeric example uses full softmax for clarity. Real Word2Vec implementations typically use negative sampling or hierarchical softmax for speed.
- Embedding dimension D is a hyperparameter (commonly 50--300). Larger D captures more nuance but needs more data.
- Window size controls syntactic (small) vs semantic (large) relationships.
- After training, the input matrix W_in rows (or sometimes W_in + W_out averaged) are used as the word embeddings.
- Normalize embeddings (e.g., unit vectors) before computing cosine similarities for downstream tasks.

---

## 7) Quick worked-check summary (numbers)

- Initial score vector: [0.12, 0.08, 0.00, -0.02]
- Softmax probs: [0.2690, 0.2585, 0.2386, 0.2339]
- Loss: ≈ 1.351 (for target = index 1)
- dScores: [0.2690, -0.7415, 0.2386, 0.2339]
- dW_out (D x V):
  [ [ 0.1076, -0.2966, 0.0954, 0.0936],
    [ 0.0538, -0.1483, 0.0477, 0.0468] ]
- dW_in[2] (for center word "cats") ≈ [-0.04117, -0.07625]
- Updated W_in[2] (alpha=0.1): ≈ [0.40412, 0.20763]

---

## Sources

- TensorFlow Word2Vec tutorial (skip-gram & negative sampling): https://www.tensorflow.org/text/tutorials/word2vec
- Skip-gram model explanation and derivation: https://mbrenndoerfer.com/writing/skip-gram-model-word2vec-word-embeddings

