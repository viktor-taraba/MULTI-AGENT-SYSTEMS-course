# What is an embedding?

## Executive summary
An embedding is a learned, dense vector representation of an object (word, sentence, image, user, item, graph node, etc.) that maps that object to a point in a continuous, typically low-dimensional vector space. Embeddings capture semantic and structural relationships: objects that are similar in meaning or role appear close together in the vector space. They are fundamental building blocks for search, recommendation, clustering, classification, and many modern NLP and multimodal systems.

## Definition and intuition
- Definition: An embedding is a numeric vector (array of real numbers) that represents an input item so that geometric relationships between vectors reflect semantic or functional relationships between the original items.
- Intuition: Think of each object as being assigned coordinates in an n-dimensional space. Similar objects cluster together; distances (Euclidean, cosine) or dot products of vectors provide measures of similarity or relevance.
- Why learn embeddings? One-hot or sparse encodings don't capture relationships and are high-dimensional and inefficient. Embeddings compress information into dense vectors that models can use effectively.

## Common types of embeddings
- Word embeddings: represent words (Word2Vec, GloVe, FastText).
- Contextual (token-level) embeddings: produced by transformer models (BERT, GPT) where the same word can have different embeddings depending on context.
- Sentence / document embeddings: fixed-length vectors for longer text (Sentence-BERT, Universal Sentence Encoder).
- Image embeddings: vectors representing images, often from deep CNNs (e.g., ResNet feature vectors).
- Audio embeddings: learned from audio models (e.g., VGGish).
- Graph embeddings: nodes mapped to vectors preserving graph structure (node2vec, DeepWalk, Graph Neural Networks).
- User/item embeddings: in recommender systems, users and items are embedded so their dot product predicts preference.

## How embeddings are created (short overview)
- Embedding layer in a neural network: categorical inputs (IDs) map to trainable dense vectors learned via gradient descent.
- Shallow algorithms: Word2Vec (skip-gram, CBOW) learns word vectors by predicting context; GloVe uses global co-occurrence statistics.
- Subword embeddings: FastText builds embeddings from character n-grams to handle rare or morphologically rich words.
- Contextual embeddings: Large transformer models produce context-dependent token vectors; sentence-level vectors are obtained by pooling or specialized sentence-transformer training.
- Contrastive and metric-learning approaches: models trained to pull semantically related examples together and push unrelated ones apart (used for modern sentence/image embeddings).

## Mathematical properties and similarity measures
- Embedding dimensionality: typically tens to thousands of dimensions depending on task and model capacity.
- Similarity measures: cosine similarity is widely used; dot product or Euclidean distance are alternatives depending on normalization.
- Normalization: cosine similarity is equivalent to dot product of L2-normalized vectors, which is commonly applied to control magnitude effects.

## Practical applications
- Semantic search and information retrieval: retrieve documents by nearest-neighbor search in embedding space.
- Retrieval-Augmented Generation (RAG): find relevant context passages for LLMs.
- Recommendation systems: compute scores from user/item embeddings.
- Clustering and visualization: group similar objects; use t-SNE/UMAP for 2D visualization.
- Transfer learning and feature extraction: use pretrained embeddings as input features for downstream tasks.
- Anomaly and fraud detection: embeddings reveal unusual patterns.

## Implementation notes and best practices
- Pretrained vs. task-specific: pretrained embeddings speed development and generalize; fine-tune when domain shift is large.
- Dimensionality trade-off: higher dims may capture more nuance but increase storage and compute (and risk overfitting).
- Distance metric: choose cosine for semantic tasks; dot product for recommendation scoring if magnitudes carry meaning.
- ANN for scale: use approximate nearest neighbor libraries (FAISS, Annoy, Milvus, Qdrant) for efficient retrieval.
- Normalization: often L2-normalize embeddings when using cosine similarity.
- Handling out-of-vocabulary: use subword methods (FastText) or fallback embedding vectors.

## Evaluation
- Intrinsic evaluations: word similarity tasks, analogy tasks, cluster quality.
- Extrinsic evaluations: performance on downstream tasks (classification, retrieval, recommendation).
- Ablations and robustness: test sensitivity to dimensionality, normalization, and domain drift.

## Limitations and risks
- Bias: embeddings can encode and amplify societal biases present in training data.
- Privacy: embeddings derived from private data may leak sensitive information if not protected.
- Domain mismatch: pretrained embeddings may perform poorly on specialized domains without fine-tuning.
- Interpretability: embeddings are dense and not easily interpretable by humans.

## Quick examples
- Word2Vec: similar words like "king" and "queen" are nearby; vector arithmetic can reflect analogies (king - man + woman ≈ queen).
- Sentence-BERT: semantically related sentences have high cosine similarity, enabling better sentence-level retrieval than averaging token embeddings.

## Further reading / Sources
- IBM: What is embedding? — https://www.ibm.com/think/topics/embedding
- Google Developers: Embeddings (Machine Learning Crash Course) — https://developers.google.com/machine-learning/crash-course/embeddings


## Appendix: short glossary
- Embedding vector: the numeric vector representing an object.
- One-hot encoding: sparse vector with a single 1 representing a categorical value.
- Contextual embedding: token embedding that depends on surrounding tokens.
- ANN: approximate nearest neighbor, used to scale nearest-neighbor searches.


Sources
- https://www.ibm.com/think/topics/embedding
- https://developers.google.com/machine-learning/crash-course/embeddings