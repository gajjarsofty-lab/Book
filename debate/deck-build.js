const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/01f17702-7b0d-4589-9cd3-2014a9a5364e_a898d5ca-e1be-434e-a62a-d418d813f0af/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";

const THEME = {
  name: "Group 6 Debate",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "16201D", lt1: "FFFFFF", dk2: "1D4D6A", lt2: "EEF2F1",
    accent1: "1D4D6A", accent2: "9B5A3C", accent3: "5B6763", accent4: "C9D8E1",
    accent5: "7FA3B8", accent6: "F3E8E1", hlink: "1D4D6A", folHlink: "1D4D6A"
  }
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Group 6 — Debate Deck";
pres.author = "Group 6";
const C = pres.SchemeColor;

// Slide numbers used by hyperlinks
const N = { position: 2, test: 8, menu: 9, duty: 10, publishers: 11, knew: 12, clearly: 13, algorithms: 14, profit: 15, incentive: 16, moderate: 17, harm: 18, law: 19, backdrop: 20 };

/* ---------------- Layouts ---------------- */
const label = (text, color) => ({ text: { text, options: { x: 0.6, y: 0.32, w: 4.0, h: 0.35, fontSize: 11, bold: true, color, charSpacing: 2, margin: 0 } } });

pres.defineSlideMaster({
  title: "OUR_CASE",
  background: { color: "FFFFFF" },
  objects: [label("OUR CASE", C.accent3)]
});
pres.defineSlideMaster({
  title: "OUR_CASE_ARG",
  background: { color: "FFFFFF" },
  objects: [
    label("OUR CASE", C.accent3),
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 1.15, w: 11.7, h: 1.1, fontSize: 44, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } }
  ]
});
pres.defineSlideMaster({
  title: "REBUTTAL_MENU",
  background: { color: "FFFFFF" },
  objects: [label("THEIR CASE  →  OUR RESPONSE", C.accent2)]
});
pres.defineSlideMaster({
  title: "REBUTTAL",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.5, w: 11.7, h: 1.45, fontSize: 36, bold: true, color: C.accent1, align: "left", valign: "top", margin: 0 }, text: "" } }
  ]
});

