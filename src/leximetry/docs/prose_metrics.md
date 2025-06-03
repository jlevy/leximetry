# Abstract Quality Metrics for Prose

## Purpose

This document describes a simple set of high-level metrics for assessing the quality of
prose.

## Background

"Good writing" is often considered highly subjective or a matter of taste.
However, there are many attributes of prose that can be assessed fairly objectively.
For spelling, formatting, grammar, and style, we have traditionally turned to books like
Strunk and White or the *Chicago Manual of Style*.

More abstract attributes of writing such as coherence, factuality, subjectivity, or
rigor, are critical to quality writing but harder to quantify.
Readers do tend to recognize these attributes when they see them either directly or
quite often infer them from the source (as a well-known magazine or a known publisher or
a blurb for a book) or the appearance (such as a book that seems designed or printed
well). In established publications or journals, processes for fact checking and review
processes are what help ensure certain levels of quality.

LLMs do not replace any of this.
However, they do make systematic measurement of many attributes of text easier, to a
degree that things that used to be considered subjective may now by assessed via
consistent process across many documents, which makes comparisons along these dimensions
easier, more consistent, and potentially very useful.
Increasingly, measurements of quality are necessary, both to instruct LLMs to improve
their writing and to help us filter out content we don't wish to read.

While scores are inherently reductive, there is a strong need for ways for readers to
rapidly asses content and whether to trust it.
If we find a way to make relatively consistent measurement and summarize them in concise
and even visual ways, it could go a long ways toward helping us decide what content to
consume.

## The Leximetry Abstract Quality Metrics

The metrics here are an attempt at building a list and rubric of several mostly
independent, abstract characteristics of prose that are easy to assess on a 1-to-5 scale
by a human or an LLM.

It can apply to fiction and nonfiction, traditional or social media, or any text of a
meaningful length. The selection of these attributes is subjective.
But the evaluation of each one on a given piece of text should be mostly something
careful readers (and LLMs) would agree on.

These are intended to be used as qualitative attributes rather than scores.
For some attributes, higher scores are better, this isn't the case for all of them, and
the "right" quality metrics for a given context vary greatly.

However, it should be possible to use these qualitative scores for comparison and
categorization, such as to compare the rigor of a blog post with the writing in a book,
or compare the output of an LLM with something written by a human on the same subject.

## List of Metrics

There are currently just **12 metrics** broken into **four categories**: *style*,
*groundedness*, *expression*, and *impact*.

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

4. **Narrativity:** Is the material organized more by topic or with a narrative arc in
   mind? Note this does not relate to whether the facts are subjective.
   It applies to both fiction and non-fiction.

5. **Subjectivity:** Are the statements or opinions inherently tied to individual
   experience or fictional people or concepts rather than facts?

6. **Warmth:** What is the emotional disposition of the writer to the reader, the
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

9. **Thoroughness:** To what degree does the work include all relevant information that
   is within scope? Note something can be narrow but still thorough, like a research
   paper.

### Impact

How are readers likely to engage with the material?

10. **Accessibility:** How accessible is the content to readers with varying levels of
    background knowledge and training?

11. **Longevity:** How likely would it be for a reader to find this interesting in a
    week, a month, a year, or a decade in the future?

12. **Sensitivity:** To what degree is the content sensitive, potentially causing
    offense or posing safety/security risks?

## FAQ

### But Aren't These Subjective?

Yes, certainly to some degree.
But they seem to be at a level of granularity a modern LLM could assess them fairly
consistently and a human would find it reasonable most of the time.
They aren't perfect, but they might be useful.

### Why These Metrics?

Because they seem like the highest-level attributes of text that can reasonably be
assessed somewhat consistently.
I may have missed some and invite suggestions!
There are several attributes of text that I deliberately did not included:

- Dimensions that are inherently difficult to assess.
  For example, "creativity" or "originality" are certainly attributes of writing, but it
  human assessments are highly variable and it's almost impossible to say whether the
  creativity comes from the writer or is simply being copied (especially by an LLM).

- Dimensions that reflect how a work relates to a specific audience, like
  appropriateness for a given audience.

- Dimensions that change over time, like "notability."

- Dimensions that tend to be assessed quite differently by different people, like
  "offensiveness," "controversiality," or "bias."
  Having them within the middle of the "harmlessness" metric seems like a reasonable
  compromise that will tend to produce consistent assessments.
  It's worth marking offensive content but clearly distinguishing it from things that
  may lead to physical harm.
  We may not agree on how offensive something is, but we can agree how likely some
  people will find it offensive.

- Dimensions that would largely be used to filter content and better handled by
  dedicated classifiers, like fraudulent content or spam.

## Scoring Instructions

To evaluate a piece of text, you will be given

- the text in its entirety

- possibly additional background on the source

- possibly content or web pages drawn from the links, citations, or key concepts in the
  text

- the metric you will evaluate, chosen from the table above (such as "Clarity" or
  "Factuality"), as well as a list of examples of what each score means for that metric

