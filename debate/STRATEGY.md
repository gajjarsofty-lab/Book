# Group 6 Debate War Room: Final Strategy (for approval)

## Context
- Motion: "Should online platforms be held legally liable for user-posted misinformation?" Group 6 argues NO.
- Five debaters with equal roles, a corporate setting, provisional timings, and an overtime penalty.
- This document covers Steps 1–14 (research → strategy → mock debate → judging → repairs). After approval, Step 15 builds the HTML War Room.
- Skills repo (biyachuev/claude-debate-skills): two of its three skills need Codex. I'm using its creator–critic method instead (value / flaw / hidden assumption / failure scenario) for the red-team passes below. Nothing gets installed.
- Assumption: create branch `debate-generator` as requested and push there. This replaces the session default branch.

---

## 1. Debate theory in use (why each technique works)
| Technique | Use here | Why it works |
|---|---|---|
| Burden of proof | G5 proposes changing the law, so they must show a definable wrong, a standard platforms can meet, net benefit, and that it beats alternatives | Judges reward the team that sets the test. The other side then spends its time meeting our test. |
| Framing / weighing | "Everyone wants less misinformation. The question is whether lawsuits get us there." | It moves the debate from intentions (where they win) to mechanisms (where we win). |
| Strategic concession | Concede harm, platform influence, and imperfect Section 230 | Conceding the obvious builds credibility and narrows the clash to our strongest ground. |
| "Even if" layering | "Even if algorithms amplify, X still follows" | One lost premise doesn't sink the argument. |
| Fork questions | Every trap gives two or three answers, and each one costs them something | A nuanced answer can't escape a real dilemma, but it can escape a cheap gotcha. |
| Attacking assumptions | Dependency map (Section 5) | Knocking out one assumption takes down an entire family of arguments. |
| Flowing | 7-field note template, by domain | Dropped arguments lose debates. Domain ownership means nothing gets dropped. |
| Signposting + landing lines | Every speech has STOP HERE points | Prevents overtime and keeps the structure clear for judges. |

Sources: WUDC Debating & Judging Manual; WSDC burden guidance (opposition must cast more than reasonable doubt; both teams share the burden of clash).

## 2. Motion definitions (Step 3)
- **Online platform:** deliberately broad. It means any service that hosts or distributes content its users create, not just Facebook/X/TikTok. See Section 2A for the spectrum and the legal distinctions. We use the breadth as a **test** of G5's rule, not as a technicality.
- **User-posted:** the platform didn't create it. Content the platform creates or materially develops is already outside Section 230 (*Roommates.com*, 9th Cir. 2008).
- **Misinformation:** false or misleading content regardless of intent. It is NOT a legal category. Distinguish it from:
  - disinformation (intentional)
  - defamation (false fact about an identifiable person; already actionable against the speaker)
  - fraud (already illegal)
  - opinion, satire and predictions (not falsifiable)
  - disputed claims
  - harmful-but-legal content
- **Legally liable:** civil damages or penalties. There are four possible standards:
  - strict (liable regardless of knowledge)
  - negligence (failed reasonable care)
  - knowledge/notice (liable after being told)
  - own-conduct (liable for its own acts)
- **Conduct spectrum:** host → rank/recommend → amplify → monetise → edit → co-create → knowingly distribute illegal content. Liability rises as we move right, toward the platform's own conduct.

### FINAL POSITION (stress-tested)
> **"Platforms shouldn't be legally liable because a user posted something false. They should answer for their own conduct — their own speech, their own product design, knowingly helping illegal activity — and for content a court or a clearly written law has already defined as illegal."**

- **Memorise:** "Liability for what platforms *do* — not for what users *say* that turns out to be untrue."
- **Bright line:** illegality and conduct trigger liability. Falsity alone does not.
- This blocks "platforms can do anything" and survives G5's best retreat ("knowingly monetising known falsehoods after notice"): notice of "misinformation" is still notice of a *disputed claim*.
- Rejected wording: "only after notice." It concedes too much, because notice-based liability for falsity still forces the platform to judge truth.

## 2A. "Online platforms" is deliberately broad: the platform spectrum
**P1 opening line:** "The motion says *online platforms*. That isn't just Facebook. It's Reddit, Wikipedia, YouTube, a newsletter host, a local paper's comment section, a 2,000-member hobby forum. Any liability rule has to work across all of them, or tell us exactly where it stops."

### What US law actually does: same baseline, different outcomes
- **FACT: one broad baseline.** §230 protects any "provider or user of an interactive computer service" for content provided by *another* information content provider (E1). It isn't size-based or social-media-only, and it covers individual users who repost others' content (*Barrett v. Rosenthal*, Cal. 2006, E22). Courts have also rejected notice-based "distributor" liability (*Zeran v. AOL*, 4th Cir. 1997, E23).
- **FACT: outcomes still diverge by conduct, control and context.** Never say every service gets identical treatment. The differences:
  - **The platform's own content or "material contribution" isn't protected:** *Roommates.com* (2008). "Neutral tools" like an aggregate star rating stay protected (*Kimzey v. Yelp*, 9th Cir. 2016, E24).
  - **Product-design claims proceed:** *Lemmon v. Snap*; the 2026 jury verdicts (E8).
  - **Algorithmic curation is contested:** treated as the platform's own speech in the 3rd Circuit (*Anderson*, E7) and as protected expression under *Moody* (E5). The Supreme Court hasn't resolved it.
  - **Statutory exclusions apply to every service:** federal criminal law, IP, and sex trafficking under FOSTA (E1, E15). Copyright has its own conditional safe harbour (DMCA §512, which requires a takedown process).
  - **Some state laws target only large platforms:** Texas HB 20 (>50M monthly US users) and Florida SB 7072 (revenue/user thresholds), both reviewed in *Moody* (E25; verify the exact thresholds).
