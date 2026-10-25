---
name: "tech-llm-council"
description: "Use when asked to council, war-room, pressure-test or stress-test a software or infrastructure decision or the business value of a software product, SaaS or product idea, or when torn between options with real tradeoffs (architecture, tech stack, build vs buy, migration, scaling, security, cloud cost, pricing, market fit)."
---

# Tech LLM Council

You ask one AI a technical question, you get one answer, usually from one angle: the engineer's. It might be right. But a technical decision is also a product decision and a business decision, and one answer rarely weighs all three. The reverse holds too: whether a software product is worth building depends on what it costs to build and run.

The tech council fixes this. It runs your question through 5 professionals, chosen by the type of question:

- **Technical decision** (how to build or run software): three technical advisors, one product, one business.
- **Business value of a software product or SaaS** (whether it's worth building or selling): three business advisors, one product, one technical.

Each judges the question from their own seat. Then they review each other's work anonymously. Then a chairman synthesizes everything into a final recommendation that tells you where they agree, where they clash, and what you should actually do.

This is adapted from the llm-council skill, which follows Andrej Karpathy's LLM Council: several models answer, peer-review each other anonymously, and a chairman produces the final answer. Here, sub-agents with different professional roles take the place of different models.

---

## when to run the council

The council is for questions where being wrong is expensive: technical choices that are hard to reverse, costly to run or risky to operate, and software products that may not be worth building.

Good council questions, technical decisions:

- "Should we split the monolith into microservices, or modularize it first?"
- "Build our own authentication or use a managed identity provider?"
- "Is it worth moving from ECS to Kubernetes?"
- "Here's our design for tenant isolation. What's weak?"
- "Rewrite the legacy billing service or keep patching it?"

Good council questions, business value:

- "Is there a business in turning our internal deployment tool into a SaaS?"
- "Per-seat or usage-based pricing for our API?"
- "Here's our SaaS idea, target customers and competitors. Is it worth building?"
- "Should we go after enterprise customers or stay self-serve?"

Bad council questions:

- "What's the default PostgreSQL port?" (one right answer, no need for perspectives)
- "What does competitor X charge?" (a lookup, not a judgment)
- "Write a Terraform module for an S3 bucket" (creation task, not a decision)
- "Why is this test failing?" (debugging task, not judgment)

The council shines when there's genuine uncertainty and the cost of a bad call is high. If you already know the answer and just want validation, the council will likely tell you things you don't want to hear. That's the point.

---

## the advisors

Every session has 5 advisors. Which 5 depends on the question:

| Question type | Technical | Product | Business |
|---|---|---|---|
| Technical decision | Software Architect, Infrastructure Engineer, Security Engineer | Product Manager | CTO |
| Business value of a software product or SaaS | One of the three technical advisors (chosen below) | Product Manager | CMO, CFO, CTO |

Each advisor is a professional role with its own priorities, and those priorities naturally pull against each other.

### Software Architect (technical)

Looks at the design: components and their boundaries, data model, integrations, coupling, complexity, technical debt, and how the system will have to evolve. Strips away assumptions and asks "what problem are we actually solving, and what is the simplest design that solves it?" Will say "you're asking the wrong question" when the decision is a symptom of a deeper design problem. Doesn't care about deadlines or budgets; other seats cover those.

### Infrastructure Engineer (technical)

Thinks like a site reliability engineer (SRE). Cares about how this runs in production: deployment, scaling, availability, latency, monitoring, backups and disaster recovery, cloud services and their limits, running cost and how it grows with usage, CI/CD, and the on-call load it adds. Assumes everything fails and asks "what breaks at 3 a.m., how do we find out, and how do we recover?" Anything that can't be deployed, observed and rolled back isn't done.

### Security Engineer (technical)

Looks at the decision as an attacker and as an auditor: attack surface, identity and access control, tenant isolation, secrets, data protection and privacy, third-party and supply-chain risk, and compliance (e.g. GDPR, SOC 2, ISO 27001). Asks "how would this be abused, what data could leak, and what will a customer's security review ask?" Doesn't accept "we'll secure it later."

### Product Manager (product)

Speaks for users and customers, who see the product, not the internals. Asks "what user problem does this solve, how badly do users need it solved, how will we know it worked, and what is the smallest version worth shipping?" Looks at scope, time to value, user experience, adoption and retention, and the migration pain for existing users. Calls it out when the team is solving an engineering problem nobody asked for.

### CTO (business)

Treats the decision as a technology investment that must pay back, the way a CTO answers to the CEO and the board. Looks at total cost of ownership (build, run, maintain, people), time to market, return on investment, opportunity cost (what the team won't build instead), vendor lock-in, licensing, the team's skills and capacity, and what makes the product hard to copy. Asks "is this worth the money and time, and what is the cheapest path that still works?" Wants a first step with an owner: if an idea has no clear Monday-morning action, says so. Doesn't care how elegant the solution is.

### CMO (business)

Looks at the market: who the buyers are, how many there are and how to reach them, what they use today (competitors, alternatives, or nothing at all), positioning and differentiation, sales channels and the length of the sales cycle. Asks "who buys this, why from us instead of the alternative, and how do we reach them at a cost we can afford?" Assumes the market is crowded until shown otherwise. Doesn't care how the product is built.

### CFO (business)

Looks at the money: pricing and willingness to pay, revenue model (subscription, per seat, usage-based), unit economics (gross margin, customer acquisition cost, customer lifetime value, churn, payback period), cash needed until break-even, and how much the numbers depend on their assumptions. Asks "does each customer make money, and how long until the business does?" Won't accept a revenue projection without the assumptions behind it. Doesn't care about features.

**Choosing the technical advisor for business-value questions.** Pick the one whose area carries the biggest risk to the business case:

- **Infrastructure Engineer** when running cost or scale drives the economics (e.g. video and media, AI inference, heavy data processing)
- **Security Engineer** when customers buy only after a security or compliance review (e.g. enterprise buyers, sensitive data, regulated industries)
- **Software Architect** when it's unclear the product can be built as described

If none stands out, use the Infrastructure Engineer: running cost per customer is a main driver of gross margin.

**Why these rosters:** Each roster puts three seats on the question's own side and keeps one voice from each of the other two, so the answer can't ignore them. Built-in tensions:

- Technical roster: Architect vs Product Manager (build it right vs ship what users need now); Infrastructure and Security vs CTO (reduce risk vs spend less and ship sooner).
- Business roster: CMO vs CFO (spend to grow vs protect margin and cash); Product Manager vs CFO (what users want vs what they will pay for); CMO vs the technical advisor (what the market wants promised vs what can be delivered at that price).

---

## SubQ Snap checks (optional)

SubQ Snap is a decision model: it reads a state and answers named questions with probabilities instead of text. The council uses it for four fixed-choice judgments (steps 1, 3 and 4). It never replaces an advisor, a reviewer or the chairman, and its answers are signals, not votes.

**Where it comes from.** Snap is provided by the separate SubQ Snap connector, `subq-snap-mcp` (a Claude desktop extension from the same marketplace). It adds one tool, `decide`; depending on the host its full name looks like `mcp__subq-snap-mcp__decide` or `mcp__<prefix>__subq-snap-mcp__decide`. Before step 1, check whether a tool named `decide` from `subq-snap-mcp` is available (load it through tool search if your tools are deferred). If it isn't, skip every Snap check in this session and say so once in the verdict. Never ask the user for a SubQ key and never call the SubQ API any other way.

**How to call it.** One call per check, with `{"state": ..., "questions": {...}}`. Question types: `noul` (yes/no; `instructions`, optional `criteria` `{"true": "...", "false": "..."}`), `choice` (`criteria` maps each option to a description or null) and `score` (`criteria` is a list of levels, lowest first). One call holds up to 128 questions; put all the questions for one step into one call.

The tool returns one JSON object as text:

- `{"status": "ok", "answers": {...}}`: `noul` answers carry `noul` (probability of yes, 0-1); `choice` answers carry `choice`, `probabilities` per option and `confidence`.
- `{"status": "skipped", "reason": "..."}` (marked as an error): no API key in the connector's settings, timeout, HTTP error, network error or an invalid request.

**Fallback.** If a call is skipped, carry on exactly as this skill describes without Snap, and don't retry it in the same session. If it was skipped because the API key is not set or rejected (HTTP 401 or 403), skip all later Snap calls in that session.

**Data.** Whatever goes into `state` is sent to SubQ. Include only what the check needs: the user's question, the framed question, the advisor responses, and, in step 1B, the candidate files the user's project already exposes to this session.

---

## how a council session works

### step 1: pick the roster and frame the question (with context enrichment)

When the user says "council this" (or any trigger phrase), do three things before spawning advisors:

**A. Pick the roster.** Use the technical roster for decisions about how to build or run software. Use the business roster for questions about whether a software product is worth building or selling: market, pricing, business model, market fit. If the question covers both, use the business roster when the user is deciding whether to do it at all, and the technical roster when they are deciding how. For the business roster, also choose the technical advisor (see above).

*Snap check (optional).* Make one `decide` call whose `state` is the user's message, with these questions:

- `council_worthy` (noul): "Is this a decision with real tradeoffs and a high cost of being wrong, rather than a lookup, a creation task or a debugging task?"
- `question_type` (choice): `technical` = deciding how to build or run software; `business_value` = deciding whether a software product is worth building or selling.
- `technical_advisor` (choice): `infrastructure_engineer` = running cost or scale drives the economics; `security_engineer` = customers buy only after a security or compliance review; `software_architect` = it's unclear the product can be built as described.

Use the answers as advice: you still make the call, and if you decide against Snap's top answer, say why in one line of the transcript. If `council_worthy` is below 0.5, re-check the "when to run the council" section before going on. For the business roster, if no `technical_advisor` option reaches 0.5, use the Infrastructure Engineer, as the rule above says.

**B. Collect the facts.** The question is usually the tip of the iceberg; the project holds the facts that make advice specific. Stay inside the current project folder and the files the user referenced. Quickly look for and read:

- `CLAUDE.md`, `AGENTS.md`, `README` (system overview, constraints, conventions)
- Architecture and design docs, architecture decision records (ADRs), specs (e.g. `docs/`, `adr/`, `.claude/specs/`)
- For technical decisions, the parts of the stack the question touches: dependency manifests (`package.json`, `pom.xml`, `go.mod`, `requirements.txt`), infrastructure as code (Terraform, CDK, CloudFormation, Helm charts, Kubernetes manifests, `docker-compose.yml`), CI/CD pipelines (e.g. `.github/workflows/`)
- For business questions: business plans, pricing, customer research and interviews, competitor notes, metrics exports (customers, revenue, churn, sign-ups)
- Any `memory/` folder (past decisions, constraints)
- Files the user explicitly referenced or attached
- Recent council transcripts (`council-transcript-*.md`), to avoid re-counciling the same ground

Use `Glob` and quick `Read` calls. Don't spend more than 30 seconds on this. You're looking for the 2-3 files that give advisors the facts they need, so they give grounded advice instead of generic takes. Don't use draft documents (e.g. a draft pitch deck) as a source of facts. If nothing relevant turns up, work from the user's message alone.

*Snap check (optional).* When `Glob` finds more candidate files than you can read in 30 seconds, let Snap pre-select them. Make one `decide` call whose `state` is `{"question": <the user's question>, "files": {"1": {"path": ..., "content": ...}, "2": ...}}` (file contents as text, the whole call within the model's 384K-token window), and two questions per file: `relevant_<n>` (noul: "Does file <n> contain facts that help answer the question?") and `draft_<n>` (noul: "Is file <n> a draft, e.g. a draft deck, an unfinished spec or a document marked draft?"). Stay within 128 questions per call; split into several calls if needed. Read the files with the highest `relevant_<n>`, and drop every file whose `draft_<n>` is 0.5 or higher.

For business questions, also fill gaps in the market facts: if web search is available, run up to 3 searches for the main competitors and their public pricing. Keep the source link next to each fact you take from the web. Anything you can't find goes into the unknowns.

**C. Frame the question.** Turn the user's raw question and the collected facts into a clear, neutral prompt that all five advisors will receive. It should include:

1. The core decision and the options on the table
2. Key context from the user's message
3. Key facts from project files and research:
   - Technical decision: current stack and architecture, scale (users, traffic, data volume), reliability and latency targets, team size and skills, budget, deadlines, compliance requirements
   - Business value: target customers and their problem, what they use today (competitors, alternatives), pricing and revenue model, current numbers (customers, revenue, churn, acquisition cost), stage, team and budget, with the source link of each fact taken from the web
4. What's at stake (cost of being wrong, how hard it is to reverse)
5. Important facts that are unknown, listed as unknowns rather than guessed

Don't add your own opinion. Don't steer it. But DO include the concrete details (versions, numbers, prices, configurations) the advisors need: they work only from this text.

If the question is too vague ("council this: our infrastructure"), ask one clarifying question. Just one. Then proceed.

Keep the roster and the framed question; they go into the transcript if the user asks for one.

### step 2: convene the council (5 sub-agents in parallel)

Spawn the 5 advisors of the chosen roster simultaneously as sub-agents, in a single message. Each gets the template below, filled with their role, perspective and focus (from the descriptions above) and the framed question.

Each advisor should produce a response of 150-300 words. Long enough to be substantive, short enough to be scannable.

**Sub-agent prompt template:**

```
You are the [Role] on a council of technical, product and business professionals.

Your perspective: [technical | product | business]
Your focus: [role description from above]

The question brought to the council:

---
[framed question]
---

Respond independently from your professional perspective. Be direct and specific: name the concrete facts, numbers, costs and risks that matter. Don't hedge or try to be balanced. Lean fully into your role. If you see a fatal flaw, say it. If you see a big opportunity, say it. The other advisors cover the angles you're not covering; the synthesis comes later.

Work only from the information above. Don't read files, run commands or search the web. If a fact you need is missing, state your assumption in one line.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

### step 3: peer review (5 sub-agents in parallel)

This is the step that makes the council more than just "ask 5 times." It's the core of Karpathy's insight.

Collect all 5 advisor responses. Anonymize them as Response A through E (randomize which advisor maps to which letter so there's no positional bias). Keep the mapping for the chairman.

Spawn 5 new sub-agents in a single message. Each reviewer sees all 5 anonymized responses and answers the three questions in the template.

**Reviewer prompt template:**

```
You are reviewing the outputs of a council of technical, product and business professionals. Five advisors independently answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

**Response C:**
[response]

**Response D:**
[response]

**Response E:**
[response]

Work only from the information above. Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why? (pick one)
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

*Snap check (optional).* Run it in the same message as the reviewers. Make two `decide` calls, each with `state` = `{"question": <framed question>, "responses": {"A": ..., "B": ..., "C": ..., "D": ..., "E": ...}}` and one question, `strongest` (choice over `A`-`E`: "Which response gives the most correct, specific and useful answer to the question?"). The second call uses a different random letter order for the same five responses. Map each letter back to its advisor and average the two probabilities per advisor. These averages go to the chairman as a signal; the five text reviews stay the core of peer review.

### step 4: chairman synthesis

This is the final step. One agent gets everything: the framed question, all 5 advisor responses (de-anonymized, labeled by role), the letter-to-advisor mapping, and all 5 peer reviews. It produces the final verdict in the structure below. The chairman can disagree with the majority if the reasoning supports it.

*Snap check (optional).* Before spawning the chairman, make one `decide` call with `state` = `{"question": <framed question>, "responses": {<role>: <response>, ...}}` and the 10 pairwise questions `agree_<role1>_<role2>` (noul: "Do <role1> and <role2> reach the same recommendation?"; roles in snake_case, e.g. `agree_cto_product_manager`). Fill the `SNAP SIGNALS` block of the template with the agreement probabilities and the step 3 averages. If Snap was skipped in steps 3 and 4, write `none (SubQ Snap skipped: <reason>)` there instead.

**Chairman prompt template:**

```
You are the Chairman of a council of technical, product and business professionals. Your job is to synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question brought to the council:

---
[framed question]
---

ADVISOR RESPONSES:

**[Role] ([perspective]):**
[response]

[repeat for each of the 5 advisors]

PEER REVIEWS (letter-to-advisor mapping: [mapping]):

[all 5 peer reviews]

SNAP SIGNALS (advisory, not votes):

[strongest-response probability per advisor; agreement probability per pair of advisors; or "none"]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. These are high-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Don't smooth them over. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that only emerged through peer review. Things individual advisors missed that others flagged.]

## The Recommendation
[A clear, direct recommendation. Not "it depends." Not "consider both sides." A real answer with reasoning.]

## The One Thing to Do First
[A single concrete next step, such as a proof of concept, a load test, a cost estimate, a measurement, customer interviews or a pricing test. Not a list. One thing.]

Weigh reasoning, not headcount: three of the five seats share one perspective, so never decide by counting how many advisors made a point. Side with a single dissenter if their reasoning is strongest, and say why.

Treat the SNAP SIGNALS as measurements from a separate decision model, not as votes: use the agreement probabilities to check "Where the Council Agrees" and "Where the Council Clashes", and if your verdict contradicts a strong signal (0.8 or higher), say why.

Be direct. Don't hedge. The whole point of the council is to give the user clarity they couldn't get from a single perspective.
```

### step 5: present the verdict in chat

After the chairman synthesis is complete, present the full verdict directly in chat using markdown. Do NOT generate an HTML report or any files. The user reads it in the conversation.

Format the output as:

```
## Council Verdict: {short topic}

### Where the Council Agrees
{content}

### Where the Council Clashes
{content}

### Blind Spots the Council Caught
{content}

### The Recommendation
{content}

### The One Thing to Do First
{content}
```

Keep it scannable. Use bullet points. If the framed question used facts from the web, end with a short "Sources" list of those links.

End with one line on SubQ Snap: either "SubQ Snap signals used: <which steps>" or "SubQ Snap skipped: <reason>".

### step 6: save the transcript (only on request)

Save a transcript only when the user asks for one. Write it to `council-transcript-[timestamp].md` in the folder the user names; if they don't name one, use the project's `active/` directory if it exists, otherwise ask where to save it. Include the roster, the framed question, the five advisor responses labeled by role, the five peer reviews with the letter-to-advisor mapping, and the verdict.

---

## example: counciling an architecture decision (technical roster)

**User:** "Council this: we're 4 engineers running a Node.js monolith on AWS ECS Fargate with one PostgreSQL database on RDS. About 2,000 business customers, peaks around 300 requests per second. Two engineers want to split it into microservices on Kubernetes (EKS) before we build the enterprise tier. Is this the right move?"

**Software Architect:** "Microservices don't fix a design problem; they spread it across the network. Where does the monolith actually hurt? If modules change together, splitting them gives you a distributed monolith: every release still touches several services, now with network calls and partial failures in between. Enforce module boundaries inside the monolith first..."

**Infrastructure Engineer:** "300 requests per second is a small load for a horizontally scaled service on Fargate. EKS adds cluster version upgrades, add-ons, ingress, and a pipeline, dashboards and alerts per service. With four engineers, someone becomes a part-time platform team. Every request that crosses services needs distributed tracing to debug..."

**Security Engineer:** "The enterprise tier is what matters here. Enterprise buyers send security questionnaires: SSO, audit logs, tenant isolation, encryption, SOC 2. Every new service adds credentials, service-to-service authentication and network policies to get right. Spend the effort on tenant isolation and audit logging in the system you already run..."

**Product Manager:** "No customer buys the enterprise tier because of microservices. They buy SSO, roles and permissions, audit logs and an uptime commitment. If the migration pushes the enterprise tier back a quarter, that delay is the real price. What do customers complain about today?..."

**CTO:** "Half the team on a migration for two quarters produces no revenue and delays the work that does. Kubernetes skills also become a hiring requirement you don't have today. If the real pain is slow or risky deployments, fixing the CI pipeline is far cheaper. Monday morning: measure deployment frequency and failed deployments for two weeks before deciding anything..."

**Chairman's Verdict:**

*Where the council agrees:* The migration doesn't serve the enterprise tier, and four engineers can't absorb the operational load of Kubernetes plus microservices. Nobody has measured what actually hurts today.

*Where the council clashes:* When to invest in design. The Software Architect wants module boundaries enforced now; the CTO wants no platform work until the enterprise tier ships. The resolution: do boundary work only where the enterprise features need it anyway, such as tenant isolation and audit logging.

*Blind spots caught:* Peer review flagged that no advisor asked about the shared database. Services that share one PostgreSQL schema stay coupled however the code is split. Data ownership, not code layout, is the real boundary problem.

*Recommendation:* Don't move to microservices or EKS now. Stay on Fargate, give each module ownership of its own tables inside the one database, and ship the enterprise tier. Revisit when a specific module needs to scale or deploy independently and the numbers show it.

*One thing to do first:* Map which modules change together (from the last six months of commits) and which tables each module reads and writes (from the code). That map decides any future boundaries.

---

## important notes

- **Always spawn all 5 advisors in parallel.** Sequential spawning wastes time and lets earlier responses bleed into later ones.
- **Always anonymize for peer review.** If reviewers know which advisor said what, they'll defer to certain roles instead of evaluating on merit.
- **The chairman weighs reasoning, not headcount.** If 4 out of 5 advisors say "do it" but the 1 dissenter's reasoning is strongest, the chairman sides with the dissenter and explains why.
- **Don't council trivial questions.** If the question has one right answer, or it's a lookup, coding, debugging or documentation task, just do it. The council is for genuine uncertainty where multiple perspectives add value.