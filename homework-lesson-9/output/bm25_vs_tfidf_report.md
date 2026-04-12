# Executive Summary
BM25 and TF-IDF are related term-weighting/scoring families but come from different models and behave differently in practice. TF-IDF (vector-space style) multiplies a term-frequency (TF) factor by an inverse-document-frequency (IDF) factor (often using ln(N/n)) and typically scores documents by dot product with the query vector; TF scales linearly with raw counts (or with sublinear transforms such as log TF) and document-length handling is ad-hoc or via normalization. BM25 (Okapi/BM25) is derived from the probabilistic relevance framework (RSJ / Binary Independence idea) and replaces linear TF with a saturating TF formula, introduces principled length normalization via parameters k1 and b, and uses an RSJ-style IDF. In short: TF-IDF = simple linear weighting (optionally with log TF and normalization); BM25 = TF-IDF-like structure but with TF saturation + length-normalization + RSJ IDF (and tunable parameters) that usually produces better retrieval ranking out of the box for ad-hoc search. Below you will find formal definitions, intuitions, parameter defaults, a worked numeric example on the requested corpus, a comparison table, pros/cons/use cases, authoritative references, and an appendix with implementation notes and recommended hyperparameter ranges.

---

# 1. Formal definitions and formulas (with variable definitions)
Notation (used in all formulas)
- N : total number of documents in the collection
- n(t) : document frequency of term t (number of documents that contain t)
- tf_{t,d} : raw term frequency of term t in document d (count of occurrences)
- |d| : document length measured in terms (number of tokens in d)
- avgdl : average document length = (1/N) * sum_{d}|d|
- q_t or tf_{t,q} : term frequency of term t in the query (often small; many retrieval systems treat query tf as binary or apply small smoothing)
- ln(·) : natural logarithm

1.1 TF variants
- Raw TF (linear):
  Equation (TF-raw)
  tf_{t,d} = count of term t in document d

- Log (sublinear) TF: (common choice to dampen large counts)
  Equation (TF-log)
  tf_{t,d}^{(log)} = \begin{cases} 0 & \text{if } tf_{t,d} = 0 \\ 1 + \ln(tf_{t,d}) & \text{if } tf_{t,d} > 0 \end{cases}
  (some variants use ln(1 + tf) instead; we use 1+ln(tf) because it keeps tf=1 -> 1)

1.2 IDF variants
- Classic IDF (logarithmic):
  Equation (IDF-classic)
  idf_{classic}(t) = \ln\frac{N}{n(t)}
  - Many authors add smoothing to avoid division by zero or tiny denominators when n(t)=0.

- Smoothed IDF (add-1 style or +0.5 smoothing):
  Equation (IDF-smoothed)
  idf_{smooth}(t) = \ln\frac{1 + N}{1 + n(t)}  \quad\text{(or variants like } \ln\frac{N}{1 + n(t)}\text{)}

- RSJ / Robertson-Sparck-Jones IDF (used by BM25 family):
  Equation (IDF-RSJ)
  idf_{RSJ}(t) = \ln\frac{N - n(t) + 0.5}{n(t) + 0.5}
  - This originates in the probabilistic relevance framework and can be negative when n(t) > N/2.
  - Many production systems clamp negative RSJ-IDF to 0 or use BM25+ to avoid negative or overly penalizing common terms.

1.3 TF–IDF (two common variants)
- Raw TF \u00d7 Classic IDF (document weight):
  Equation (TFIDF-raw)
  w_{t,d} = tf_{t,d} \cdot idf_{classic}(t)

- Log-TF variant (document weight):
  Equation (TFIDF-log)
  w_{t,d} = tf_{t,d}^{(log)} \cdot idf_{classic}(t)    \quad\text{where } tf_{t,d}^{(log)} = 1 + \ln(tf_{t,d}) \text{ for } tf>0

Scoring a document for query Q in basic vector-space TF-IDF (simple dot product, query tf=1 per term):
  Equation (TFIDF-score)
  score(d,Q) = \sum_{t\in Q} tf_{t,d} \cdot idf_{classic}(t) \cdot tf_{t,Q}  (often tf_{t,Q}=1)

Notes: classic TF-IDF can be combined with document length normalization (L2 normalization of the full vector) or pivoted normalization — these are added components and not intrinsic to the simplest TF-IDF formula.