- **FACT: other democracies tier by function and size:**
  - **EU DSA:** separate regimes for "mere conduit", caching and hosting (Arts. 4–6). Micro/small platforms are exempt from most platform duties (Art. 19). Extra duties apply only to very large platforms with ≥45M EU users (Art. 33) (E26).
  - **UK Online Safety Act:** Category 1 requires a recommender system plus >34M UK users, or >7M with resharing; Category 2B covers >3M with direct messaging (E27).
  - **Germany NetzDG:** exempted platforms under 2M registered users and set 24h removal only for *manifestly unlawful* content (E28).
- **INFERENCE:** every serious regime distinguishes platforms by function, size, control and knowledge, and triggers duties on illegality or systemic process. None imposes liability on a hosting service simply because a user's post is false.

### The spectrum (what changes legally and practically)
| Category | Example | Control / knowledge | Legally relevant distinction | Why falsity liability fits badly |
|---|---|---|---|---|
| Large algorithmic social network | Facebook, TikTok, X | ML ranking, ads, huge moderation budget | Design claims proceed (E8); curation is contested (E5/E7); size-tiered duties abroad (E26–27) | Even here: no truth referee at scale (E10, E11) |
| Video/audio host | YouTube, podcast hosts | Recommendations; monetisation via partner programmes | Monetisation and ads are the platform's own commercial conduct | Liability should attach to the conduct (paying for or promoting content), not the falsity |
| Volunteer-moderated community | Reddit, Discord servers | Users vote; volunteer moderators decide | §230 protects *users*; Reddit argued votes and moderators are protected (E29) | Who's liable: the company or the volunteer who actually saw it? |
| Small independent forum | Hobby/local/patient forums | One volunteer admin, chronological threads, no algorithm | Same §230 baseline; exempt from DSA Art. 19 and NetzDG duties | Can't afford lawyers or moderators, so it shuts or bans topics; no amplification exists to blame |
| Comment section | Local news site, business page | Owner writes the article but not the comments | US: §230 covers comments. Abroad: *Delfi* (2015) allowed liability for clearly unlawful hate speech; *MTE v. Hungary* (2016) rejected it for offensive comments; *Voller* (Aus. 2021) made page owners publishers (E30) | After *Voller*, CNN restricted its Facebook pages in Australia (E31) |
| Blogging / newsletter host | Substack, Medium, WordPress.com | Hosts authors and sometimes promotes or pays them | Editorial picks and payments are the platform's own conduct; ordinary hosting is not | The author is identifiable and already liable |
| Review site | Yelp, Tripadvisor, Google reviews | Aggregates opinions | *Kimzey*: aggregate rating is a neutral tool (E24) | Reviews are opinions and disputed facts, the hardest truth calls |
| Collaborative knowledge | Wikipedia | Volunteer editors; the foundation doesn't edit articles | Wikimedia challenged the UK categorisation rules (E27) | Liability would fall on a non-profit for volunteers' good-faith edits |
| Private/encrypted messaging | WhatsApp, Signal | Provider *cannot read* end-to-end messages | UK Category 2B duties; encryption limits knowledge | A knowledge standard is impossible without breaking encryption |
| Infrastructure | Web hosts, CDNs, search | No relationship to individual posts | DSA mere conduit/caching; §230 "access software provider" | Liability here means blocking whole sites |

### THE FIVE-QUESTION TEST (one question per person, asked of any G5 standard)
| Question | Owner | Why it bites |
|---|---|---|
| **Which platforms?** | P1 | All of them hits forums, Wikipedia and comment sections. Only big ones means size is the trigger, not misinformation. |
| **What knowledge?** | P2 | General awareness vs. this-post knowledge vs. notice. Encrypted services know nothing. |
| **What conduct?** | P3 | Hosting, ranking, monetising or co-creating? Each gives a different answer, and conduct is our line. |
| **What control?** | P4 | Company, volunteer moderator, or nobody (encryption)? Liability without control just produces shutdowns. |
| **What threshold?** | P5 | Strict, negligence or notice? 2M, 34M or 45M users? Every line is arbitrary for *falsity* but sensible for *process duties*. |

### The two-platform stress test (use in rebuttal)
These are labelled hypotheticals for illustration, not real data:
- **"MegaFeed"**: 3 billion users, ML-ranked feed, ad revenue, a 10,000-person moderation team.
- **"Riverside Cyclists Forum"**: 2,000 members, one volunteer admin, chronological threads, no ads.

Apply G5's principle to both:
- **Same rule for both:** the forum can't comply, so it closes, bans topics, or goes offline. The forum has no algorithm, so "amplification" was never the reason for liability.
- **Different rules:** then what triggers liability is size, design and conduct, not user misinformation. That's our position.
- **Threshold:** where, and why? A false post doesn't become more false at user 45,000,001. Size is a good reason for **process duties** (audits, transparency), which we support. It isn't a reason to impose liability for falsity.