Then given the content you have, your job is to assign the best score.

It must be **0**, **1**, **2**, **3**, **4**, or **5**.

Guidelines:

- Pick the score that best matches.

- If you can tell it is one of two adjacent values pick the smaller value.
  (Example: If the rigor of the text seems like a **2** or a **3**, pick **2**.)

- If a metric is squarely between the endpoints as described, or a mix that is unclear,
  it typically should be a **3**.

- If there simply isn't enough information to assess that metric, such as a very brief
  or seemingly missing text, assign it a **0**.

For output, provide a result in the form "SCORE (REASON)":

- The score as a single digit (0-5).

- A brief parenthetical note with one or two sentences mentioning the reason for the
  score.

An example of output for Clarity might be:
```
5 (Well written. No language errors.)
```

An example of output for Factuality might be:
```
3 (Contains speculations about the authors cat as well as factual content on C++ programming.)
```

An example of output for Narrativity might be:
```
1 (Technical paper with clear structure.)
```

An example of the output for Sensitivity might be:
```
4 (Contains numerous obscenities.)
```

### Scoring Rubric

- **Metric:** Clarity

  - **Description:** Is the language readable and clear, with good command of language
    and correct spelling and grammar?

  - **Value 0:** Cannot assess.
    Content missing. Only use this if no content is present.

  - **Value 1:** Contains numerous spelling and punctuation errors and sentences with
    grammatical errors or that are hard to follow.
    Use this for single-word or fragmentary content.

  - **Value 2:** Contains errors but is clear and understandable language.

  - **Value 3:** Typical business email quality with few errors in spelling,
    punctuation, or grammar and may contain a few typos, lack capitalization, etc.

  - **Value 4:** Clear, correct language but with flaws in language use, such as trite
    phrases or gratuitous big words, or uses good language but is particularly lengthy
    or dense like some fiction.

  - **Value 5:** Perfect grammar and no typos if short, or written with true clarity if
    long, suitable for publication without changes in high editorial standard
    publications like the Wall Street Journal or Oxford University Press.

- **Metric:** Coherence

  - **Description:** How well can the reader follow the progression of ideas and across
    the whole work? This metric reflects only the way something is written and does not
    include logical coherence or rigor, covered below.

  - **Value 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Value 1:** Incoherent with no clear topic or argument.

  - **Value 2:** Weak coherence or an incomplete draft.

  - **Value 3:** Adequate and generally possible to follow.

  - **Value 4:** Strong coherence but has clear gaps or areas where structure or
    narrative could be improved.

  - **Value 5:** Seamless, with each sentence, paragraph, and section necessary and the
    whole organized to achieve its purpose.

- **Metric:** Sincerity

  - **Description:** To what degree do the writer or writers seem to mean what they say?
    This can't always be assessed, in which case the value is a 3.

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Trolling or clickbait where nothing said is actually meant.

  - **Value 2:** Confusing content or statements where the intent is completely unclear
    or deliberately ambiguous.

  - **Value 3:** Promotional or marketing content or content with unclear intent.

  - **Value 4:** Sincerely written content but with an intent to persuade.

  - **Value 5:** Genuine attempt at conveying sentiments if personal, presenting
    information if non-fiction, or expressing artistic intent for fiction.

- **Metric:** Narrativity

  - **Description:** Is the material organized more by topic or with a narrative arc in
    mind? Note this does not relate to whether the facts are subjective.
    It applies to both fiction and non-fiction.

  - **Value 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Value 1:** Pure nonfiction organized by topic with clear scope and very little or
    no personal stories or narrative transitions between topics.

  - **Value 2:** Mostly informative or factual content without narrative, but some
    elements of narrative like a technical book with a few personal stories.

  - **Value 3:** Mix of narrative and facts, like a travel blog post or recipe blog that
    is both a practical guide and includes personal anecdote.

  - **Value 4:** Narrative presentation but the purpose is not narrative, such as a
    best-selling non-fiction book filled with stories and anecdotes.

  - **Value 5:** Personal experience, autobiography, or fictional story where the
    purpose of the writing is narrative.

- **Metric:** Subjectivity

  - **Description:** Are the statements or opinions inherently tied to individual
    experience or fictional people or concepts rather than facts?

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Everything stated is objectively true or false.

  - **Value 2:** Things stated are mostly objective but may include some personal
    opinions or interpretations.

  - **Value 3:** A mix of events and a person's feelings about them.

  - **Value 4:** Personal narrative where much is subjective but includes facts, such as
    childhood recollections.

  - **Value 5:** Everything stated is personal or inner experience.

- **Metric:** Warmth

  - **Description:** What is the emotional disposition of the writer to the reader, the
    material, or the people mentioned?

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Cold or negative toward reader or subject matter.

  - **Value 2:** Some neutral content but includes expressions of negativity or
    coldness.

  - **Value 3:** Completely neutral or an even mix of positive and negative emotions.

  - **Value 4:** Neutral tone but with occasional warmth or positive emotion from the
    writer.

  - **Value 5:** Strong positive emotions expressed toward reader or subject matter.