/* ---------------- Helpers ---------------- */
function card(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08,
    x, y, w, h, fill: { color: opts.fill || C.background2 },
    line: opts.line ? { color: opts.line, width: opts.lineW || 1.5 } : { type: "none" },
    fontSize: opts.size || 26, bold: opts.bold !== false, color: opts.color || C.text1,
    align: opts.align || "center", valign: "middle", margin: opts.margin !== undefined ? opts.margin : 8,
    objectName: opts.name, hyperlink: opts.link ? { slide: opts.link, tooltip: opts.tip || "" } : undefined
  });
}
function arrow(slide, x, y, w, h, color) {
  slide.addText("→", { x, y, w, h, fontSize: 30, color: color || C.accent3, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function progress(slide, current) {
  const stages = ["01 TRIGGER", "02 TRUTH", "03 CONDUCT", "04 CONSEQUENCES", "05 ALTERNATIVE"];
  stages.forEach((s, i) => {
    const on = i === current;
    slide.addText(s, {
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.2,
      x: 3.3 + i * 1.88, y: 0.24, w: 1.8, h: 0.44,
      fill: { color: on ? C.accent1 : C.background2 }, line: { type: "none" },
      fontSize: 12, bold: true, color: on ? C.background1 : C.accent3, align: "center", valign: "middle", margin: 0,
      charSpacing: 1, objectName: "Progress " + (i + 1)
    });
  });
}
function takeaway(slide, text, y) {
  slide.addText(text, { x: 0.8, y: y || 6.35, w: 11.7, h: 0.6, fontSize: 26, italic: true, color: C.accent1, margin: 0, isTextBox: true, objectName: "Takeaway" });
}
function navLinks(slide, items, y) {
  // items: [label, slideNumber]; right-aligned row of small links
  const w = 1.55; let x = 12.53 - items.length * w;
  items.forEach(([t, n]) => {
    slide.addText(t, { x, y: y || 6.85, w, h: 0.35, fontSize: 13, color: C.accent3, align: "right", valign: "middle", margin: 0, isTextBox: true, hyperlink: { slide: n, tooltip: t }, objectName: "Nav " + t });
    x += w;
  });
}

/* ---------------- Speaker notes ---------------- */
const MUST_BEAT = "THE VERSION OF GROUP 5 WE MUST BEAT\n\"Large platforms should face liability when they knowingly or negligently fail to address harmful misinformation that they amplify.\"\nEven under a negligence or notice standard, they still have to answer our five questions:\n1. TRIGGER (P1): what triggers the duty?\n2. TRUTH (P2): who determines falsity?\n3. CONDUCT (P3): what exactly did the platform do?\n4. CONSEQUENCES (P4): what will the liability rule reward?\n5. ALTERNATIVE (P5): is there a narrower way to target the actual harm?";

function argNotes(o) {
  return [
    "SPEAKER: " + o.who,
    "OBJECTIVE: " + o.objective,
    "",
    "THEIR STRONGEST CASE\n" + o.theirs,
    "",
    "OUR ARGUMENT (45–60s)\n" + o.ours,
    "",
    "KEY EXAMPLE\n" + o.example,
    "",
    "THEY MAY COUNTER\n" + o.counter,
    "",
    "OUR RESPONSE (10–15s)\n" + o.response,
    "",
    "QUESTION BACK\n" + o.question,
    "",
    "EVIDENCE\n" + o.evidence,
    o.also ? "\nALSO MINE IN REBUTTAL\n" + o.also : "",
    "",
    "HANDOFF\n" + o.handoff
  ].join("\n");
}
function rebNotes(o) {
  return [
    "OWNER: " + o.owner,
    "",
    "THEIR STRONGEST VERSION\n" + o.steel,
    "",
    "OUR 10-SECOND RESPONSE\n" + o.r10,
    "",
    "OUR 30-SECOND RESPONSE\n" + o.r30,
    "",
    "THEY MAY COUNTER\n" + o.counter,
    "",
    "OUR FINAL RESPONSE\n" + o.final,
    "",
    "QUESTION BACK\n" + o.question,
    "",
    "BEST EVIDENCE\n" + o.evidence,
    "",
    "WATCH OUT\n" + o.watch,
    "",
    "Then click ← Menu for the next argument."
  ].join("\n");
}

/* ================= SECTION: OUR CASE ================= */
pres.addSection({ title: "Our case" });

// 1 · The Question
{
  const s = pres.addSlide({ masterName: "OUR_CASE", sectionTitle: "Our case" });
  s.addText("WHO SHOULD BE LEGALLY RESPONSIBLE?", { x: 0.8, y: 1.15, w: 11.7, h: 1.0, fontSize: 48, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "Headline" });
  card(s, "A user posts\nsomething false", 0.8, 2.85, 3.45, 1.55, { name: "Step 1" });
  arrow(s, 4.25, 2.85, 0.68, 1.55);
  card(s, "A platform\nhosts it", 4.93, 2.85, 3.45, 1.55, { name: "Step 2" });
  arrow(s, 8.38, 2.85, 0.68, 1.55);
  card(s, "Someone\nis harmed", 9.06, 2.85, 3.45, 1.55, { name: "Step 3", fill: C.accent6 });
  s.addText("When does the platform become legally responsible?", { x: 0.8, y: 5.15, w: 11.7, h: 0.8, fontSize: 32, italic: true, color: C.accent1, margin: 0, isTextBox: true, objectName: "Question" });
  s.addNotes([
    "SPEAKER: P1 (opening)",
    "OBJECTIVE: Frame the debate around where legal responsibility begins, not whether misinformation is harmful.",
    "",
    "SAY (ACKNOWLEDGE)\n\"Let's start with what we agree on. Misinformation can cause real harm, and platforms have enormous influence over what people see.\"",
    "",
    "Point at the three steps: a user posts, a platform hosts, someone is harmed. Then: \"Tonight's real question is the last line: when does the platform become legally responsible?\"",
    "",
    "Advance to the next slide."
  ].join("\n"));
}

// 2 · Our Position
{
  const s = pres.addSlide({ masterName: "OUR_CASE", sectionTitle: "Our case" });
  s.addText("MISINFORMATION CAN CAUSE REAL HARM.", { x: 0.8, y: 1.2, w: 11.7, h: 1.1, fontSize: 42, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "Statement" });
  s.addText("But harm alone does not answer who should be legally liable.", { x: 0.8, y: 2.5, w: 11.7, h: 0.7, fontSize: 30, color: C.accent3, margin: 0, isTextBox: true, objectName: "Gap" });
  s.addText([
    { text: "Hold platforms accountable for what ", options: {} },
    { text: "they do", options: { bold: true, color: C.accent1 } },
    { text: ",", options: { breakLine: true } },
    { text: "not simply for what ", options: {} },
    { text: "users say", options: { bold: true, color: C.accent1 } },
    { text: ".", options: {} }
  ], { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: 0.8, y: 4.0, w: 11.7, h: 2.0, fill: { color: C.background2 }, line: { type: "none" }, fontSize: 34, color: C.text1, valign: "middle", margin: [0, 30, 0, 30], objectName: "Principle" });
  s.addNotes([
    "SPEAKER: P1 (opening, continued)",
    "OBJECTIVE: Show we are not defending misinformation, and separate harm from liability before Group 5 merges them.",
    "",
    "SAY (CLASH)\n\"Our disagreement isn't about whether the problem matters. It's about whether making a platform legally responsible for determining the truth of what someone else says actually solves it.\"",
    "",
    "SAY (FRAME)\n\"So throughout this debate, we're going to ask one simple question: what exactly triggers liability?\"",
    "",
    "Land the bottom line slowly: they do / users say.",
    "",
    "Advance to P1 · Trigger."
  ].join("\n"));
}

// 3–7 · Argument slides
// 3 · P1 Trigger
{
  const s = pres.addSlide({ masterName: "OUR_CASE_ARG", sectionTitle: "Our case" });
  progress(s, 0);
  s.addText("WHEN DOES LIABILITY BEGIN?", { placeholder: "title" });
  card(s, "False post?", 0.8, 2.75, 3.45, 1.45, { size: 32, name: "Cue 1" });
  arrow(s, 4.25, 2.75, 0.68, 1.45);
  card(s, "Notice?", 4.93, 2.75, 3.45, 1.45, { size: 32, name: "Cue 2" });
  arrow(s, 8.38, 2.75, 0.68, 1.45);
  card(s, "Failure to act?", 9.06, 2.75, 3.45, 1.45, { size: 32, name: "Cue 3" });
  takeaway(s, "A legal rule needs a clear trigger.", 5.95);
  s.addNotes(argNotes({
    who: "P1 · TRIGGER",
    objective: "Make Group 5 name the exact trigger for liability. Pressure-test: what exactly creates the duty?",
    theirs: "\"We're not asking for automatic liability. Every business has a duty of care. Once a platform knows harmful misinformation is spreading and does nothing, that's negligence, like a store ignoring a spill it's been told about.\"\n\n" + MUST_BEAT,
    ours: "\"Fair, and that's a narrower rule than the motion sounds. So let's test it. What creates the duty: the post being false, someone reporting it, or the platform failing to act? If it's a report, a complaint isn't proof. The platform still has to decide whether the complaint is right. And 'reasonable steps' toward what: taking it down, or working out whether it's true? If it's taking it down, true posts go too. If it's checking the truth, the platform becomes the judge. We accept liability for a platform's own wrongdoing. We don't accept that someone else's false sentence creates the duty.\"",
    example: "A bookshop isn't liable for a false claim inside a book it sells but hasn't read. Courts rejected that idea decades ago, because shops would stop stocking anything risky.",
    counter: "\"Only for content that's clearly false and harmful.\"",
    response: "\"Who decides it's clearly false? If a court decides, we agree. If the company decides on a complaint, that's the problem.\"",
    question: "\"Under your rule, is a platform liable just because a user's post turns out to be false?\"\n  If yes: \"So a small forum is liable for a post nobody there has read?\"\n  If no: \"Then what's the extra step? That's a much narrower rule.\"\n  If 'only after notice': \"Told by whom? A complaint isn't proof.\"",
    evidence: "1. US Supreme Court (1959) rejected holding booksellers liable for books they hadn't read.\n2. US courts have rejected liability just because a platform was told about a post.",
    also: "Publisher comparison: \"Newspapers choose each piece before printing, and even they usually have to be at fault.\"",
    handoff: "\"And every one of those options needs someone to decide what's false. [P2].\""
  }));
}

// 4 · P2 Truth
{
  const s = pres.addSlide({ masterName: "OUR_CASE_ARG", sectionTitle: "Our case" });
  progress(s, 1);
  s.addText("WHO DECIDES WHAT IS FALSE?", { placeholder: "title" });
  ["Platform?", "Experts?", "Court?"].forEach((t, i) => card(s, t, 0.8, 2.6 + i * 0.98, 4.3, 0.82, { size: 30, align: "left", name: "Cue " + (i + 1) }));
  s.addText("And what happens while the facts are still disputed?", { x: 5.8, y: 2.6, w: 6.7, h: 2.78, fontSize: 32, italic: true, color: C.accent3, valign: "middle", margin: 0, isTextBox: true, objectName: "Disputed" });
  takeaway(s, "Liability requires someone to make the call.", 5.95);
  s.addNotes(argNotes({
    who: "P2 · TRUTH",
    objective: "Show that every liability rule needs a referee of truth, fast, under legal risk. Never say truth is subjective.",
    theirs: "\"Most misinformation isn't a philosophical puzzle. Fake cures, wrong voting dates, invented quotes. Platforms already work with fact-checkers and experts. It's not hard.\"",
    ours: "\"Agreed, plenty of it is clearly false, and platforms already remove a lot of that. A liability rule only changes behaviour in the hard cases, where facts are disputed or still coming in. Someone has to make the call quickly. A court takes months. So the platform decides, knowing it can be sued only for leaving things up. That isn't a recipe for accuracy.\"",
    example: "In 2021 Facebook followed the expert view and banned claims that COVID came from a lab, then reversed itself about four months later as investigations continued. Under liability, which decision should it have been sued for?",
    counter: "\"Courts decide truth all the time in defamation cases.\"",
    response: "\"One statement about one person, after a trial, usually with fault required. That doesn't help someone who has to decide today.\"",
    question: "\"When a post is disputed, should the platform itself decide, with a lawsuit if it's wrong?\"\n  If yes: \"So it can only be sued for leaving things up. Which way will it lean?\"\n  If no: \"Then who? A court takes months; the platform still guesses first.\"\n  If 'follow the experts': use the Facebook example.",
    evidence: "Facebook's 2021 ban on COVID-origin claims, reversed about four months later.",
    also: "\"They know misinformation is there\": \"Knowing it exists isn't knowing this post is false.\"\nFree speech: \"Fraud and defamation aren't protected, but a statement isn't unprotected just because it's false.\"",
    handoff: "\"So the real question is what the platform itself did. [P3].\""
  }));
}

// 5 · P3 Conduct
{
  const s = pres.addSlide({ masterName: "OUR_CASE_ARG", sectionTitle: "Our case" });
  progress(s, 2);
  s.addText("WHAT DID THE PLATFORM ACTUALLY DO?", { placeholder: "title" });
  card(s, "HOSTED", 0.8, 2.6, 3.45, 1.75, { size: 28, name: "Hosted" });
  arrow(s, 4.25, 2.6, 0.68, 1.75);
  card(s, "PROMOTED", 4.93, 2.6, 3.45, 1.75, { size: 28, fill: C.accent4, name: "Promoted" });
  arrow(s, 8.38, 2.6, 0.68, 1.75);
  card(s, "CREATED /\nKNOWINGLY PARTICIPATED", 9.06, 2.6, 3.45, 1.75, { size: 22, fill: C.accent1, color: C.background1, name: "Created" });
  s.addText("Where does responsibility actually begin?", { x: 0.8, y: 4.75, w: 11.7, h: 0.7, fontSize: 30, color: C.text1, margin: 0, isTextBox: true, objectName: "Question" });
  takeaway(s, "Responsibility should follow conduct.", 5.95);
  s.addNotes(argNotes({
    who: "P3 · CONDUCT",
    objective: "Separate what the platform did from what a user said. Concede that ranking is a platform choice; show that conduct, not falsity, is the right target.",
    theirs: "\"Platforms design algorithms that push outrage and falsehood to millions because it keeps people scrolling, and they profit from it. That's not hosting. That's participation.\"",
    ours: "\"I agree platforms aren't neutral. Ranking and recommending are choices, and when a platform's own choices cause harm, it should answer for them. Courts are already doing that: juries this year found against platforms over addictive design and a company's own misleading statements about safety. But that actually narrows the issue. If amplification is what creates responsibility, simply hosting can't be enough. If recommendation is the problem, regulate recommendation. That still doesn't make a platform liable because the underlying post is false.\"",
    example: "If a car maker builds faulty brakes, it's liable. If a passenger in the car tells a lie, it isn't. Same car, different responsibility.",
    counter: "\"One US appeals court has said the algorithm is the platform's own speech, so it can be liable.\"",
    response: "\"That case was about an app pushing a dangerous challenge to a child. That's the platform's conduct, which we agree can carry liability. It isn't a rule about users' false posts.\"",
    question: "\"If a site just shows posts in date order, with no recommending, should it be liable for a user's false post?\"\n  If yes: \"Then algorithms aren't your reason.\"\n  If no: \"So hosting isn't enough. It's what they do. That's our point.\"",
    evidence: "The March 2026 jury verdicts against platforms concerned addictive design and a company's own statements. They are jury decisions under appeal, not binding precedent, so don't overclaim them.",
    also: "\"They profit from it\": \"They profit from true posts too. Profit tells us who can afford rules, not which posts are false.\"",
    handoff: "\"So what would a rule like theirs actually make platforms do? [P4].\""
  }));
}

// 6 · P4 Consequences
{
  const s = pres.addSlide({ masterName: "OUR_CASE_ARG", sectionTitle: "Our case" });
  progress(s, 3);
  s.addText("WHAT DOES LIABILITY INCENTIVIZE?", { placeholder: "title" });
  s.addText([
    { text: "LEAVE IT UP", options: { bold: true, fontSize: 32, breakLine: true } },
    { text: "→  legal risk", options: { fontSize: 26 } }
  ], { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: 0.8, y: 2.6, w: 5.65, h: 1.8, fill: { color: C.accent6 }, line: { type: "none" }, color: C.text1, align: "center", valign: "middle", margin: 8, objectName: "Leave up" });
  s.addText([
    { text: "REMOVE IT", options: { bold: true, fontSize: 32, breakLine: true } },
    { text: "→  lower legal risk", options: { fontSize: 26 } }
  ], { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: 6.85, y: 2.6, w: 5.65, h: 1.8, fill: { color: C.background2 }, line: { type: "none" }, color: C.text1, align: "center", valign: "middle", margin: 8, objectName: "Remove" });
  s.addText("What happens to the close calls?", { x: 0.8, y: 4.75, w: 11.7, h: 0.8, fontSize: 36, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "Question" });
  takeaway(s, "Legal incentives shape moderation.", 5.95);
  s.addNotes(argNotes({
    who: "P4 · CONSEQUENCES",
    objective: "Show the asymmetric incentive. Not 'everything gets censored', but 'the close calls go to delete'.",
    theirs: "\"Voluntary moderation comes and goes. Meta dropped its US fact-checking in 2025. Without a legal consequence, safety lasts until the next strategy change.\"",
    ours: "\"Platforms do have incentives today: advertisers, users, regulators. The question is what liability adds. Put yourself in the platform's legal team. A disputed post is a risk if it stays up and no risk if it comes down. So the close calls go one way. Meta itself estimated that one or two in every ten of its removals may already be mistakes, without any lawsuit pressure. Smaller sites often can't carry the risk at all. We're not saying everything gets censored. We're saying the incentive points at deleting, not at getting it right.\"",
    example: "When Australia made page owners responsible for readers' comments, CNN switched off its Facebook pages there rather than carry the risk.",
    counter: "\"Add a good-faith safe harbour so honest mistakes aren't punished.\"",
    response: "\"Then you've designed a process rule, not liability for misinformation. Tell us the process. That's a much narrower debate.\"",
    question: "\"Under your rule, does taking down a true post cost the platform anything?\"\n  If yes: \"Then they're sued both ways on every disputed post. Only the biggest can live with that.\"\n  If no: \"Then every close call goes to deletion.\"",
    evidence: "1. Meta's own estimate (January 2025): one to two in every ten removals may have been mistakes.\n2. CNN restricted its Facebook pages for Australian users after the 2021 ruling.\nBoth are patterns, not proof about a misinformation-liability law. Say so if challenged.",
    also: "\"They already moderate\": \"Moderating under your own rules isn't moderating under a lawsuit.\"\n\"AI can catch it\": \"AI copies past labels. New disputed claims are exactly what it gets wrong.\"",
    handoff: "\"So is there a better way to go after the harm? [P5].\""
  }));
}

// 7 · P5 Alternative
{
  const s = pres.addSlide({ masterName: "OUR_CASE_ARG", sectionTitle: "Our case" });
  progress(s, 4);
  s.addText("IS BROAD LIABILITY THE BEST REMEDY?", { placeholder: "title" });
  const tags = ["Speaker", "Fraud", "Scam ads", "Platform design", "Knowing participation", "Court orders"];
  tags.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    card(s, t, 0.8 + col * 3.98, 2.55 + row * 1.05, 3.75, 0.85, { size: 24, fill: C.background1, line: C.accent1, color: C.accent1, name: "Tool " + (i + 1) });
  });
  s.addText("Target the specific wrong.", { x: 0.8, y: 4.85, w: 11.7, h: 0.8, fontSize: 36, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "Principle" });
  takeaway(s, "Accountability does not require one universal rule for misinformation.", 5.95);
  s.addNotes(argNotes({
    who: "P5 · ALTERNATIVE",
    objective: "Show that targeted legal tools exist, without sounding anti-regulation or committing us to design a regime. Deliver the weighing.",
    theirs: "\"Real people get hurt, and anonymous users can't be sued. If the platform isn't accountable, nobody is.\"",
    ours: "\"Nobody here is saying 'do nothing'. The person who lied can be sued, and people have been, for very large amounts. Fraud, and scam ads a platform knowingly sells, are wrongs the law can already reach. Platforms can be held liable for harmful design or for knowingly taking part. Courts can order specific content down. And if more regulation is needed, process-based duties for the biggest platforms are a more targeted alternative than liability for whether every user's statement is true. Accountability works best when it's attached to a defined wrong.\"",
    example: "Even Europe, often held up as the strict model, doesn't make a host liable just because lawful content turns out to be false. It makes platforms act on illegal content and requires the biggest ones to manage risks in their systems.",
    counter: "\"Those tools are slow. Court orders arrive after the damage is done.\"",
    response: "\"Fast and wrong isn't better. Speed is exactly where mistakes happen, and a vague rule makes the fast decision 'delete'.\"",
    question: "\"Should the same rule apply to a giant social network and a 2,000-member forum run by one volunteer?\"\n  If yes: \"The forum closes or bans topics, and it has no algorithm.\"\n  If no: \"Then the trigger isn't the false post. What is it?\"\n  If 'scaled duties': \"Fair. Then what duty, and how is it met without deciding what's true?\"",
    evidence: "1. Fox's $787.5M settlement with Dominion (2023): speakers face consequences for their own falsehoods.\n2. EU Digital Services Act: hosts act on illegal content once they know; the biggest platforms must assess systemic risks.",
    also: "\"Europe does it\": \"Even Europe doesn't make a host liable just because lawful content is false.\"\nWEAK SPOT: don't claim process rules are proven to work better. Say they are more targeted.",
    handoff: "\"Which leaves five questions their case has to answer.\" (advance to The Test)"
  }));
}

// 8 · The Test
{
  const s = pres.addSlide({ masterName: "OUR_CASE", sectionTitle: "Our case" });
  card(s, "FALSE USER POST", 0.8, 1.05, 2.1, 0.75, { size: 14, margin: 2, fill: C.background1, line: C.accent2, color: C.accent2, name: "Start" });
  const links = ["1 TRIGGER", "2 TRUTH", "3 CONDUCT", "4 CONSEQUENCES", "5 ALTERNATIVE"];
  links.forEach((t, i) => {
    const x = 0.8 + 2.1 + 0.22 + i * (1.7 + 0.22);
    arrow(s, x - 0.22, 1.05, 0.22, 0.75);
    card(s, t, x, 1.05, 1.7, 0.75, { size: 13, margin: 2, fill: C.accent1, color: C.background1, name: "Link " + (i + 1) });
  });
  s.addText("Before making the platform legally responsible, these five questions need answers.", { x: 0.8, y: 2.05, w: 11.7, h: 0.5, fontSize: 20, color: C.accent3, margin: 0, isTextBox: true, objectName: "Test line" });
  s.addText("HOLD PLATFORMS ACCOUNTABLE\nFOR WHAT THEY DO,\nNOT FOR EVERY FALSE THING\nTHEIR USERS SAY.", { x: 0.8, y: 2.9, w: 11.7, h: 3.6, fontSize: 48, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true, lineSpacingMultiple: 0.95, objectName: "Closing" });
  navLinks(s, [["Argument menu ›", N.menu]]);
  s.addNotes([
    "SPEAKER: Closer (per the confirmed speaking order)",
    "OBJECTIVE: Make the conclusion feel inevitable. Mirror the opening.",
    "",
    "WHAT GROUP 5 PROVED\nMisinformation can cause harm. We agreed in our first sentence.",
    "",
    "WHAT GROUP 5 NEEDED TO PROVE\nWhen and why another person's false statement should create legal liability for the platform.",
    "",
    "WALK THE CHAIN (one line each)\nTrigger: we still don't know what makes the platform liable.\nTruth: we still don't know who decides what's false, or how fast.\nConduct: every real wrong they named was the platform's own design or statements, and we accept liability there.\nConsequences: their rule makes removing true posts free and leaving disputed ones costly.\nAlternative: narrower tools target what platforms actually control.",
    "",
    "30-SECOND EMERGENCY CLOSE\n\"Everyone here wants less misinformation. Group 5 showed it can cause harm, and we agreed with that from the start. What they needed to show was why another person's false statement should make the platform legally liable. A rule like that needs someone to decide what's true in minutes, and it rewards deleting over getting it right. Hold platforms to account for what they do. That's why we oppose the motion.\"",
    "",
    "REBUTTAL: click 'Argument menu' (bottom-right) or type 9 then Enter."
  ].join("\n"));
}

/* ================= SECTION: LIVE REBUTTAL ================= */
pres.addSection({ title: "Live rebuttal" });

// 9 · Menu
{
  const s = pres.addSlide({ masterName: "REBUTTAL_MENU", sectionTitle: "Live rebuttal" });
  s.hidden = true;
  s.addText("WHAT'S THEIR ARGUMENT?", { x: 0.8, y: 0.85, w: 11.7, h: 0.9, fontSize: 44, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "Menu title" });
  const cols = [
    ["P1 · TRIGGER", [["DUTY OF\nCARE", N.duty], ["PUBLISHERS", N.publishers]]],
    ["P2 · TRUTH", [["THEY\nKNEW", N.knew], ["CLEARLY\nFALSE", N.clearly]]],
    ["P3 · CONDUCT", [["ALGORITHMS", N.algorithms], ["PROFIT", N.profit]]],
    ["P4 · CONSEQUENCES", [["NO\nINCENTIVE", N.incentive], ["ALREADY\nMODERATE / AI", N.moderate]]],
    ["P5 · ALTERNATIVE", [["HARM &\nVICTIMS", N.harm], ["LAW IS\nCHANGING", N.law]]]
  ];
  cols.forEach(([head, tiles], i) => {
    const x = 0.8 + i * (2.22 + 0.15);
    s.addText(head, { x, y: 2.0, w: 2.22, h: 0.4, fontSize: 13, bold: true, color: C.accent1, charSpacing: 1, align: "center", margin: 0, isTextBox: true, objectName: "Owner " + (i + 1) });
    tiles.forEach(([t, n], j) => {
      card(s, t, x, 2.5 + j * 1.95, 2.22, 1.75, { size: t.includes("MODERATE") ? 18 : 22, fill: C.background1, line: C.accent1, lineW: 2, link: n, tip: t.replace("\n", " "), name: "Tile " + t.replace("\n", " ").replace("&", "and") });
    });
  });
  navLinks(s, [["Our case", N.position], ["The test", N.test], ["Backdrop", N.backdrop]]);
  s.addNotes([
    "LIVE REBUTTAL MENU (hidden slide; reach it from 'Argument menu' on slide 8, or type 9 then Enter).",
    "Workflow: they say something → recognise it → click the tile → owner responds → click ← Menu.",
    "",
    MUST_BEAT,
    "",
    "FAST ROUTING\nDuty, notice, 'reasonable steps', negligence, newspapers/publishers → P1\nKnowledge, experts, fact-checkers, 'it's obviously false', free speech → P2\nAlgorithms, design, profit, scam ads → P3\nIncentives, 'they already moderate', AI → P4\nHarm, victims, Europe, Section 230 reform, court verdicts → P5"
  ].join("\n"));
}

// 10–19 · Rebuttal slides
const REB = [
  { key: "duty", cat: "DUTY OF CARE", owner: "P1",
    claim: "Platforms should take reasonable steps once they know.",
    head: "REASONABLE STEPS TOWARD WHAT?",
    lines: [["Remove the post?"], ["Or decide whether it's true?"]],
    ask: "What exactly triggers the legal duty?",
    notes: { owner: "P1 · TRIGGER", steel: "\"We're not asking for automatic liability. Every business owes a duty of care. When a large platform has been told that harmful misinformation is spreading, and it amplifies it anyway, failing to act is negligence. That's how responsibility works everywhere else.\"\n\n" + MUST_BEAT,
      r10: "\"Reasonable steps toward what? Taking it down, or deciding whether it's true? Either way, someone has to judge the post.\"",
      r30: "\"That's a narrower rule, and we're glad to test it. What creates the duty: a report? A report isn't proof, so the platform still has to decide if it's right. If the duty is to take it down, true posts go too. If it's to check the truth, the platform becomes the judge of what's true, with a lawsuit if it guesses wrong. A duty about how platforms build their systems is a different thing, and that's not liability for users' speech.\"",
      counter: "\"Only for content that's clearly false and harmful.\"",
      final: "\"Who decides it's clearly false? If a court, we agree. If the company on a complaint, that's the problem.\"",
      question: "\"What exactly triggers the legal duty: the post, the report, or something the platform did?\"",
      evidence: "1. US Supreme Court (1959): bookshops can't be held liable for books they hadn't read.\n2. US courts have rejected liability just because a platform was told about a post.",
      watch: "Don't imply we oppose all duties. Duties about system design, set in advance, are a fair alternative." } },
  { key: "publishers", cat: "PUBLISHERS", owner: "P1",
    claim: "Newspapers are liable. Why not platforms?",
    head: "PUBLISHERS CHOOSE. PLATFORMS HOST.",
    lines: [["An editor picks every piece before it runs."], ["Platforms carry posts no one there has read."]],
    ask: "Should a platform be liable for a post no one there has seen?",
    notes: { owner: "P1 · TRIGGER", steel: "\"A newspaper that prints a defamatory letter can be sued. Platforms reach far more people than any newspaper. Giving them special protection is a double standard. Other industries are liable for harms they facilitate too.\"",
      r10: "\"Publishers choose every piece before it goes out. Platforms host posts nobody at the company has read.\"",
      r30: "\"An editor reads and picks each item, and even newspapers are usually liable only when they're at fault. Platforms carry huge volumes of posts that no one there has seen. Before 1996, treating a site that moderated like a publisher meant the site that tried got sued and the one that didn't look was fine. That's why the law changed. And other industries are liable for what they make, not for what their customers say.\"",
      counter: "\"Algorithms are the editor now.\"",
      final: "\"Then the issue is the algorithm's design. That's conduct, and you can judge it without the platform ruling on each post's truth.\"",
      question: "\"Should a platform be liable for a post no one at the company has seen?\"",
      evidence: "Before Section 230 (1996), a service that moderated was treated as a publisher; one that didn't wasn't. That is why the law was written.",
      watch: "Don't say platforms make no choices. Concede ranking is a choice and route to P3 if they press on algorithms." } },
  { key: "knew", cat: "KNOWLEDGE", owner: "P2",
    claim: "They know misinformation is on their platform.",
    head: "KNOWING IT EXISTS ≠ KNOWING THIS POST IS FALSE.",
    lines: [],
    ask: "What exactly must the platform know before liability begins?",
    notes: { owner: "P2 · TRUTH", steel: "\"Platforms have internal research showing misinformation spreads on their services. They know who the repeat offenders are. They choose engagement over action. Knowledge plus inaction is exactly when the law should step in.\"",
      r10: "\"Knowing misinformation exists somewhere isn't knowing this post is false.\"",
      r30: "\"Every large platform knows some false content exists, just as a phone company knows people lie on calls. That's general awareness, not knowledge that a specific post is false. And if knowing is what makes you liable, the safest legal strategy is to stop looking. That's the opposite of what we want.\"",
      counter: "\"They know who the repeat offenders are.\"",
      final: "\"Then deal with repeat offenders through account rules and transparency. That doesn't need liability for the truth of every post.\"",
      question: "\"What exactly must the platform know: that misinformation exists, or that this particular post is false?\"",
      evidence: "US Supreme Court (2023, unanimous): running a service everyone uses, recommendations included, isn't the same as knowingly helping wrongdoing. (A terrorism case, not Section 230; use as an analogy only.)",
      watch: "Don't say platforms are ignorant or innocent. They know a lot. The point is what kind of knowledge." } },
  { key: "clearly", cat: "CLEARLY FALSE", owner: "P2",
    claim: "Experts and fact-checkers can tell what's false.",
    head: "THE CLEAR CASES ARE ALREADY HANDLED.",
    lines: [["Liability matters for the disputed ones."], ["Someone still has to make that call, fast."]],
    ask: "While the facts are still disputed, who decides?",
    notes: { owner: "P2 · TRUTH", steel: "\"This isn't about opinions. Fake cures, wrong voting dates, invented quotes. Fact-checkers and experts identify these every day. And lies aren't protected speech anyway.\"",
      r10: "\"Agreed, plenty is clearly false, and platforms already remove it. Liability bites on the disputed ones.\"",
      r30: "\"Clearly false content is the easy part, and platforms already take much of it down. A liability rule only changes behaviour in the grey area, where facts are disputed or still emerging. Someone has to make that call in minutes, long before a court does. In 2021 Facebook followed expert guidance and banned claims that COVID came from a lab, then reversed itself about four months later. Under liability, which decision should it have been sued for?\"",
      counter: "\"Courts decide truth in defamation cases all the time.\"",
      final: "\"One statement about one person, after a trial, usually with fault required. Not a moderator deciding today.\"",
      question: "\"While the facts are still disputed, who decides, and what happens if they're wrong?\"",
      evidence: "Facebook's 2021 ban on COVID-origin claims, reversed about four months later.\nOn free speech: the US Supreme Court has said a statement isn't automatically unprotected just because it's false (fraud and defamation still aren't protected).",
      watch: "Never say truth is subjective. Concede that many falsehoods are clear-cut." } },
  { key: "algorithms", cat: "ALGORITHMS", owner: "P3",
    claim: "Platforms actively amplify misinformation.",
    head: "THEN FOCUS ON THE AMPLIFICATION.",
    lines: [["Ranking and recommendation are platform conduct."], ["A user's false statement is still the user's statement."]],
    ask: "Is your liability based on the false post, or the platform's conduct?",
    notes: { owner: "P3 · CONDUCT", steel: "\"Platforms aren't bulletin boards. Their recommendation systems choose what millions see, and they push sensational falsehoods because it keeps people engaged. That design choice makes them active participants, and courts have started to agree.\"",
      r10: "\"That actually narrows the issue. If amplification is the problem, regulate amplification, not every false post.\"",
      r30: "\"We agree ranking is a choice, and platforms should answer for their own choices. Juries this year found against platforms over addictive design. But if amplification is what creates responsibility, simply hosting can't be enough. So the right target is the recommendation system: how it's designed and tested. That still doesn't make the platform liable because a user's underlying post is false.\"",
      counter: "\"A US appeals court has said the algorithm is the platform's own speech, so it can be liable.\"",
      final: "\"That case was about an app pushing a dangerous challenge to a child. That's conduct, and we agree it can carry liability. It isn't a rule about users' false posts.\"",
      question: "\"If a site just shows posts in date order, with no recommending, should it be liable for a user's false post?\"",
      evidence: "1. March 2026 jury verdicts (design, failure to warn): jury decisions under appeal, not precedent.\n2. MIT study (2018): people, not bots, mainly spread false stories.",
      watch: "Concede ranking is a choice. Don't lead with free-speech law, and don't claim algorithms don't matter." } },
  { key: "profit", cat: "PROFIT", owner: "P3",
    claim: "Platforms profit from engagement, including misinformation.",
    head: "THEY PROFIT FROM TRUE POSTS TOO.",
    lines: [["Profit shows who can afford rules,"], ["not who made the false statement."]],
    ask: "If the platform earned nothing from a false post, would that change who's responsible?",
    notes: { owner: "P3 · CONDUCT", steel: "\"Platforms earn money from attention, and false, outrageous content attracts attention. They sell ads against it and even pay creators who spread it. If you profit from the harm, you should share the cost.\"",
      r10: "\"They profit from true posts too. Profit tells us who can afford rules, not which posts are false.\"",
      r30: "\"The business model matters, and we're not defending it. But profit is earned on true and false posts alike. If the concern is how platforms make money, look at what they do: the ads they sell, the creators they pay, the scams they knowingly carry. That's the platform's own conduct, and the law can reach it. It still doesn't make the platform liable because a user said something false.\"",
      counter: "\"Banks profit from transactions and they're liable for fraud.\"",
      final: "\"Banks are liable for fraud the law defines in advance. Nobody asks a bank to decide whether a customer's claim is true.\"",
      question: "\"If a platform made no money from a false post, would it stop being responsible for it?\"",
      evidence: "Scam ads a platform knowingly sells are its own commercial conduct, a defined wrong.",
      watch: "Don't defend engagement-driven design. Concede the incentive problem; contest the remedy." } },
  { key: "incentive", cat: "INCENTIVES", owner: "P4",
    claim: "Without liability, platforms won't act.",
    head: "LIABILITY CREATES AN INCENTIVE. BUT WHICH ONE?",
    lines: [["LEAVE IT UP  →  legal risk", true], ["REMOVE IT  →  lower legal risk", true]],
    ask: "What happens to the close calls?",
    notes: { owner: "P4 · CONSEQUENCES", steel: "\"Voluntary moderation comes and goes. Meta ended its US fact-checking programme in 2025. Without legal consequences, user safety lasts only until the next strategy change.\"",
      r10: "\"Liability does create an incentive: to delete anything disputed, not to get it right.\"",
      r30: "\"Platforms already respond to advertisers, users and regulators. What liability adds is lopsided risk: a disputed post is dangerous to leave up and free to take down. So the close calls go to delete. Meta itself estimated one or two in every ten removals may already be mistakes, with no lawsuit pressure. We agree voluntary steps can be reversed. If regulation is needed, process-based duties are a more targeted answer than liability for whether users' statements are true.\"",
      counter: "\"Over-removal of misinformation is a price worth paying.\"",
      final: "\"The mistakes don't only hit false posts. They hit true ones and questions that are still open.\"",
      question: "\"Under your rule, which mistake costs the platform money: leaving a false post up, or taking a true one down?\"",
      evidence: "Meta's own estimate (January 2025): one to two in every ten removals in December 2024 may have been mistakes. A company estimate under its own policies, not a liability regime.",
      watch: "Don't claim 'everything will be censored', and don't claim process duties are proven to work. Acknowledge the fact-checking reversal openly." } },
  { key: "moderate", cat: "MODERATION", owner: "P4",
    claim: "They already moderate, and AI can do it at scale.",
    head: "MODERATING BY CHOICE ≠ MODERATING UNDER THREAT OF A LAWSUIT.",
    lines: [["Under liability, close calls go to \"delete\"."]],
    ask: "Under your rule, what does it cost to remove a true post?",
    notes: { owner: "P4 · CONSEQUENCES", steel: "\"Platforms already remove millions of posts every day, and AI keeps getting better at spotting falsehoods. So liability isn't asking for anything impossible, just for them to do properly what they already do.\"",
      r10: "\"Moderating under your own rules is different from moderating with a lawsuit over you. Close calls go to delete.\"",
      r30: "\"Today a platform can make a judgement call and fix it if it's wrong. Under liability, every close call becomes a legal risk if it stays up, so it comes down. AI doesn't solve that: it learns from what people labelled false before, and new, disputed claims are exactly where it struggles. Better tools are welcome. They don't change who has to decide disputed truth, or which way the incentive pushes.\"",
      counter: "\"Add a good-faith safe harbour so honest mistakes aren't punished.\"",
      final: "\"Then you've designed a process rule, not liability for misinformation. Tell us the process. That's a much narrower debate.\"",
      question: "\"Under your rule, does removing a true post cost the platform anything?\"",
      evidence: "After Australia made page owners responsible for readers' comments (2021), CNN restricted its Facebook pages there rather than carry the risk.",
      watch: "Present over-removal as a pattern, not proof: no study of a misinformation-liability law exists here." } },
  { key: "harm", cat: "HARM & VICTIMS", owner: "P5",
    claim: "Misinformation causes real-world harm.",
    head: "WE AGREE.",
    lines: [["But harm proves there is a problem."], ["It does not prove ", false, "who should be legally liable."]],
    ask: "What makes the platform legally responsible for another person's statement?",
    notes: { owner: "P5 · ALTERNATIVE", steel: "\"People have died from fake cures. Election lies have undermined trust and sparked violence. Victims are real, and anonymous users can't be sued. If platforms aren't legally accountable, nobody is.\"",
      r10: "\"We agree the harm is real. That still doesn't tell us who should be legally liable.\"",
      r30: "\"Nobody here disputes the harm; we said so first. But accountability already exists where it fits. The person who lied can be sued, and people have been, for very large amounts. Platforms can be held liable for their own conduct, like harmful design or scams they knowingly carry. Courts can order specific content down. If there's a gap, it's about finding and recovering from speakers, so fix that gap directly, rather than making every platform liable for disputed truth.\"",
      counter: "\"Unmasking anonymous users is slow, and they often can't pay.\"",
      final: "\"Then the gap is identifying and recovering from the speaker. Fix that directly.\"",
      question: "\"Under your rule, who can sue: the person harmed, or anyone who was misled?\"",
      evidence: "Fox's $787.5M settlement with Dominion (2023): speakers face real consequences for their own falsehoods.",
      watch: "Concede the harm first, every time. Never sound dismissive of victims." } },
  { key: "law", cat: "REGULATION", owner: "P5",
    claim: "Europe regulates platforms. Courts are moving.",
    head: "THEY TARGET CONDUCT AND ILLEGAL CONTENT.",
    lines: [["Europe: illegal content and big platforms' systems."], ["Recent verdicts: design and a company's own statements."]],
    ask: "Which of those makes a platform liable just because a user's post was false?",
    notes: { owner: "P5 · ALTERNATIVE", steel: "\"Europe already regulates platforms. US juries found against Meta and YouTube this year. Congress has bipartisan bills to sunset Section 230. The world is moving toward platform accountability, and the US is the outlier.\"",
      r10: "\"They target illegal content and platforms' own conduct, not the falsity of users' posts.\"",
      r30: "\"Look at what those rules actually do. Europe makes hosts act on illegal content once they know about it, and requires the biggest platforms to assess risks in their systems. The verdicts this year were about addictive design and a company's own misleading statements. None of that makes a host liable just because a user's lawful post turns out to be false. That's our line, not theirs.\"",
      counter: "\"Europe's human-rights court allowed a news site to be held liable for readers' comments.\"",
      final: "\"For clearly illegal hate speech and threats. The same court refused liability for merely offensive comments.\"",
      question: "\"Which of those rules makes a platform liable just because a user's post was false?\"",
      evidence: "1. EU Digital Services Act: hosting exemption unless the host knows of illegal content; systemic-risk duties for very large platforms.\n2. March 2026 verdicts: design and Meta's own statements; under appeal.",
      watch: "Europe does use knowledge-based liability for illegal content. Never say it doesn't. Section 230 bills are only introduced, not passed." } }
];

REB.forEach((r) => {
  const s = pres.addSlide({ masterName: "REBUTTAL", sectionTitle: "Live rebuttal" });
  s.hidden = true;
  s.addText("GROUP 5  ·  " + r.cat, { x: 0.8, y: 0.4, w: 8.0, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 2, margin: 0, isTextBox: true, objectName: "Category" });
  s.addText([
    { text: "“", options: { color: C.accent2 } },
    { text: r.claim.toUpperCase(), options: {} },
    { text: "”", options: { color: C.accent2 } }
  ], { x: 0.8, y: 0.95, w: 11.7, h: 1.3, fontSize: 30, bold: true, color: C.accent3, valign: "top", margin: 0, isTextBox: true, objectName: "Their claim" });
  s.addText(r.head, { placeholder: "title" });
  if (r.lines.length) {
    const runs = [];
    r.lines.forEach((ln, i) => {
      const last = i === r.lines.length - 1;
      if (ln.length === 3) {
        runs.push({ text: ln[0], options: {} });
        runs.push({ text: ln[2], options: { bold: true, color: C.accent1, breakLine: !last } });
      } else {
        runs.push({ text: ln[0], options: { bold: !!ln[1], breakLine: !last } });
      }
    });
    s.addText(runs, { x: 0.8, y: 4.0, w: 11.7, h: 1.05, fontSize: 24, color: C.text1, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 2, objectName: "Support" });
  }
  s.addText("ASK", { x: 0.8, y: 5.25, w: 2.0, h: 0.3, fontSize: 12, bold: true, color: C.accent3, charSpacing: 2, margin: 0, isTextBox: true, objectName: "Ask label" });
  s.addText(r.ask, { x: 0.8, y: 5.55, w: 11.7, h: 0.9, fontSize: 24, italic: true, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: "Ask" });
  s.addText("OWNER  ·  " + r.owner, { x: 0.8, y: 6.85, w: 3.0, h: 0.35, fontSize: 13, bold: true, color: C.accent1, charSpacing: 1, valign: "middle", margin: 0, isTextBox: true, objectName: "Owner" });
  navLinks(s, [["← Menu", N.menu], ["Our case", N.position], ["The test", N.test]]);
  s.addNotes(rebNotes(r.notes));
});

// 20 · Backdrop
{
  const s = pres.addSlide({ masterName: "REBUTTAL_MENU", sectionTitle: "Live rebuttal" });
  s.hidden = true;
  s.addText("TRIGGER  ·  TRUTH  ·  CONDUCT  ·  CONSEQUENCES  ·  ALTERNATIVE", { x: 0.8, y: 2.9, w: 11.7, h: 1.2, fontSize: 26, bold: true, color: C.accent1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Backdrop" });
  navLinks(s, [["← Menu", N.menu], ["The test", N.test]]);
  s.addNotes("Rebuttal backdrop (hidden). Leave on screen while a speaker answers without a specific rebuttal slide. Click ← Menu to return.");
}

pres.writeFile({ fileName: OUT }).then(async () => {
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
});
