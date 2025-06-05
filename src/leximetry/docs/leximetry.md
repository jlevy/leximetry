# Leximetry: Qualitative Metrics for Prose

Joshua Levy\
*v0.1.1 (June 2025) – Draft!*

## Scope

This document is a draft of a few general but practical *qualitative metrics* for
assessing prose. The goal is to make traditionally implicit, manual assessments of
written works more reproducible with the use of LLMs.

This short paper gives background, scores, and a rubric.

It is written in a way that it can be used by an LLM or a human.
The [`leximetry`](https://github.com/jlevy/leximetry) command-line tool uses the metrics
and rubric as defined here.

## Motivation

### What is Quality Writing?

Some attributes of prose are easy to evaluate objectively.
Spelling, formatting, and grammar can be fixed easily and automatically by software.
Writers and editors have long turned to guides like Strunk and White or the *Chicago
Manual of Style* for guidance on clear writing.
And within organizations or publications, style guides are a way to systematize the use
of language and conventions.

Most of the time, readers implicitly sense certain attributes of a work from the text
itself as well as from context, like the source (such as recognizing a well-known
magazine or a known publisher or a blurb on a book cover) or the appearance of the work
(such as a book that seems designed or printed well, or whether it is on a website with
intrusive ads).

In established publications or journals, quality is often maintained by traditions and
processes like editorial review, fact checking, and copy editing.
Over time, especially for books, we use popularity and reviews as signals of what
writing is high quality.

In short, except for the low-level, enforceable details, we tend to infer the quality of
writing implicitly.

### Can Quality Be Measured?

While we implicitly often recognize quality, measuring it explicitly is elusive.
It's contextual, subjective, and not quantitative.

However, there are *qualitative attributes* of writing, such as clarity, coherence,
factuality, rigor, or warmth, that are both important and much easier to define.

Today, with LLMs, what can be defined precisely can be measured systematically.

LLMs do not eliminate the inherent difficulties and nuances of evaluating text.
However, they *do* make even imprecise measurement *more systematic* and possible in
higher volumes. When an evaluation that previously was considered subjective can be
performed consistently across many documents, it makes comparisons along these
dimensions easier, better defined, and potentially useful in new ways.

### Measurements are Imperfect but Useful

Scores are inherently reductive.
But this brevity has value for readers to assess the nature of content rapidly,
especially online. Measurements of quality are increasingly necessary to help us filter
out content we don't wish to read.
These measurements can also be used to assist LLM-based tools in producing better
output.

My hope is that if we find ways to reveal metrics or visualizations of metrics like this
online or in apps, it would spend our reading time more wisely—and perhaps help us find
common ground in the fractured and confusing world of online content.

## The General Quality Metrics

### Scope of Metrics

The metrics below are chosen to be independent, abstract characteristics of prose that
are easy to assess on a 1-to-5 scale when given clear instructions and a rubric.

Such an evaluation can be done by a human or an LLM.

These metrics can apply to fiction and nonfiction, traditional or social media, or any
intelligible prose of a meaningful length.

### Choice of Attributes

The selection of which attributes to measure isn't obvious and the choices here are my
own.

But even though the selection of metrics is subjective, the evaluation of them is much
more objective.

If done correctly, the evaluation of a given piece of text by both humans and LLMs
should be reasonably consistent.
For example, a well-written blog post by a competent writer would typically score **4**
(out of 5) for clarity.
Most good Wikipedia articles should score **5** for factuality.

### These Metrics are Descriptive, Not Prescriptive

The individual metrics are not themselves measurements of quality.
They are simply descriptive attributes.

For some metrics, higher scores are "better" but in general, *larger numbers are not
always better*. The "right" metrics for a given situation depend on the context.

For this reason, there is no single aggregated scores.

Rather than qualitative scores for comparison and categorization, such as to compare the
rigor of a blog post with the writing in a book, or compare the output of an LLM with
something written by a human on the same subject.

## List of Metrics

There are currently **12 metrics** broken into **four categories**: *expression*,
*style*, *groundedness*, and *impact*.

### Expression

Is language used effectively?
This category covers how well the writer expresses themselves.
It does not address style.

1. **Clarity:** Is the language readable and clear, with good command of language and
   correct spelling and grammar?
   This attribute includes errors covered by spell checkers, and tools like Google Docs,
   Grammarly and Vale. It also covers the parts traditional style guides like AP or CMS
   that cover the use of language.
   Note the upper end of this spectrum includes conciseness.

2. **Coherence:** How well can the reader follow the progression of ideas and across the
   whole work? This metric reflects only the way something is written and does not
   include logical coherence or rigor, covered below.

3. **Sincerity:** To what degree do the writer or writers seem to mean what they say?
   This can't always be assessed, in which case the value is a **3**. This reflects
   *apparent* sincerity and does not cover factuality, which is part of groundedness.

### Style

What style, format, and tone is used?
This covers the content and tone.

1. **Subjectivity:** Are the statements or opinions fiction or inherently tied to
   individual experience?
   Or are they closer to objective facts?

2. **Narrativity:** Is the material organized more by topic or with a narrative arc in
   mind? Note this does not relate to whether the facts are subjective.
   It applies to both fiction and non-fiction.

3. **Warmth:** What is the emotional disposition of the writer to the reader, the
   material, or the people mentioned?

### Groundedness

Is the content grounded in reality?
This category covers the use of facts and sound reasoning in the content.

7. **Factuality:** Are the statements included verifiably true?
   Not everything can be assessed perfectly for truth, of course, but this should be
   done to a reasonable depth, i.e. an assessment based on simple online fact checking
   and review of the expertise of the writer and citations.

8. **Rigor:** Is content logically organized, with terms and statements well defined,
   reasoning sound, and multiple perspectives or explanations considered?
   Note this is distinct from subjectivity; it's certainly possible for subjective
   topics to be discussed with some rigor.

9. **Depth:** To what degree does the work include all relevant information that is
   within scope? Note something can be narrow but still thorough, like a research paper.

### Impact

How are readers likely to engage with the material?

10. **Sensitivity:** To what degree is the content sensitive, potentially causing
    offense or posing safety/security risks?

11. **Accessibility:** How accessible is the content to readers with varying levels of
    background knowledge and training?

12. **Longevity:** How likely would it be for a reader to find this interesting in a
    week, a month, a year, or a decade in the future?

## FAQ

### Are these metrics too subjective?

Characteristics like "narrativity" are not formal or precise definitions.
But they are less subjective than very general assessments like whether something is "a
great article" or creative, which potentially makes them more useful

They aim to be at a level of granularity that they are general but a modern LLM could
assess them fairly consistently—and a human would find reasonable most of the time.
They aren't perfectly precise (which is why we only use a 1-to-5 score), but they may be
useful.

### Why these metrics and not others?

Because they seem to be the most important general attributes of text that can
reasonably be assessed somewhat consistently.
The rough criteria are:

- **Descriptive:** The attribute must be descriptive of the text only, not of other
  things, like the the reader.
  It should not be prescriptive or subjective.

- **Quantifiable:** It should make sense as 1-to-5 score.
  This is for consistency in reporting and since simple scores are easier to get
  consensus on.

- **Measurable:** It should be possible to ask a person or an LLM to assess the text and
  expect *mostly* consistent results at the precision of a 1-to-5 score.
  This makes the measurement repeatable and inexpensive.

- **Fixed:** Doesn't change over time.
  A score assigned today to be the same in a year on the same document.

- **Discriminative:** The attribute helps decide the nature of a piece of writing in a
  useful way.

None of these are perfectly achievable goals for a measurement.
For example, a work that is factual today might become non-factual in a year, depending
on external events. But they are generally still good goals.

This does lead to excluding some attributes:

- "Appropriateness" relates to a specific audience so is not descriptive.

- "Creativity" or "originality" are not measurable.
  It's almost impossible to say whether the creativity comes from the writer or is
  simply being copied (especially by an LLM).

- "Notability" is not fixed.
  A post that is notable today is not notable in a year.

- "Offensiveness" and "bias" are hard to measure since opinions can be so variable.
  Instead we use "sensitivity" to capture presence of potentially offensive content.
  Opinions on what is offensive differ, but we often can agree that a significant number
  of people will find specific content offensive.

There are a few other attributes I've considered and might make sense to add to the
list:

- *Facetiousness* could be helpful.
  *Humor* may seem like a good attribute but it's a confusing name for this dimension,
  since it implies perceptions of the reader.
  ("Maybe that's a joke but it's not funny!") Also, although one might think
  facetiousness is the opposite of sincerity, it's actually a distinct dimension.
  For example, something can be facetious and sincere (like a humorous compliment) or
  facetious and insincere (like a trolling comment).

- *Utility* could possibly distinguish artistry or entertainment from practical, useful
  information.

## Scoring Instructions

To evaluate a piece of text, you will be given

- The text in its entirety

- Any additional context, including background on the source and web pages drawn from
  the links, citations, or key concepts in the text

- The metric you will evaluate, chosen from the table above (such as "Clarity" or
  "Factuality") and a description of what it attempts to measure

- The rubric for how to score that metric, with a more detailed description or examples
  for each possible score

Given this information, your job is to assign the best score to the text according to
the rubric and provide:

- A score

- A brief note of one or two sentences with specifics on why you selected the score.

Your answer must for the score must be: **0**, **1**, **2**, **3**, **4**, or **5**.

Guidelines:

- If there simply isn't enough information to assess that metric, such as a very brief
  or seemingly missing text, assign it a **0**.

- Pick the score in in the rubric that most closely describes the text.
  If more than one does, pick the one that seems closest.

- If a metric is squarely between the endpoints of the metric as described, or has a
  wide range or content as a mixture, pick a **3**. There is just one exception to this
  rule: As the rubric describes *sensitivity*, if any portion of a text is sensitive,
  pick the highest score that applies to the most sensitive portion.

For output, provide a result that contains:

- The score as a single digit (0-5).

- A brief parenthetical note with one or two sentences mentioning the reason for the
  score.

Write the result in the format "SCORE (REASON)", i.e. a string matching the regular
expression `[0-5] \(.*?\)`.

An example of output for *clarity* might be:
```
5 (Well written. No language errors.)
```

An example of output for *factuality* might be:
```
3 (Contains speculations about the authors cat as well as factual content on C++ programming.)
```

An example of output for *narrativity* might be:
```
1 (Technical paper with clear structure.)
```

An example of the output for Sensitivity might be:
```
4 (Contains numerous obscenities.)
```

### Scoring Rubric

- **Metric:** *Clarity*

  - **Description:** Is the language readable and clear, with good command of language
    and correct spelling and grammar?

  - **Score 0:** Cannot assess.
    Content missing. Only use this if no content is present.

  - **Score 1:** Contains numerous spelling and punctuation errors and sentences with
    grammatical errors or that are hard to follow.
    Use this for single-word or fragmentary content.

  - **Score 2:** Contains errors but is clear and understandable language.

  - **Score 3:** Typical business email quality with few errors in spelling,
    punctuation, or grammar and may contain a few typos, lack capitalization, etc.

  - **Score 4:** Clear, correct language but with flaws in language use, such as trite
    phrases or gratuitous big words, or uses good language but is particularly lengthy
    or dense like some fiction.

  - **Score 5:** Perfect grammar and no typos if short, or written with true clarity if
    long, suitable for publication without changes in high editorial standard
    publications like the Wall Street Journal or Oxford University Press.

- **Metric:** *Coherence*

  - **Description:** How well can the reader follow the progression of ideas and across
    the whole work? This metric reflects only the way something is written and does not
    include logical coherence or rigor, covered below.

  - **Score 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Score 1:** Incoherent with no clear topic or argument.

  - **Score 2:** Weak coherence or an incomplete draft.

  - **Score 3:** Adequate and generally possible to follow.

  - **Score 4:** Strong coherence but has clear gaps or areas where structure or
    narrative could be improved.

  - **Score 5:** Seamless, with each sentence, paragraph, and section necessary and the
    whole organized to achieve its purpose.

- **Metric:** *Sincerity*

  - **Description:** To what degree do the writer or writers seem to mean what they say?
    This can't always be assessed, in which case the value is a 3.

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Trolling or clickbait where nothing said is actually meant.

  - **Score 2:** Confusing content or statements where the intent is completely unclear
    or deliberately ambiguous.

  - **Score 3:** Promotional or marketing content or content with unclear intent.

  - **Score 4:** Sincerely written content but with an intent to persuade.

  - **Score 5:** Genuine attempt at conveying sentiments if personal, presenting
    information if non-fiction, or expressing artistic intent for fiction.

- **Metric:** *Subjectivity*

  - **Description:** Are the statements or opinions inherently tied to individual
    experience or fictional people or concepts rather than facts?

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Everything stated is objectively true or false.

  - **Score 2:** Things stated are mostly objective but may include some personal
    opinions or interpretations.

  - **Score 3:** A mix of events and a person's feelings about them.

  - **Score 4:** Personal narrative where much is subjective but includes facts, such as
    childhood recollections.

  - **Score 5:** Everything stated is personal or inner experience.

- **Metric:** *Narrativity*

  - **Description:** Is the material organized more by topic or with a narrative arc in
    mind? Note this does not relate to whether the facts are subjective.
    It applies to both fiction and non-fiction.

  - **Score 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Score 1:** Pure nonfiction organized by topic with clear scope and very little or
    no personal stories or narrative transitions between topics.

  - **Score 2:** Mostly informative or factual content without narrative, but some
    elements of narrative like a technical book with a few personal stories.

  - **Score 3:** Mix of narrative and facts, like a travel blog post or recipe blog that
    is both a practical guide and includes personal anecdote.

  - **Score 4:** Narrative presentation but the purpose is not narrative, such as a
    best-selling non-fiction book filled with stories and anecdotes.

  - **Score 5:** Personal experience, autobiography, or fictional story where the
    purpose of the writing is narrative.

- **Metric:** *Warmth*

  - **Description:** What is the emotional disposition of the writer to the reader, the
    material, or the people mentioned?

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Cold or negative toward reader or subject matter.

  - **Score 2:** Some neutral content but includes expressions of negativity or
    coldness.

  - **Score 3:** Completely neutral or an even mix of positive and negative emotions.

  - **Score 4:** Neutral tone but with occasional warmth or positive emotion from the
    writer.

  - **Score 5:** Strong positive emotions expressed toward reader or subject matter.

- **Metric:** *Factuality*

  - **Description:** Are the statements included verifiably true?

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Pure fiction.

  - **Score 2:** Content where a reasonable person would have doubts, such as fringe
    theories or casual speculation by non-experts, or comments made without regard for
    truth like jokes or trolling that might be true or false, or content from sources
    known to be frequently inaccurate.

  - **Score 3:** A mix of true statements and things where it is unclear if they are
    true or false, including assertions with no citation that cannot be confirmed or
    refuted by sources.

  - **Score 4:** Opinion by someone recognized as an expert in the subject or standard
    scientific article in a peer-reviewed publication, or writing with verifiable
    citations, including Wikipedia articles that don't have complete verifiable
    citations.

  - **Score 5:** Proven and consensus facts verified by multiple third-party sources.

- **Metric:** *Rigor*

  - **Description:** Is content logically organized, with terms and statements well
    defined, reasoning sound, and multiple perspectives or explanations considered?

  - **Score 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Score 1:** Sloppy reasoning and imprecise statements.

  - **Score 2:** Some logical gaps or unclear terms.

  - **Score 3:** Generally logical but could be more precise.

  - **Score 4:** Well-structured with mostly clear reasoning.

  - **Score 5:** Scientifically precise and logical; if objective, assertions have
    multiple citations from credible sources; if subjective, are thoroughly discussed
    from multiple perspectives.

- **Metric:** *Depth*

  - **Description:** To what degree does the work include all relevant details that are
    generally within scope of the topic or narrative?
    This reflects the level of detail in the work for both non-fiction and fiction.

  - **Score 0:** Cannot assess.
    Content is missing.

  - **Score 1:** Disjointed ideas or a very short text or post where there is largely a
    single thought. A one-sentence post on Twitter would have this score.

  - **Score 2:** A short post that covers a clear set of ideas but makes no effort to be
    comprehensive. Many short blog posts with a few ideas or threads on Twitter are like
    this. Writing of only a few paragraphs but still containing some detail and nuance
    should have this score.

  - **Score 3:** Carefully written and with at least 2 pages of highly dense technical
    material or at least 3-4 pages of typical text.
    It may or may not have citations or footnotes.
    For example, it could be a long blog post.
    For fiction, it should have detail and be several pages, like a short story.

  - **Score 4:** For nonfiction, this means a focused but thorough work, such as a long
    research paper complete with related work, many citations and deep coverage of
    specifics. For fiction, it should have significant detail and be at least 10 pages
    long.

  - **Score 5:** For nonfiction, this means a comprehensive and fully researched
    treatment of the topic.
    Includes a full treatment with great detail, significant numbers of citations and
    key terminology defined within the work.
    For fiction, this is an extensive and detailed creative work, such as a complete and
    internally consistent, well-written novel or fantasy book with many characters.

- **Metric:** *Sensitivity*

  - **Description:** To what degree is the content sensitive, potentially causing
    offense or posing legal or safety/security risks?
    *Important:* Unlike with the other metrics, if *any* portion of a text is sensitive,
    pick the highest score that applies to the most sensitive portion.
    Don't "average out" the score, even if the sensitive content is included with
    non-sensitive content.

  - **Score 0:** Cannot assess.
    Content missing. Only use this for content that is missing.

  - **Score 1:** Least sensitive: Content that is broadly innocuous, very unlikely to
    cause offense or safety/security concerns.
    Typical of most general fiction or non-fiction.
    Also use this score for fragmentary or unclear content.

  - **Score 2:** Content expressing opinions that are likely to evoke strong emotions in
    some, but is not inflammatory and poses no clear safety, security, legal risks, or
    significant risks of offense.

  - **Score 3:** Contains content that contains highly inflammatory discussions (e.g.,
    on wars, conflicts) or statements on sensitive topics (e.g., race, gender) that
    could be considered biased or offensive by some readers, but does not directly
    incite harm. Harsh or obscene language.

  - **Score 4:** Contains content that could lead to tangible negative impacts, guides
    to criminal acts, or deliberately deceptive information (e.g., on vaccines,
    elections). Also use this for content that would likely be called "hate speech" or
    explicit sexual content suitable only for adults.

  - **Score 5:** Most sensitive: Contains content that poses a direct and immediate risk
    to people's safety or security.
    For example, this would include instructions for creating weapons, guides to
    suicide, or direct incitement to violence.

- **Metric:** *Accessibility*

  - **Description:** How accessible is the content to readers with varying levels of
    background knowledge and training?

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Requires graduate study or researcher-level knowledge to follow.
    Research papers are typically in this category.

  - **Score 2:** Requires undergraduate or professional-level knowledge in the field and
    does not link to background materials or define all terminology.

  - **Score 3:** Requires some background to understand.
    May define terms or link to background materials.

  - **Score 4:** Accessible to educated general audience but requires significant study.
    Defines all terms and cites sources for further reading.

  - **Score 5:** Accessible to readers without specialized training and does not require
    significant time and effort to understand.

- **Metric:** *Longevity*

  - **Description:** How likely would it be for a reader to find this interesting in a
    week, a month, a year, or a decade in the future?

  - **Score 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Score 1:** Least longevity: Very recent news, most interesting with a day or two,
    like news or a Twitter post about current news.

  - **Score 2:** Interesting for a few days to weeks, like a family Facebook post.

  - **Score 3:** Interesting for months, like a New Yorker article.

  - **Score 4:** Interesting for years, like a typical book.

  - **Score 5:** Likely will be of of interest in decades, like an encyclopedia article
    or a critically acclaimed book.
