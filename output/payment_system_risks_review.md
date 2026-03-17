# Literature Review: Payment System Risks and Mitigation Approaches

Executive summary

This literature review synthesizes peer-reviewed and academic working-paper evidence on the nature, transmission, and mitigation of risks in large-value and retail payment systems. It focuses on settlement/credit risk, liquidity and intraday liquidity risk, operational and cyber risk, and systemic contagion. The review highlights empirically and theoretically supported mitigation approaches including RTGS adoption, liquidity-saving mechanisms (LSMs), collateral and net debit limits, central bank intraday liquidity provision, legal and operational standards, monitoring and stress-testing, and recovery/fallback arrangements.

Scope and methodology

The review draws on academic working papers and peer-reviewed journal articles and surveys addressing payment-system risks and policy responses. Key sources include a theoretical working paper on systemic risk in multilateral netting systems (Federal Reserve Bank working paper, 1996), journal articles on liquidity risk and policy options, a survey of systemic risk in financial networks, and empirical analyses of RTGS-based interbank networks. Only scientific/academic sources were used; practitioner or purely industry reports were consulted only where they summarized or extended peer-reviewed findings.

1. Definitions and taxonomy of risks in payment systems

- Settlement risk: the risk that a party delivering a payment does not receive the corresponding final funds (timing/delivery mismatch). Historically illustrated by Herstatt (1974) in FX settlements. Settlement risk is central to multilateral netting and deferred settlement systems.

- Credit risk: exposures created when one participant owes funds to another across a settlement cycle (more relevant in deferred net settlement systems).

- Liquidity risk (intraday): the risk that a participant lacks sufficient funds at the time payments are due and therefore cannot settle outgoing obligations, potentially leading to payment failures and gridlock. With widespread adoption of RTGS, liquidity risk has become a primary focus because RTGS eliminates multilateral credit accumulation but increases intraday liquidity needs.

- Systemic risk / contagion: the probability that liquidity or solvency problems of one or more participants propagate through the payment network, producing broader disruption to the financial system or economy.

- Operational and cyber risk: failures of systems, communications, or deliberate attacks that interrupt payment processing or cause incorrect settlement.

- Legal and interoperability risk: uncertainty about legal finality, enforceability of netting, or inconsistencies across jurisdictions and systems that can impede settlement or recovery.

2. Key mechanisms of risk transmission (findings from literature)

- Network topology and connectivity: empirical network studies show that connectivity creates both risk-spreading and risk-sharing channels. Highly connected systems can spread shocks quickly but also allow liquidity redistribution. The trade-off depends on the distribution of exposures and centrality of participants.

- Netting vs RTGS trade-offs: Deferred net settlement reduces aggregate intraday liquidity needs via multilateral netting but accumulates credit exposures and creates settlement risk if large participants fail. RTGS removes interparticipant credit exposures by settling payments individually in real time, reducing settlement risk but raising intraday liquidity demand.

- Liquidity shocks and gridlock: Models and simulations (e.g., multilateral netting models and RTGS liquidity models) demonstrate thresholds where an initial set of failures triggers cascading defaults or payment delays. Gridlock resolution mechanisms (e.g., queuing with priority, optimized bilateral offsetting) can materially alter outcomes.

- Role of central bank liquidity provision: The central bank acting as intraday liquidity provider or by offering intraday credit reduces liquidity-constrained failures but introduces moral hazard considerations; policy design (price of intraday credit, collateralization) affects participant behavior.

3. Empirical evidence and stylized facts

- Working-paper and empirical studies (including cross-country analyses) find that adoption of RTGS generally reduces settlement risk and the size-duration of credit exposures, but increases participants' need for intraday liquidity management. Countries have subsequently layered liquidity-saving mechanisms to address this.

- Network analyses of RTGS flows in specific countries find vulnerability concentrated in a small set of highly central participants; failure of a central node can propagate large-scale disruptions, underscoring the need for access rules and risk controls.

- Studies of intraday liquidity find heavy-tailed distributions of peak intraday needs and show that timing of payments (concentration early in the day) materially increases systemic susceptibility to gridlock.

4. Mitigation approaches identified in the literature

A. System design and settlement model

- Real-time Gross Settlement (RTGS): Promoted across countries to eliminate settlement (Herstatt-type) risk. RTGS makes payments final at delivery and removes multilateral credit accumulation.

- Deferred net settlement with safeguards: Where netting remains (e.g., some securities or retail systems), enforceable netting laws, collateral requirements, and default rules reduce settlement exposures.

B. Liquidity management tools

- Liquidity-Saving Mechanisms (LSMs): Algorithms that reorder or offset queued payments to economize on liquidity (e.g., debiting only netted obligations, bilateral offset optimization). Academic and simulation studies indicate LSMs can substantially reduce intraday liquidity needs while preserving RTGS finality.