1.4 BM25 (Okapi BM25) — standard formula
BM25 computes a score as the sum over query terms of term contributions:
  Equation (BM25)
  score_{BM25}(d,Q) = \sum_{t\in Q} idf_{RSJ}(t) \cdot \frac{tf_{t,d} \cdot (k_1 + 1)}{tf_{t,d} + k_1 \cdot (1 - b + b \cdot |d|/avgdl)}

Where:
- idf_{RSJ}(t) = ln((N - n(t) + 0.5)/(n(t) + 0.5))  (Eq. IDF-RSJ)
- k1 : controls TF saturation (typical values ~1.2–1.5)
- b : controls document length normalization (0 <= b <= 1; typical value ~0.75)
- avgdl : average document length

Important notes: many implementations clamp negative idf_{RSJ} to 0 (i.e., idf = max(idf_{RSJ}, 0)) to avoid penalizing documents for containing common query terms. BM25+ is a variant that adds a delta to the numerator so that documents always get a minimum positive contribution for a matching term (prevents short documents from being outranked too much by long docs that match). BM25F is an extension to multiple weighted fields (title, body, anchor text) where field-specific TF and length normalization are combined.

1.5 BM25+ (sketch)
BM25+ aims to remove the undesirable negative score behavior for very frequent terms and introduces a small delta \u03b4 > 0 added in the TF numerator term to ensure a floor contribution:
  Equation (BM25+)
  contribution_{t} = idf_{RSJ}(t) \cdot \left( \frac{tf_{t,d} (k_1 + 1)}{tf_{t,d} + k_1 (1 - b + b |d|/avgdl)} + \u03b4 \right)
Typical \u03b4 values are small (e.g., 1.0 in some descriptions) but tuneable. An alternative production shortcut is simply clamping idf to zero for negative RSJ-IDF.

1.6 BM25F (sketch)
BM25F extends BM25 to multiple weighted fields: each field f has its own tf_{t,d,f} and length normalization, then per-term contributions are computed from a combined field-level tf (often a weighted sum) and then fed into BM25 formula. This is how search engines give more weight to title matches, for example.

---

# 2. Intuitions for components
- TF (term frequency): indicates how often a term occurs in a document. Intuition: more occurrences -> likely more about the term. Raw TF is linear (each extra occurrence increases weight proportionally); log TF reduces the marginal effect of repeated occurrences (dampening).

- IDF (inverse document frequency): punishes common terms (stop-words) and promotes rare, discriminative terms. In classic TF-IDF, idf = ln(N/n) increases for rare terms. In RSJ-IDF, the ratio (N - n + 0.5)/(n + 0.5) comes from a probabilistic view comparing odds of term appearing in relevant vs non-relevant sets; it can be negative if term appears in most documents.

- Length normalization: longer documents tend to have larger raw TFs simply because they contain more tokens. BM25 handles document length with the (1 - b + b * |d|/avgdl) factor (b[0,1]). If b=0 length has no effect; b=1 full pivot normalization (proportional to length).

- Saturation: BM25 uses a saturating TF formula (nonlinear) so that the marginal benefit from additional term occurrences falls as tf increases. This prevents overly long documents stuffed with a term from dominating the score.

- Probabilistic vs Vector-space interpretation:
  - TF-IDF is naturally viewed in a vector-space model: documents and queries are vectors of term weights and relevance is the cosine/dot product. Its IDF is heuristic from distributional arguments.
  - BM25 is derived from the probabilistic relevance framework (PRF / Binary Independence Model); RSJ-IDF originates from odds ratio reasoning about term presence in relevant vs non-relevant sets. However, BM25 can be read as a TF-IDF-like scoring function with principled TF saturation and length normalization.

---

# 3. Default parameter values used in common implementations
- Lucene / Solr / Elasticsearch (common defaults): k1 = 1.2, b = 0.75 (Lucene historically used 1.2; some papers and practitioners prefer k1=1.5). Elasticsearch docs note default k1 = 1.2 and b = 0.75.
- Common alternative setting quoted in literature and practice: k1 = 1.5 and b = 0.75 (we use k1=1.5, b=0.75 for the main worked example per your request; note Lucene default = 1.2).
- BM25+: introduces delta (\u03b4) (often small, e.g. 1.0 or tuned between 0 and 1 depending on implementation).
- BM25F: introduces per-field boosts and per-field b,f and k1 choices, typically tuned per-field.

References for defaults: Lucene BM25Similarity docs and Elasticsearch similarity settings (see Sources).

---