## 3. Evidence vault (label: FACT / INFERENCE / ARGUMENT)

| # | Claim | Label | Source |
|---|---|---|---|
| E1 | §230(c)(1): no provider "shall be treated as the publisher or speaker" of another's content. §230(e) excludes federal criminal law, IP, ECPA, and sex-trafficking claims (FOSTA). | FACT | law.cornell.edu/uscode/text/47/230 |
| E2 | Section 230 responded to *Stratton Oakmont v. Prodigy* (1995): a moderating service was treated as publisher. *Cubby v. CompuServe* (1991): a non-moderating one was not. This created the "moderator's dilemma". | FACT | Cornell LII / case reporters |
| E3 | *Smith v. California* (1959): strict liability for a bookseller is unconstitutional. It would make the seller restrict even protected material. | FACT | supreme.justia.com/cases/federal/us/361/147 |
| E4 | *U.S. v. Alvarez* (2012): false statements are not, as a category, outside First Amendment protection. | FACT | law.cornell.edu/supremecourt/text/11-210 |
| E5 | *Moody v. NetChoice* (2024): curating and ranking feeds is expressive activity protected by the First Amendment. | FACT | supremecourt.gov/opinions/23pdf/22-277_d18f.pdf |
| E6 | *Twitter v. Taamneh* (2023), unanimous: recommendation algorithms as "agnostic" infrastructure did not amount to aiding and abetting. *Gonzalez v. Google* (2023) was vacated without reaching §230. | FACT | supremecourt.gov/opinions/22pdf/21-1496_d18f.pdf ; 21-1333 |
| E7 | *Anderson v. TikTok* (3d Cir. 2024): algorithmic recommendation is first-party speech, so not §230-protected. **This is a G5 weapon.** | FACT | ca3 opinion; Goldman blog critique |
| E8 | Courts already reach platform conduct: *Lemmon v. Snap* (9th Cir. 2021), design defect not barred; LA jury (Mar 25 2026, KGM v. Meta/YouTube), negligent design, $6M total; New Mexico jury v. Meta, $375M. | FACT | CNBC 2026-03-25; CalMatters |
| E9 | SCOTUS denied cert in *Doe v. X Corp.* (No. 25-949) on May 18 2026. §230 scope is still unresolved at the Supreme Court. | FACT | scotusblog.com/cases/doe-v-x-corp |
| E10 | Meta (Jan 7 2025): removed millions of items daily; estimated 1–2 in 10 removals in Dec 2024 "may have been mistakes". | FACT (company estimate) | about.fb.com/news/2025/01/meta-more-speech-fewer-mistakes |
| E11 | Facebook banned "man-made COVID" claims ~Feb 2021 and reversed on May 26 2021, citing ongoing investigations. | FACT | Fortune 2021-05-27 |
| E12 | Vosoughi, Roy & Aral, *Science* 2018: false news was ~70% more likely to be retweeted. The gap remained after removing bots, so humans drove it. The study counted only stories where six fact-checkers agreed ≥95%. | FACT | doi.org/10.1126/science.aap9559 |
| E13 | Guess et al., *Science* 2023: switching to a chronological feed *increased* exposure to untrustworthy-source content and did not reduce polarisation over 3 months. Contested: Grabowicz et al. cite 63 "break-glass" changes. | FACT + caveat | doi.org/10.1126/science.abp9364 |
| E14 | DMCA notice-and-takedown (Urban, Karaganis & Schofield, 2016/17): ~31% of sampled Google Search notices were questionable; ~70% in the Image Search sample. | FACT | papers.ssrn.com/abstract=2755628 |
| E15 | FOSTA (2018): GAO-21-385 found 1 criminal case in 3 years. Craigslist shut its US personals: "Any tool or service can be misused." | FACT | gao.gov/products/gao-21-385 ; NPR 2018-03-23 |
| E16 | Community Notes, *PNAS* 2025 (Slaughter, Saveski et al.): after a note was attached, reposts fell 46%; over the post's lifespan, about 12%. | FACT | pmc.ncbi.nlm.nih.gov/articles/PMC12478135 |
| E17 | EU DSA (Reg. 2022/2065): hosting safe harbour retained (Art. 6), no general monitoring obligation (Art. 8), systemic-risk duties for very large platforms (Arts. 34–35). Even the strictest regulator doesn't make platforms liable for user falsehoods. | FACT + INFERENCE | eur-lex.europa.eu/eli/reg/2022/2065/oj |
| E18 | TAKE IT DOWN Act (2025): 48-hour removal of nonconsensual intimate images after a valid request; FTC enforcement since May 19 2026. This is narrow, defined-category regulation. | FACT | ftc.gov |
| E19 | Speaker liability works: Dominion–Fox settlement $787.5M (2023); Sandy Hook verdicts against Alex Jones. | FACT | court/press records |
| E20 | Cost estimates: a baseless suit costs up to ~$80k (Engine) or ≥$100k (CCIA). These are **industry estimates**; say so aloud. | FACT (industry claim) | engine.is ; ccianet.org |
| E21 | Sunset Section 230 Act (Graham/Durbin, bipartisan) proposes 230 expire unless reform is negotiated. Current status is unverified; recheck before the debate. | FACT | Senate press |
| E22 | *Barrett v. Rosenthal* (Cal. 2006): §230 protects individual *users* who republish others' content, even after notice. The court acknowledged "troubling consequences". | FACT | 40 Cal.4th 33 |
| E23 | *Zeran v. AOL* (4th Cir. 1997): §230 bars notice-based "distributor" liability. | FACT | 129 F.3d 327 |
| E24 | *Kimzey v. Yelp* (9th Cir. 2016): an aggregate star rating is a neutral tool, so Yelp isn't the author of the review. | FACT | Goldman blog 2016-09 |
| E25 | Texas HB 20 covered platforms with >50M monthly US users; Florida SB 7072 used revenue/user thresholds. Both were remanded in *Moody* (2024). | FACT (verify thresholds) | supremecourt.gov 22-277 |
| E26 | EU DSA: Arts. 4–6 cover conduit, caching and hosting; Art. 19 exempts micro/small platforms; Art. 33 designates VLOPs at ≥45M EU users. | FACT | eur-lex 2022/2065 |
| E27 | UK OSA Threshold Regulations 2025: Category 1 = recommender + >34M UK users, or >7M + resharing; Category 2B = >3M + direct messaging. Wikimedia sought judicial review. | FACT | legislation.gov.uk/ukdsi/2025/9780348267174 |
| E28 | Germany NetzDG: platforms with <2M registered users exempt; 24h removal for *manifestly unlawful* content, 7 days otherwise. | FACT | CDT overview |
| E29 | Reddit's *Gonzalez* amicus (2023): user votes and volunteer moderation depend on §230's protection for *users*. | FACT (party's argument) | supremecourt.gov 21-1333 Reddit brief |
| E30 | *Delfi v. Estonia* (ECtHR GC 2015): commercial news portal liable for clearly unlawful hate speech/threats in comments. *MTE v. Hungary* (2016): liability for merely offensive comments violated Art. 10; notice-and-takedown can be appropriate. *Fairfax v. Voller* [2021] HCA 27: page owners are publishers of Facebook comments. **G5 weapons; none concerns misinformation as such.** | FACT | Stanford WILMap; hcourt.gov.au |
| E31 | After *Voller*, CNN restricted its Facebook pages for Australian users (Sept 2021), saying Facebook would not let it disable comments page-wide. | FACT | Mediaweek; AdNews 2021-09 |

Before the debate, recheck E21 and the current §230 docket.

## 4. Group 5's predicted AI case (steelmanned), with two rounds of clash
Format for each entry:
- **Claim**
- **Why judges like it**
- **Hidden assumption**
- **Us → Them → Us** (rebuttal, their counter, our counter-counter)
- **Escape → Final** (their best escape, our final response)
- **Concede / Never concede**

The HTML holds the full 11-field version.

1. **Profit from engagement**
   - Claim: they profit from virality, so they should bear the costs.
   - Hidden assumption: profit from a system = responsibility for each piece of content.
   - Us: profit is also earned from true content. Profit tells you who to regulate, not what standard to apply. Liability for falsity forces removal of disputed content, not accuracy.
   - Them: "Banks profit from transactions and must stop fraud."
   - Us: Banks act on *defined* illegality (fraud, laundering), not on "false statements". That's our line.
   - Escape → Final: "Monetised misinformation specifically." Then the target is ad policy and design — the platform's own conduct.
   - Concede: profit motives distort incentives.
   - Never concede: profit ⇒ content liability.
2. **Algorithms amplify, so the platform is an active participant**
   - Us: amplification is the platform's conduct, so regulate the system (design, transparency, DSA-style risk audits). But Moody says curation is protected speech, and Alvarez says false speech is generally protected. Their "first-party speech" theory walks into the First Amendment.
   - Them: Anderson v. TikTok.
   - Us: Anderson was about pushing a lethal challenge to a child — a dangerous-product/conduct claim, which our line already covers. Its reasoning has been sharply criticised, and the Supreme Court hasn't adopted it (Doe v. X cert denied 2026).
   - Escape → Final: chronological feed (E13). Removing ranking didn't reduce untrustworthy content in the best natural experiment. Humans spread falsehood (E12).
3. **Real-world harm (public health, elections, violence)**
   - Concede: the harm is real.
   - Us: harm proves a problem, not that this remedy works. The question is whether lawsuits over falsity reduce the harm or just remove contested speech, including the true speech (E11).
   - Them: "Some harm is clear-cut: 'drink bleach'."
   - Us: clear-cut dangerous content is already removable under platform policy. Where it's illegal, a defined law can address it (E18). The fight is over the grey zone, which is where liability does damage.
4. **Duty of care / negligence / foreseeability**
   - Us: duty of care for *design* is already being litigated and won (E8) — conduct. A duty of care for the *truth of billions of posts* has no workable "reasonable" standard. Juries would decide truth after the fact.
   - Them: "UK Online Safety Act does it."
   - Us: the UK model is a systems/process duty enforced by a regulator, not private suits over individual falsehoods. That's our alternative.
5. **"They already moderate, so they can do more"**
   - Us: moderating under your own policy is different from moderating under threat of a lawsuit. Errors are already 1–2 in 10 (E10). Liability makes removing a mistake free and leaving it up costly.
   - Them: "Errors are acceptable."
   - Us: the errors fall on true speech too (E11).
   - Escape → Final: "Good-faith safe harbour." That's a notice/process regime, i.e. our position.
6. **Publishers are liable, so platforms should be too**
   - Us: a publisher selects each item before publication. Platforms carry billions of posts that no one sees beforehand.
   - Them: "Algorithms select."
   - Us: → T4 fork (recommendation vs hosting).
   - Final: even newspapers are liable only with fault (Sullivan). They're asking for more liability for platforms than newspapers have.
7. **Product liability**
   - Concede: design can be a defect (E8).
   - Us: a product-defect claim targets the design, not the falsity of a user's sentence. That proves our line exists and works.
8. **Victims need remedies**
   - Us: victims can sue the speaker (E19). Platforms aren't immune for their own conduct, design, or federal crimes (E1).
   - Them: "Anonymous speakers."
   - Us: subpoenas for identity exist. Fix the identification gap, not the liability rule.
   - Final: who sues for "misinformation" — anyone misled? → T8.
9. **"No liability = no incentive"**
   - Us: they moderate now without liability (advertisers, users, regulators, DSA).
   - Them: "Not enough."
   - Us: then debate *how much and what kind* of incentive. Liability for falsity produces removal, not accuracy (DMCA E14, FOSTA E15).
10. **AI makes moderation feasible**
    - Us: AI predicts what humans labelled false in the past. It can't adjudicate new disputed claims — exactly the ones that matter. Meta's 2025 own admission (E10).
    - Them: "AI is improving."
    - Us: better tools are an argument for better voluntary systems, not for liability that punishes every miss.
11. **Section 230 is outdated (1996)**
    - Concede: it deserves review.
    - Us: the motion isn't "reform 230". It's liability for user falsehood. Courts are already narrowing 230 for conduct (E7, E8).
    - Final: even the EU kept the hosting safe harbour (E17).
12. **Other industries are liable for harms they facilitate**
    - Us: they're liable for defects in what *they* make, not for what customers say. Phone companies aren't liable for lies told on calls.
    - Them: "Platforms aren't phone companies; they curate."
    - Us: curation is protected speech (E5). Curating true and false content alike isn't knowing participation (E6).
13. **Platforms know misinformation exists / repeat offenders**
    - Us: general knowledge that falsehood exists ≠ knowledge that *this* post is false (Taamneh logic, E6).
    - Repeat offenders: account-level enforcement is a policy tool; we support transparency on it.
    - Final: knowledge-based liability tells platforms to stop looking (E2).
14. **Power and influence like a utility; the EU does it**
    - Us: the EU does *not* do it (E17). It regulates systemic risk and process. We endorse that model.
15. **Fraud, scam ads, defamation**
    - Concede: fraud is already illegal. Paid ads are the platform's own commercial conduct, and liability there is consistent with our line.
    - Defamation: liability stays with the speaker; the court decides truth.

## 5. Argument dependency map (the 5 foundational assumptions)
| Foundational assumption | G5 arguments resting on it | How we attack it | What remains if we win |
|---|---|---|---|
| F1 Misinformation can be reliably identified at scale | 3, 4, 5, 10, 13 | E11 lab-leak reversal; E10 error rate; E12 relied on ≥95% fact-checker agreement (easy cases only); E4 | Defined illegal categories, which we accept |
| F2 Liability produces accuracy, not just removal | 1, 5, 8, 9 | Asymmetric cost; E14 DMCA; E15 FOSTA; E2 moderator's dilemma | Liability for the platform's own conduct |
| F3 Distributing = authoring/causing | 1, 2, 6, 7, 12 | E6 Taamneh; E12 human spread; E13; E5 (if it's the platform's speech, it's protected speech) | Design-defect claims (E8), which fit our line |
| F4 Current law leaves victims with nothing | 8, 11, 15 | E19 speaker liability; E1 exclusions; E8 design verdicts | Anonymity gap → targeted identification tools |
| F5 Scale/power justifies content liability | 12, 14, 11 | E17 DSA keeps the safe harbour; regulate process, not speech | Transparency/audit regulation, which we endorse |
| F6 "Online platforms" are one kind of actor with similar knowledge, control and capacity | 1, 2, 4, 5, 9, 10, 14 | Two-platform test; Five-Question Test; every regime tiers by function and size (E25–E28); encrypted services can't know; volunteer moderators (E29) | Size- and design-scaled *process* duties, which we endorse. Not falsity liability. |

**G5 escapes on platform scope:**
- **"We only mean big algorithmic platforms."**
  - Response: then the motion has shrunk from "online platforms" to a handful of companies, and the trigger is scale and design, not user misinformation.
  - Even for those, F1 (no reliable truth referee) and F2 (liability drives removal, not accuracy) still hold.
  - The real regimes for those companies (DSA VLOPs, UK Category 1) impose process duties and keep the hosting safe harbour.
- **"Europe and Australia already do it" (*Delfi*, *Voller*).**
  - Response: *Delfi* was limited to clearly unlawful hate speech and threats on a commercial news portal. The same court in *MTE* refused liability for merely offensive comments.
  - *Voller* is Australian defamation law, not misinformation. Its practical result was CNN restricting its Facebook pages in Australia. Both cases illustrate our line: illegality, not falsity.

## 6. Group 6 core case (red-teamed twice)
Scored on support, logic, simplicity, resilience, and how fast it can be explained.
- **Kept:** A1–A4.
- **Cut:**
  - "chilling effect" in the abstract
  - "end of the internet"
  - "platforms are neutral"
  - "censorship"
  - "small platforms will die" as a standalone argument; demoted to support for A2, because G5 answers it with a size exemption.

**A1 — Liability needs a definable wrong (P1)**
- Mechanism: every standard fails or collapses into our position.
  - Strict liability: unconstitutional in spirit (E3), and total removal.
  - Negligence: no "reasonable care" for truth across billions of posts.
  - Notice: rewards not looking and invites abusive notices (E14).
- Attack 1: "Legislature will define it." Repair: then the motion is a blank cheque. Judges can't weigh an undescribed mechanism.
- Attack 2: "Notice + clear falsity." Repair: who certifies "clear"? → A2.

**A2 — Nobody can be a reliable referee of truth at speed (P2)**
- Mechanism: truth is often disputed and evolving. Liability makes the platform decide in seconds, under penalty.
- Evidence: E11, E12, E4.
- Attack 1: "Courts decide truth in defamation." Repair: yes — one statement, one identifiable victim, after trial, with fault standards (Sullivan). Not a moderator in seconds.
- Attack 2: "Only liable for obvious falsehoods." Repair: obvious falsehoods are already removed under policy. Liability only bites in the grey zone, where the errors are.

**A3 — Responsibility follows conduct (P3)**
- Mechanism: the user authors. The platform is accountable for what it does — its own speech, design, ads, or knowing help with crime — and the law already reaches that (E8, E19, E1).
- Attack 1: "Amplification is conduct." Repair: agreed. Regulate amplification as design (DSA audits). Falsity-based liability adds nothing but a truth referee. Chronological feeds don't fix it (E13).
- Attack 2: Anderson v. TikTok. Repair: see Section 4, #2.

**A4 — Liability gets removal, not accuracy; better tools exist (P4 + P5)**
- P4 (mechanism): asymmetric cost leads to over-removal or wilful blindness (E2, E10, E14, E15).
- P5 (comparison): context labels (E16), process regulation (E17), defined-category laws (E18), speaker liability (E19).
- Attack 1: "Over-removal of misinformation is fine." Repair: the errors include true speech and whistleblowers, and they hit smaller platforms hardest.
- Attack 2: "Community Notes are slow/voluntary." Repair: we don't claim self-regulation is enough. We support regulation of process. We oppose liability for content.

**Weighing (P5 + P1, in final):** compare the mechanisms. Theirs depends on a truth referee that doesn't exist and produces removal. Ours targets conduct, which the law can actually prove.

## 7. Socratic traps (16) — Bait → Commitment → Fork
Each one in the HTML will have opening, likely answer, follow-up, YES/NO/QUALIFIED branches, concession won, escape, and our reply to the escape.

| # | Owner | Opening question | Fork | Concession won |
|---|---|---|---|---|
| T1 | P1 | "Which legal standard: strict, negligence, or after notice?" | Strict → Smith v. California; negligence → who defines reasonable for truth?; notice → you've abandoned "merely because users post" | They must pick, and each choice costs |
| T2 | P2 | "Who decides what counts as misinformation: platform, court, or government?" | Platform → private truth-arbiter under lawsuit pressure; court → too slow, so the platform decides first anyway; government → would you give that power to an administration you disagree with? | A truth-arbiter is required |
| T3 | P2 | "Can something labelled misinformation later become mainstream?" | Yes → liable for hosting it, or for removing it?; No → E11 | Truth evolves |
| T4 | P3 | "Is it recommending, or hosting, that creates responsibility?" | Recommending → pure hosting is fine: motion conceded; hosting → algorithms were never their reason; qualified → amplification is conduct: our line | Hosting alone isn't enough |
| T5 | P3 | "When a user posts a lie, who's first responsible?" | User → why isn't speaker liability enough?; escape "anonymous" → identification fix | Primary responsibility lies with the speaker |
| T6 | P4 | "Would you accept removing some true posts to catch more false ones?" | Yes → how many? 1–2 in 10 already; No → you can't back a rule whose rational outcome is over-removal | Error costs count |
| T7 | P4 | "Does AI decide what's true, or predict what was labelled false before?" | Predicts → new disputed claims escape it; decides → who audits it? | AI ≠ truth |
| T8 | P5 | "Who exactly gets to sue: the harmed person or anyone misled?" | Specific person → defamation/fraud already exist; anyone → millions of plaintiffs; government → Alvarez/capture | Remedy already exists or explodes |
| T9 | P5 | "If someone hears a claim on TV, from a friend, and online, then acts — who caused it?" | Causation is shared → why single out the platform? | Causation is diffuse |
| T10 | P1 | "Is a newspaper liable for letters it chooses to print? Does a platform choose each post beforehand?" | Yes it chooses → T4; No → the analogy breaks at selection | Publisher analogy fails |
| T11 | P5 | "If there's no liability now, why do platforms moderate at all?" | Advertisers/users → incentives exist; the question is what liability adds | "No incentive" is false |
| T12 | P1 | "Does your rule cover a 2,000-member hobby forum run by one volunteer?" | Yes → it closes or bans topics, and it has no algorithm, so amplification wasn't your reason; No → the trigger is size/design, not misinformation; Qualified ("proportionate") → then tell us the threshold → T13 | The motion's breadth is unworkable, or it's narrowed to our line |
| T13 | P5 | "Where's the line: 2 million, 34 million, 45 million users? Does a false post become actionable at user 45,000,001?" | Picks a number → that's a process duty for big services, which we support; no number → the rule hits everyone → T12; "the regulator decides" → a blank cheque | Size justifies process, not falsity liability |
| T14 | P4 | "On Reddit, who's liable: the company, or the volunteer moderator who actually saw the post?" | Company → the person with knowledge and control is exempt, so knowledge isn't your test; Moderator → you're suing volunteers; Both → who volunteers to moderate after that? | Liability must track control |
| T15 | P2 | "In an end-to-end encrypted group chat the provider can't read messages. Liable or not?" | Yes → only possible by breaking encryption; No → knowledge and control decide, not falsity; Qualified ("only public content") → private chats, where much misinformation travels, are excluded | Knowledge, not falsity, is the trigger |
| T16 | P3 | "Is a local newspaper liable for a false comment a reader leaves under its article?" | Yes → *Voller* outcome: comment sections close, as CNN's did in Australia; No → hosting without endorsement isn't enough, which is our position; Only if the paper promotes it → conduct, our line | Hosting ≠ authorship |

T9 is now a shared reserve trap; anyone can use it.

## 8. Five equal roles (Step 10)
| | P1 Frame & Law | P2 Truth & Expression | P3 Conduct & Algorithms | P4 Enforcement & Consequences | P5 Harm, Alternatives & Weighing |
|---|---|---|---|---|---|
| Opening (~55s) | Platform-spectrum line, motion definition, our line, burden test | A2 | A3 | A4 mechanism | A4 alternatives + "how we win" |
| Core argument | A1 | A2 | A3 | A4a | A4b + weighing |
| Monitors | Section 230 outdated, publisher, negligence/duty, legal standard | Public health, elections, "clearly false", free speech | Algorithms, profit, monetisation, product liability, Anderson | AI moderation, already moderate, repeat offenders, incentive | Harm, victims, other industries, EU/UK, fraud |
| Five-Question Test | **Which platforms?** | **What knowledge?** | **What conduct?** | **What control?** | **What threshold?** |
| Traps | T1, T10, T12 | T2, T3, T15 | T4, T5, T16 | T6, T7, T14 | T8, T11, T13 |
| Key evidence | E1, E2, E3, E22, E23 | E4, E11, E12, E28 | E5, E6, E8, E13, E24, E30, E31 | E10, E14, E15, E29 | E16–E19, E25–E27 |
| Platform-scope duty | Opening spectrum line; "which platforms" fork | Encrypted/private services | Comment sections, video monetisation, blogs | Volunteer-moderated communities, small forums | Size thresholds; DSA/UK tiering |
| Emergency counter | "Which platforms does this cover?" | "Who decides, and how would they know?" | "Hosting or recommending?" | "Who has control here?" | "Where's the line, and why there?" |
| Backup for | P2 | P3 | P4 | P5 | P1 |

## 9. Speaking structure (configurable in HTML)
- **Opening 5:00:** P1 0:00–0:55 → P2 0:55–1:50 → P3 1:50–2:45 → P4 2:45–3:40 → P5 3:40–4:35. Then 25s buffer. Hard stop by 4:50.
- **Opening 3:00 fallback:** 35s each, with a 5s buffer.
- **Rebuttal 2:00:** P2, P3, P4 (~40s each). **1:00 fallback:** 20s each.
- **Final/collective rebuttal 2:00:** P5 (55s, weighing) → P1 (55s, close + one-sentence position).
- **Fairness check:**
  - P1/P5 total ≈ 110s; P2–P4 ≈ 95s.
  - P2–P4 carry the live rebuttal, which is the harder skill and offsets the time gap.
  - Every speaker owns 3 traps + 1 Five-Question Test question, roughly 1 core argument, and roughly 3 G5 families.
- **If the format turns out to be all-five-in-every-round:** use "relay mode" (≈20s each, with handoff lines).
- Every speech has four tiers: MUST SAY / GOOD TO SAY / CUT FIRST / STOP HERE (a landing sentence).
- **30s emergency closing:** "Everyone in this room wants less misinformation. The question tonight was whether making platforms legally liable for what users say gets us there. It doesn't. It forces someone to referee truth in seconds, it rewards removal over accuracy, and the law already reaches what platforms themselves do. Hold platforms to account for their conduct, not for their users' mistakes. We oppose."

## 10. Shared core (all five memorise)
- **Position:** the one-liner above.
- **Liability:** a legal duty to pay or face penalties. The question is *what triggers it*.
- **Burden challenge:** "Tell us the standard, who decides truth, and why it gives accuracy, not just removal."
- **Five-Question Test:** Which platforms? What knowledge? What conduct? What control? What threshold?
- **Two-platform test:** "Does your rule work for MegaFeed *and* a volunteer-run cycling forum? If not, the trigger isn't misinformation."
- **Three facts:**
  - E10: 1–2 in 10 removals mistaken.
  - E11: lab-leak ban reversed.
  - E17: the EU kept the safe harbour.
- **Three questions:** T1, T2, T4.
- **Three concessions:**
  - The harm is real.
  - Platforms aren't neutral.
  - §230 deserves review.
- **30-second philosophy:** "conduct, not content".
- **Emergency closing:** as in Section 9.

## 11. Mock debate (strong G5) + neutral judge (Steps 11–13)
**G5 best line**
- Leads with a teen-harm victim and the March 2026 verdicts: "the law is already moving our way".
- Narrows to "knowing amplification and monetisation of misinformation after notice".
- Cites Anderson.

**Judge verdict (first run): G5 narrowly ahead.** Reasons:
- G6 sounded abstract against concrete harm.
- G6 failed to separate "design verdicts" from "misinformation liability", so G5 claimed those cases as theirs.
- The notice retreat went unanswered for too long.
- Two rebuttal speakers chased minor points.

**Repairs adopted (already in the strategy above):**
1. Concede harm in the first 20 seconds of P1.
2. Make the bright line explicit: **illegality/conduct, not falsity**. KGM/New Mexico are design/conduct cases, so they support us.
3. Pre-load the answer to the notice retreat in P2: notice of a disputed claim still needs a truth referee, and E14 shows notice systems get abused.
4. Answer Anderson with the Moody/Alvarez fork in P3.
5. Use the listening triage rule: rebut only arguments that would decide the judge's ballot, i.e. that hit a foundational assumption (F1–F6). Ignore the rest.
6. **Platform-scope repair** (added after the scope review):
   - **G5's best adaptation:** in their opening they define the motion as "very large algorithmic platforms only".
   - **Risk:** if we complain about definitions, judges treat it as definitional whining and penalise it.
   - **Fix:** accept the narrowing gracefully ("Happy to debate the largest platforms"), then make two moves:
     1. The narrowing concedes that hosting user content isn't the trigger: size and design are.
     2. Even for the largest platforms, F1 and F2 still apply, and the real regimes for them (DSA VLOPs, UK Category 1) impose process duties, not falsity liability.
   - If G5 *doesn't* narrow, P1 runs T12 and P5 runs T13 to force them to.

**Re-run verdict: G6 narrowly ahead, on clash and weighing.**
- This depends on clean timing and holding the bright line.
- The Five-Question Test gave G6 a visible, repeatable structure. The judge noted that G5 answered "which platforms" and "what threshold" inconsistently across speakers.
- The HTML includes the full transcript and judge notes.

## 12. Do-not-say list
| Don't say | Why |
|---|---|
| "§230 gives total immunity" | False: criminal, IP, and FOSTA exclusions; the platform's own content isn't covered |
| "Misinformation isn't harmful" | Loses credibility |
| "Platforms are neutral" | Moody says curation is expressive |
| "1A protects all speech" | Fraud, defamation, and incitement aren't protected |
| "End of the internet" | Hyperbole |
| "Bots spread it" | E12: humans drive the spread |
| "Algorithms don't matter" | Overclaims a contested study |
| "Censorship" / "biased fact-checkers" | Sounds partisan |
| Partisan examples | Corporate setting |
| Unsourced statistics | Easy to expose |
| "Users should just be smarter" | Victim-blaming |
| "All online services are treated the same under the law" | False: own content, design claims, statutory exclusions and DMCA conditions differ, and foreign regimes tier by size (Section 2A) |
| "The motion is too vague, so you lose" | Judges penalise definitional complaints. Use the breadth as a test of their rule instead. |
| "Small platforms will all die" | Overclaim. Say "they face costs they can't absorb, so the rational move is to close or ban topics" (E20, E31). |

## 13. Listening system
- **Note template:** THEY CLAIM / EVIDENCE / HIDDEN ASSUMPTION / MY DOMAIN? / CONCEDE·NARROW·REFUTE·TURN·OUTWEIGH / BEST RESPONSE / QUESTION.
- **Triage — major:** it rests on F1–F5, introduces new evidence, or G5 repeats it. **Minor:** rhetoric, examples that rely on an assumption already answered, or tangents.

---

## Implementation (after approval)
1. `git checkout -b debate-generator`.
2. Create `debate/STRATEGY.md`: the full strategy, including the complete 11-field steelman entries, the full trap trees, the 15-row firewall (10s/30s spoken responses), the full mock-debate transcript, and the fairness table.
3. Create `debate/war-room.html`: a single self-contained file (HTML/CSS/vanilla JS, no external dependencies).
   - **Data layer:** a single `DATA` object holding persons, arguments, traps, firewall, evidence, sources, and mock debate. A `CONFIG.timings` block at the top so timings are easy to edit.
   - **Views:** Home (role picker) → Person view (12 sections, filtered by owner) / Team view (19 sections, sticky nav).
   - **Components:**
     - Progressive disclosure buttons: WHY / EVIDENCE / THEIR COUNTER / OUR RESPONSE.
     - Trap YES/NO/QUALIFIED reveal.
     - Firewall search and filter.
     - Live Debate Mode: 13 large topic buttons → 10s response, question back, key fact, owner.
     - Live Notes: 5 panes stored in localStorage, with try/catch.
     - Timer: presets 5:00/3:00/2:00/1:00/0:30, start/pause/reset; amber at 30s, red at 10s; optional sound via a toggle that defaults to off.
     - Emergency overlay.
     - Practice Mode: random argument → best response → their counter → final response.
   - **Visual tokens:** THEM / US / FACT / QUESTION / TRAP / WARNING. Neutral palette with light/dark tokens, responsive down to 360px, no gradients.
4. Verify:
   - Open with Playwright (`/opt/pw-browsers/chromium`) at 1280px and 390px.
   - Click through every view, run the timer, refresh to confirm notes persist, test the trap branches and search.
   - Check for console errors.
   - Grep for placeholders ("TODO", "lorem", "insert").
   - Confirm every source link resolves.
5. Commit and `git push -u origin debate-generator`. Optionally publish the HTML as a private Artifact for colleagues.