- Intraday central bank credit: Provision of collateralized intraday credit (often priced or collateralized) mitigates intraday liquidity shortfalls. Literature emphasizes the need to balance timeliness of credit with measures to limit moral hazard (collateral, pricing, limits).

- Net debit caps, collateral/asset requirements: Caps on allowable net debit positions and collateral standards reduce the probability of participant default and limit contagion in netting systems (supported by theoretical models).

C. Operational, legal and governance measures

- Clear legal frameworks: Legal finality of settlement, enforceable netting, and clear rules for default management are repeatedly emphasized as prerequisites for reducing legal and settlement risk.

- Operational resilience and cyber security: Peer-reviewed literature highlights the growing importance of cyber risk; recommendations include redundancy, secure communications, incident response plans, and regular testing.

- Access rules and participant controls: Limiting direct access to critical systems to institutions meeting prudential standards, and tiered access arrangements, reduce the chance that a weak participant triggers systemic disruption.

D. Monitoring, stress testing and oversight

- Intraday liquidity indicators and monitoring: Research proposes intraday liquidity risk indicators (LRIs) to alert operators and supervisors to emerging stress and to trigger mitigants.

- Network and contagion stress tests: Simulations that use payment-flow networks to explore failure scenarios help identify systemic nodes and calibrate policy tools.

- Recovery and resolution planning: For systemically important operators, plans for operational recovery and resolution are necessary to limit prolonged outages.

E. Market-based mechanisms and incentives

- Pricing of payment services and intraday liquidity: Fee structures that reflect costs and scarcity of intraday liquidity align participant incentives with system-wide risk management.

- Collateral haircuts and eligibility criteria: Tightening collateral eligibility during stress reduces solvency transfer risks to central banks.

5. Open questions and research gaps (from the literature)

- Optimal calibration of intraday liquidity provision: How to design pricing, collateral, and limits to support smooth settlement while minimizing moral hazard remains an open empirical question.

- Interaction of network topology with new payment types: Real-time retail payments and rising non-bank participant presence change network dynamics; more empirical work is needed on cross-system contagion.

- Cyber risk quantification and mitigation effectiveness: While operational recommendations are extensive, quantitative studies on cyber shock propagation across payment systems are limited.

- Cross-border and multi-system interoperability: The literature documents legal and operational frictions; empirical research into effective interoperability models (including CLS-like solutions for FX and cross-border RTGS linkages) is ongoing.

6. Conclusions and policy implications

The academic literature converges on several robust conclusions: (1) RTGS reduces settlement credit risk but increases the focus on intraday liquidity management; (2) liquidity-saving mechanisms and carefully designed intraday credit (collateralized and priced) are effective mitigants; (3) legal finality, enforceable netting, and prudential access rules are essential complements; (4) network structure matters — systemic importance concentrates in a few central participants and requires tailored oversight; (5) operational and cyber resilience is an increasing priority that must be treated alongside financial risk controls.

Policy packages combining system design (RTGS + LSMs), central-bank liquidity backstops (collateralized), robust legal frameworks, supervisory monitoring (intraday indicators and stress-testing), and operational resilience measures are consistently recommended across studies.

Sources

- Chakravorti, S. (1996). Analysis of Systemic Risk in the Payments System. Federal Reserve Bank of Dallas working paper. https://www.dallasfed.org/-/media/Documents/banking/fiswp/fiswp9602.pdf

- IMF. Systemic Financial Risk in Payment Systems. (URL encountered: https://www.elibrary.imf.org/downloadpdf/display/book/9781557752055/ch02.pdf)

- Liquidity risk and policy options. ScienceDirect. (Article page): https://www.sciencedirect.com/science/article/pii/S0378426614000326

- Systemic Risk in Financial Networks: A Survey. Annual Reviews. https://www.annualreviews.org/content/journals/10.1146/annurev-economics-083120-111540

- Monitoring intraday liquidity risks in a real-time gross settlement system. Risk.net article page: https://www.risk.net/journal-of-financial-market-infrastructures/7874866/monitoring-intraday-liquidity-risks-in-a-realtime-gross-settlement-system

- Systemic risk in the Angolan interbank payment system - a network perspective. (Applied Economics / Taylor & Francis) https://www.tandfonline.com/doi/full/10.1080/00036846.2020.1751052

- The Next Generation RTGS: Liquidity Saving Mechanisms as an Overlay Service. FNA paper (2024). https://fna.fi/wp-content/uploads/2024/02/FNA-Papers-The-Next-Generation-RTGS_-Liquidity-Saving-Mechanisms-as-an-Overlay-Service-2024.pdf

(Notes: some full-text documents were accessed directly; where download was restricted, article pages and abstracts were used to verify findings.)