# 4. Worked numeric example (step-by-step) 	6 corpus and query provided
Corpus (tokenization is whitespace; we count terms exactly as tokens):
- D1 = "the cat sat on the mat"  -> tokens: [the, cat, sat, on, the, mat]  -> |D1| = 6
  term counts: the:2, cat:1, sat:1, on:1, mat:1
- D2 = "the quick brown fox jumped over the lazy dog"  -> tokens: [the, quick, brown, fox, jumped, over, the, lazy, dog] -> |D2| = 9
  term counts: the:2, others:1
- D3 = "the cat chased the mouse" -> tokens: [the, cat, chased, the, mouse] -> |D3| = 5
  term counts: the:2, cat:1, chased:1, mouse:1
Query Q = "cat mouse" -> query terms: {cat, mouse}

Collection statistics:
- N = 3
- n(cat) = 2 (appears in D1 and D3)
- n(mouse) = 1 (appears only in D3)
- avgdl = (6 + 9 + 5) / 3 = 20 / 3 = 6.666666666666667

Natural logs used (to 12 decimal places where shown):
- ln(3/2) = ln(1.5) = 0.405465108108
- ln(3) = 1.098612288668
- RSJ idf(cat) = ln((3 - 2 + 0.5) / (2 + 0.5)) = ln(1.5 / 2.5) = ln(0.6) = -0.510825623766
- RSJ idf(mouse) = ln((3 - 1 + 0.5) / (1 + 0.5)) = ln(2.5 / 1.5) = ln(1.666666666667) = 0.510825623766

Decimal values saved as:
- IDF_classic(cat) = 0.4054651081081644
- IDF_classic(mouse) = 1.0986122886681098
- IDF_RSJ(cat) = -0.5108256237659907
- IDF_RSJ(mouse) = +0.5108256237659907
- avgdl = 6.666666666666667

We will compute:
A) TF-IDF with classic idf ln(N/n): (both raw TF and log TF versions)
B) BM25 with RSJ idf (k1=1.5, b=0.75) 	6 detailed term contributions
C) BM25 where negative RSJ idf is clamped to zero (production common practice) and show how rankings change

---

## 4.A TF-IDF (classic idf = ln(N/n)) 	6 raw TF and log TF
We will use the simple dot-product scoring scheme where query tf is 1 for each query term. So score(d,Q) = sum_{t in Q} (tf_{t,d} * idf_classic(t)).

Term counts per doc for query terms:
- D1: tf(cat)=1, tf(mouse)=0
- D2: tf(cat)=0, tf(mouse)=0
- D3: tf(cat)=1, tf(mouse)=1

IDF numbers (classic):
- idf_classic(cat) = ln(3/2) = 0.4054651081081644
- idf_classic(mouse) = ln(3) = 1.0986122886681098

Raw TF-IDF weights (w_{t,d} = tf_{t,d} * idf):
- D1:
  - w(cat,D1) = tf(cat,D1) * idf_classic(cat) = 1 * 0.4054651081081644 = 0.4054651081081644
  - w(mouse,D1) = 0 * 1.0986122886681098 = 0

- D2:
  - w(cat,D2) = 0
  - w(mouse,D2) = 0

- D3:
  - w(cat,D3) = 1 * 0.4054651081081644 = 0.4054651081081644
  - w(mouse,D3) = 1 * 1.0986122886681098 = 1.0986122886681098

Document scores for query Q = sum over query terms of w_{t,d} (query tf=1):
- score(D1,Q) = 0.4054651081081644 + 0 = 0.4054651081081644
- score(D2,Q) = 0 + 0 = 0
- score(D3,Q) = 0.4054651081081644 + 1.0986122886681098 = 1.5040773967762742

Ranking (TF-IDF raw): D3 (1.5041) > D1 (0.4055) > D2 (0)