- **Metric:** Factuality

  - **Description:** Are the statements included verifiably true?

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Pure fiction.

  - **Value 2:** Content where a reasonable person would have doubts, such as fringe
    theories or casual speculation by non-experts, or comments made without regard for
    truth like jokes or trolling that might be true or false, or content from sources
    known to be frequently inaccurate.

  - **Value 3:** A mix of true statements and things where it is unclear if they are
    true or false, including assertions with no citation that cannot be confirmed or
    refuted by sources.

  - **Value 4:** Opinion by someone recognized as an expert in the subject or standard
    scientific article in a peer-reviewed publication, or writing with verifiable
    citations, including Wikipedia articles that don't have complete verifiable
    citations.

  - **Value 5:** Proven and consensus facts verified by multiple third-party sources.

- **Metric:** Rigor

  - **Description:** Is content logically organized, with terms and statements well
    defined, reasoning sound, and multiple perspectives or explanations considered?

  - **Value 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Value 1:** Sloppy reasoning and imprecise statements.

  - **Value 2:** Some logical gaps or unclear terms.

  - **Value 3:** Generally logical but could be more precise.

  - **Value 4:** Well-structured with mostly clear reasoning.

  - **Value 5:** Scientifically precise and logical; if objective, assertions have
    multiple citations from credible sources; if subjective, are thoroughly discussed
    from multiple perspectives.

- **Metric:** Thoroughness

  - **Description:** To what degree does the work include all relevant information that
    is within scope?

  - **Value 0:** Cannot assess.
    Content missing or less than 3 sentences long.

  - **Value 1:** Disjointed ideas or a very short text or post where there was no
    intention of covering more than a thought.
    Most single posts on Twitter are like this.

  - **Value 2:** A short post that covers a clear set of ideas but makes no effort to be
    comprehensive. Many threads on Twitter are like this.

  - **Value 3:** Carefully written and not short, but without thorough citations, such
    as a typical long blog post.

  - **Value 4:** A focused but thorough work, such as a long research paper with full
    citations.

  - **Value 5:** Comprehensive and fully researched treatment of the topic.
    Includes significant numbers of citations and terminology defined within the work.

- **Metric:** Accessibility

  - **Description:** How accessible is the content to readers with varying levels of
    background knowledge and training?

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Requires graduate study or researcher-level knowledge to follow.
    Research papers are typically in this category.

  - **Value 2:** Requires undergraduate or professional-level knowledge in the field and
    does not link to background materials or define all terminology.

  - **Value 3:** Requires some background to understand.
    May define terms or link to background materials.

  - **Value 4:** Accessible to educated general audience but requires significant study.
    Defines all terms and cites sources for further reading.

  - **Value 5:** Accessible to readers without specialized training and does not require
    significant time and effort to understand.

- **Metric:** Longevity

  - **Description:** How likely would it be for a reader to find this interesting in a
    week, a month, a year, or a decade in the future?

  - **Value 0:** Cannot assess.
    Content missing or less than 1 sentence long.

  - **Value 1:** Very recent news, most interesting with a day or two, like news or a
    Twitter post about current news.

  - **Value 2:** Interesting for a few days to weeks, like a family Facebook post.

  - **Value 3:** Interesting for months, like a New Yorker article.

  - **Value 4:** Interesting for years, like a typical book.

  - **Value 5:** Likely will be of of interest in decades, like an encyclopedia article
    or a critically acclaimed book.

- **Metric:** Sensitivity

  - **Description:** To what degree is the content sensitive, potentially causing
    offense or posing legal or safety/security risks?

  - **Value 0:** Cannot assess.
    Content missing. Only use this for content that is missing.

  - **Value 1:** Least sensitive: Content that is broadly innocuous, very unlikely to
    cause offense or safety/security concerns.
    Typical of most general fiction or non-fiction.
    Also use 1 for fragmentary or unclear content.

  - **Value 2:** Content expressing opinions that are likely to evoke strong emotions in
    some, but is not inflammatory and poses no clear safety, security, legal risks, or
    significant risks of offense.

  - **Value 3:** Content involving highly inflammatory discussions (e.g., on wars,
    conflicts) or statements on sensitive topics (e.g., race, gender) that could be
    considered biased or offensive by some readers, but does not directly incite harm.
    Harsh or obscene language.

  - **Value 4:** Content that could lead to tangible negative impacts, guides to
    criminal acts, or deliberately deceptive information (e.g., on vaccines, elections).
    Also use this for content that would likely be called "hate speech" or explicit
    sexual content suitable only for adults.

  - **Value 5:** Most sensitive: Content containing information that poses a direct and
    immediate risk to people's safety or security, such as instructions for creating
    weapons, guides to suicide, or direct incitement to violence.