Log-TF TF-IDF (tf' = 1 + ln(tf) for tf>0):
- Here all tf for relevant terms are either 0 or 1. For tf=1: tf' = 1 + ln(1) = 1 + 0 = 1; so tf' == raw tf in this corpus. Thus numerical values are identical to raw-TF case.

Note: If a document had tf > 1 for a query term, the log-TF result would be smaller than raw tf times idf; log-TF reduces the impact of repeated occurrences.

---

## 4.B BM25 (RSJ idf) detailed calculation (k1=1.5, b=0.75)
We use the standard BM25 formula (Eq. BM25 above). Re-stating parameters:
- k1 = 1.5, b = 0.75
- avgdl = 20/3 = 6.666666666666667
- IDF_RSJ(cat) = -0.5108256237659907
- IDF_RSJ(mouse) = +0.5108256237659907

Compute the length normalization constant L_d = k1 * (1 - b + b*(|d|/avgdl)) for each document (this is the additive term in the denominator after tf):
- For D1 (|D1| = 6):
  - |D1| / avgdl = 6 / 6.666666666666667 = 0.9
  - (1 - b + b * |D1|/avgdl) = 0.25 + 0.75 * 0.9 = 0.25 + 0.675 = 0.925
  - L_{D1} = k1 * 0.925 = 1.5 * 0.925 = 1.3875

- For D2 (|D2| = 9):
  - |D2| / avgdl = 9 / 6.666666666666667 = 1.35
  - (1 - b + b * ratio) = 0.25 + 0.75 * 1.35 = 0.25 + 1.0125 = 1.2625
  - L_{D2} = 1.5 * 1.2625 = 1.89375

- For D3 (|D3| = 5):
  - |D3| / avgdl = 5 / 6.666666666666667 = 0.75
  - (1 - b + b * ratio) = 0.25 + 0.75 * 0.75 = 0.25 + 0.5625 = 0.8125
  - L_{D3} = 1.5 * 0.8125 = 1.21875

Per-term BM25 fraction for tf_{t,d} = 1 (numerator = tf * (k1 + 1) = 1 * 2.5 = 2.5):
- For D1 (denom = tf + L_{D1} = 1 + 1.3875 = 2.3875):
  - fraction = 2.5 / 2.3875 = 1.047100616 (rounded)

- For D2 (if tf>0 we would compute similarly). Here tf for query terms in D2 are zero, so those term contributions are 0.

- For D3 (denom = 1 + 1.21875 = 2.21875):
  - fraction = 2.5 / 2.21875 = 1.1267605633802816

Now multiply each fraction by the RSJ idf for that term.

Term-by-term arithmetic (code-like blocks):
- D1, term = cat (tf=1)
  - idf_RSJ(cat) = -0.5108256237659907
  - numerator = 1 * (k1 + 1) = 2.5
  - denom = 1 + L_{D1} = 1 + 1.3875 = 2.3875
  - fraction = 2.5 / 2.3875 = 1.047100616
  - contribution = idf * fraction = -0.5108256237659907 * 1.047100616 = -0.534918017 (approx)

- D1, term = mouse (tf=0) => contribution = 0

- D2, term = cat (tf=0) => 0 ; mouse (tf=0) => 0

- D3, term = cat (tf=1)
  - idf_RSJ(cat) = -0.5108256237659907
  - numerator = 2.5
  - denom = 1 + L_{D3} = 1 + 1.21875 = 2.21875
  - fraction = 2.5 / 2.21875 = 1.1267605633802816
  - contribution_cat_D3 = -0.5108256237659907 * 1.1267605633802816 = -0.5756738389959823 (approx)

- D3, term = mouse (tf=1)
  - idf_RSJ(mouse) = +0.5108256237659907
  - fraction = same as above = 1.1267605633802816
  - contribution_mouse_D3 = +0.5108256237659907 * 1.1267605633802816 = +0.5756738389959823 (approx)

Now sum per document (BM25 raw RSJ idf, no clamping):
- score_BM25(D1,Q) = contribution_cat_D1 + contribution_mouse_D1 = -0.534918017 + 0 = -0.534918017
- score_BM25(D2,Q) = 0 + 0 = 0
- score_BM25(D3,Q) = contribution_cat_D3 + contribution_mouse_D3 = -0.575673839 + 0.575673839 = 0 (within rounding; exact cancellation because |idf(cat)| = |idf(mouse)| and tf and fractions equal)

Ranking (BM25 with RSJ idf allowing negative idf):
- D2 = 0 (tie with D3)
- D3 = 0 (tie)
- D1 = -0.5349 (worst)
So order: D2 and D3 (tied) > D1.

Interpretation: because cat is common (n(cat)=2) the RSJ idf for cat is negative and penalizes documents containing "cat"; mouse is rare and rewarded. D3 contains both cat (penalty) and mouse (reward) which cancel out; D1 contains cat only and so is penalized. D2 contains neither and ends up neutral (score 0).

## 4.C BM25 with clamped negative RSJ-IDF (common production behavior) 	6 i.e. idf := max(idf_RSJ, 0)
Many search engines avoid negative idf values because they cause documents to be pushed below documents that do not match the term at all. A common pragmatic choice is:
  idf_{clamped}(t) = max( idf_{RSJ}(t), 0 )

Apply clamping to our terms:
- idf_RSJ(cat) = -0.510825623766 -> idf_clamped(cat) = max(-0.5108, 0) = 0
- idf_RSJ(mouse) = +0.510825623766 -> idf_clamped(mouse) = 0.510825623766

Recompute contributions where idf for cat is 0:
- D1: cat contribution = 0 * fraction = 0 ; mouse = 0 => score(D1) = 0
- D2: still 0
- D3: cat contribution = 0 ; mouse contribution = +0.575673839 (calculated earlier) => score(D3) = +0.575673839

Ranking with clamped idf: D3 (0.5757) > D1 = D2

Comparison of rankings across methods on this corpus:
- TF-IDF (classic idf ln(N/n), raw TF): D3 > D1 > D2
- BM25 (RSJ idf allowed negative): D2 = D3 > D1 (D2 and D3 tied at 0; D1 negative)
- BM25 with clamped idf: D3 > D1 = D2

These changes show how BM25fs RSJ IDF and clamping choices can reorder results compared to TF-IDF; clamping avoids penalizing a document just for containing a common query term.

---

# 5. Point-by-point comparison table (concise)
| Aspect | TF-IDF (classic) | BM25 (standard) |
|---|---:|---|
| TF handling | Linear in raw-TF (tf) or sublinear with e.g. log-TF | Saturating TF: (tf*(k1+1))/(tf + k1 * (...) ) 	6 diminishing returns for large tf |
| IDF formula | Common: idf = ln(N / n) (or smoothed variants) | RSJ IDF: ln((N - n + 0.5)/(n + 0.5)) (often clamped to >=0 in prod.) |
| Document-length normalization | Not intrinsic; often done by vector normalization (L2) or pivoted normalization as an extra step | Built-in via b parameter and avgdl pivot; tunes how much length reduces tf impact |
| Tunable parameters | Typically none (unless you add normalization or log TF scaling) | k1 (TF saturation), b (length normalization). BM25+ adds delta; BM25F uses per-field weights |
| Computational cost | Very cheap: per-term multiplications and dot-product; easy to precompute tf*idf weights | Comparable per-query cost; needs avgdl (global) and per-doc length, but still very fast. Slightly more operations per term (division) |
| Typical output range | Unbounded positive (or negative if using uncommon normalizations); usually positive scores if idf>0 | Scores can be negative if RSJ idf negative (unless clamped); otherwise typically positive magnitudes; monotonic in term contributions |
| Can weights be negative? | Classic idf ln(N/n) >=0 if n<=N (but variant smoothing could yield small positive) 	6 weights usually non-negative unless special idf formula used | RSJ IDF can be negative for very common terms; therefore per-term contributions can be negative unless idf clamped or BM25+ used |

---

# 6. Pros / Cons and typical use cases
Pros of TF-IDF
- Simple to explain and implement.
- Fast to compute (sparse vector dot-products), good for feature engineering (text features in ML).
- Works well when combined with normalization and modern classifiers or embeddings as features.

Cons of TF-IDF
- Linear TF can over-value repeated terms (no saturation).
- Document length handling is ad-hoc and must be added explicitly.
- Not grounded in a probabilistic relevance model; less principled than BM25 for ranking.

Pros of BM25
- Principled derivation from probabilistic relevance framework.
- TF saturation prevents term stuffing from dominating results.
- Built-in length normalization (b parameter) that is effective in practice.
- Tunable parameters (k1, b) let you adjust sensitivity and get strong out-of-the-box performance.
- Widely used as default ranking in Lucene/Elasticsearch/Solr and many IR systems.

Cons of BM25
- Slightly more parameters to tune (k1,b); worst-case behavior like negative idf requires pragmatic choices (clamp or BM25+).
- Still a bag-of-words model; does not capture phrase semantics or term proximity (requires extensions).

Typical use cases
- Search ranking (ad-hoc document retrieval): BM25 is the default in many production search engines.
- Feature engineering in ML / NLP: TF-IDF is commonly used as sparse features for classifiers, clustering, or as a baseline for embeddings.
- Hybrid systems: BM25 or TF-IDF for initial sparse retrieval followed by neural rerankers (RAG / LLM pipelines).

Scalability
- Both are sparse and scale well with inverted indices; BM25 is equally scalable as TF-IDF in large systems because computations are per posting entry with similar complexity.

---

# 7. Authoritative references (selected, up-to-date)
- Manning C. D., Raghavan P., Sch fctze H., "Introduction to Information Retrieval" (2008, online edition) 	6 classic textbook describing TF-IDF and vector-space methods: https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf
- Robertson S., Zaragoza H., "The Probabilistic Relevance Framework: BM25 and Beyond" (Foundations and Trends in IR, 2009) 	6 deep authoritative review and derivation of BM25/BM25F: https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf
- Lucene BM25Similarity documentation (defaults): https://lucene.apache.org/core/7_0_1/core/org/apache/lucene/search/similarities/BM25Similarity.html (Lucene API documents the default k1=1.2, b=0.75; see current Lucene docs for exact version-specific defaults) https://lucene.apache.org/ 
- Elasticsearch: Practical BM25 	6 Part 2: The BM25 algorithm and its variables (Elastic blog) 	6 shows variables, idf formula in Lucene/ES and explains clamping/behavior: https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables
- Practical notes and comparisons (tutorials and comparisons): multiple practitioner posts and comparisons (examples): https://emschwartz.me/comparing-full-text-search-algorithms-bm25-tf-idf-and-postgres/ and blog posts comparing BM25 vs TF-IDF such as https://www.myscale.com/blog/bm25-vs-tf-idf-deep-dive-comparison/ .

(Primary canonical references used above: the Manning IR book PDF and the Robertson & Zaragoza BM25 review; plus Lucene/Elasticsearch docs and Elastic blog.)

---

# Appendix: recommended hyperparameter ranges and implementation notes
Recommended starting points (typical):
- BM25 k1: 1.2 (Lucene default) or 1.5 (commonly quoted). Range to tune: [0.5, 2.0]. Lower k1 -> less importance to TF; higher k1 -> more TF sensitivity.
- BM25 b: 0.75 (common default). Range to tune: [0.0, 1.0]. b=0 disables length normalization; b=1 uses full pivoted length normalization.
- BM25+ delta (if used): small positive, e.g. delta \u2208 [0.0, 1.0] or tuned (some references use 1.0);
- TF-IDF smoothing: use smoothed IDF = ln((1+N)/(1 + n)) to avoid divide-by-zero; consider log base natural (ln) for consistency.

Implementation notes and practical choices
- IDF clamping: RSJ idf can be negative. In production many systems do idf = max(idf_RSJ, 0) to avoid penalizing documents for matching a (very) frequent term. Alternatively, use BM25+ to add a floor.
- TF variant: for feature engineering, log-TF (1 + ln(tf)) is commonly used; for ranking, BM25fs saturation is often better.
- Document length measurement: count of index-time tokens (term occurrences) is standard. Make sure avgdl uses same tokenization and analyzer as document lengths are computed with.
- Multi-field ranking: use BM25F (or field-weighted combinations) when documents have fields with different importance; tune per-field boosts.
- Normalization in TF-IDF: if using TF-IDF vectors with cosine similarity, ensure consistent L2 normalization (query and document vectors). BM25 does not require L2 normalization.
- Ties and scaling: BM25 and TF-IDF produce scores on different scales; absolute values are not comparable across models without calibration (only rankings matter).

---

# Sources
- Manning, C., Raghavan, P., & Sch fctze, H. (2008), Introduction to Information Retrieval (online edition). https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf
- Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 3(4). https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf
- Elasticsearch blog: "Practical BM25 	6 Part 2: The BM25 Algorithm and its variables". https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables
- Apache Lucene BM25Similarity documentation (example reference showing defaults k1=1.2, b=0.75): https://lucene.apache.org/core/7_0_1/core/org/apache/lucene/search/similarities/BM25Similarity.html
- (Practical comparisons/tutorials): Emschwartz: 	1Comparing full text search algorithms: BM25, TF-IDF, and Postgres	2 — https://emschwartz.me/comparing-full-text-search-algorithms-bm25-tf-idf-and-postgres/
- Additional practitioner guides and comparisons (explain differences and BM25 variants): https://www.myscale.com/blog/bm25-vs-tf-idf-deep-dive-comparison/

(Primary theory sources used: Manning et al. IR book; Robertson & Zaragoza BM25 review; implementation references: Lucene/Elasticsearch docs and Elastic blog.)

(End of report)
