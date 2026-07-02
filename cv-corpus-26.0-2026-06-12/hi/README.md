# *हिंदी* &mdash; Hindi (`hi`)

This datasheet is for cv-corpus-26.0-2026-06-12 of the Mozilla Common Voice *Scripted Speech* dataset for Hindi [हिंदी - `hi`]. The dataset contains 19029 clips representing 26.67 hours of recorded speech (15.6 hours validated) from 480 speakers, recorded from a text corpus of 42,169 sentences.

## Language

### Accents

| Code | Accent | Clips | Speakers |
|---|---|---|---|
| - |  | 2,952 (15.5%) | 41 (8.5%) |

## Demographic information

The dataset includes the following self-declared age and gender distributions. A coverage summary is shown below each table.

### Gender

Self-declared gender information. The table shows clip and speaker counts with percentages. Speakers who did not declare a gender are listed as Unspecified. A dash (-) indicates zero.

| Code | Gender | Clips | Speakers |
|---|---|---|---|
| male_masculine | Male, masculine | 9,515 (50.0%) | 129 (26.9%) |
| female_feminine | Female, feminine | 571 (3.0%) | 21 (4.4%) |
| transgender | Transgender | - | - |
| non-binary | Non-binary | - | - |
| do_not_wish_to_say | Prefer not to say | - | - |
| - | Unspecified | 8,943 (47.0%) | 344 (71.7%) |

*Gender declared: 10,086 of 19,029 clips (53.0%), 136 of 480 speakers (28.3%)*

### Age

Self-declared age information. The table shows clip and speaker counts with percentages. Speakers who did not declare an age are listed as Unspecified. A dash (-) indicates zero.

| Code | Age | Clips | Speakers |
|---|---|---|---|
| teens | Teens | 184 (1.0%) | 16 (3.3%) |
| twenties | Twenties | 5,225 (27.5%) | 101 (21.0%) |
| thirties | Thirties | 6,081 (32.0%) | 31 (6.5%) |
| fourties | Fourties | 1,723 (9.1%) | 16 (3.3%) |
| fifties | Fifties | 255 (1.3%) | 2 (0.4%) |
| sixties | Sixties | 99 (0.5%) | 2 (0.4%) |
| seventies | Seventies | - | - |
| eighties | Eighties | - | - |
| nineties | Nineties | - | - |
| - | Unspecified | 5,462 (28.7%) | 328 (68.3%) |

*Age declared: 13,567 of 19,029 clips (71.3%), 152 of 480 speakers (31.7%)*

## Data splits for modelling

**Clip buckets**

| Bucket | Clips |
|---|---|
| Validated | 11,131 (58.5%) |
| Invalidated | 954 (5.0%) |
| Other | 6,944 (36.5%) |

**Training splits**

| Split | Clips |
|---|---|
| Train | 4,896 (44.0%) |
| Dev | 2,814 (25.3%) |
| Test | 3,342 (30.0%) |

*Training split coverage: 11,052 of 11,131 validated clips (99.3%)*

The dataset contains 11131 validated, 954 invalidated, and 6944 unresolved clips. The average clip duration is 5.047 seconds.

## Text corpus

**Validated sentences:** 32,205

| Category | Count |
|---|---|
| Unvalidated sentences | 9,964 |
| Pending sentences | 9,957 |
| Rejected sentences | 7 |
| Reported sentences | 146 |

The corpus contains 42,169 sentences: 32,205 validated and 9,964 unvalidated (9,957 pending review, 7 rejected), with 146 reported for review.

### Sample

There follows a randomly selected sample of five sentences from the corpus.

1. *रक्षा मंत्रालय ने लेफ्टिनेंट जनरल सुहाग को सेना प्रमुख बनाने की अनुशंसा की*
2. *कहां गुम हो रहीं सरकारी फाइलें*
3. *शादी में जूता हुआ चोरी तो दूल्हे ने पीट-पीट कर मार डाला*
4. *मुझपर हमला किया गया।*
5. *संजू सैमसन का शतक, श्रीलंका और बोर्ड इलेवन के बीच ड्रा रहा अभ्यास मैच*

### Sources

| Source | Sentences |
|---|---|
| sentence-collector | 32,033 (99.5%) |
| Other | 172 (0.5%) |

### Fields

#### Clips

Each row of a `tsv` file represents a single audio clip, and contains the following information:

- `client_id` - hashed UUID of a given user
- `path` - relative path of the audio file
- `sentence` - the sentence to be read aloud
- `sentence_id` - unique identifier for the sentence
- `sentence_domain` - domain classification(s) of the sentence
- `up_votes` - number of people who said audio matches the text
- `down_votes` - number of people who said audio does not match text
- `age` - age of the speaker[^1]
- `gender` - gender of the speaker[^1]
- `accents` - accents of the speaker[^1]
- `variant` - variant of the language[^1]
- `locale` - locale code of the language
- `segment` - if sentence belongs to a custom dataset segment, it will be listed here

[^1]: For a full list of age, gender, and accent options, see the [demographics spec](https://github.com/common-voice/common-voice/blob/main/web/src/stores/demographics.ts). These will only be reported if the speaker opted in to provide that information.

#### `validated_sentences.tsv`

The `validated_sentences.tsv` file contains one row per validated sentence in the text corpus:

- `sentence_id` - unique identifier for the sentence
- `sentence` - the sentence text
- `variant` - the variant of the language
- `sentence_domain` - the domain(s) the sentence belongs to
- `source` - the source the sentence was collected from
- `is_used` - whether the sentence is still in circulation for recording
- `clips_count` - number of clips recorded for this sentence

#### `unvalidated_sentences.tsv`

The `unvalidated_sentences.tsv` file contains one row per unvalidated sentence in the text corpus:

- `sentence_id` - unique identifier for the sentence
- `sentence` - the sentence text
- `variant` - the variant of the language
- `sentence_domain` - the domain(s) the sentence belongs to
- `source` - the source the sentence was collected from
- `up_votes` - number of upvotes the sentence received
- `down_votes` - number of downvotes the sentence received
- `status` - current status of the sentence (`pending` or `rejected`)

## Get involved

### Community links

- [Common Voice translators on Pontoon](https://pontoon.mozilla.org/hi/common-voice/contributors/)
- [Common Voice Communities](https://github.com/common-voice/common-voice/blob/main/docs/COMMUNITIES.md)

### Discussions

- [Common Voice on Matrix](https://chat.mozilla.org/#/room/#common-voice:mozilla.org)
- [Common Voice on Discourse](https://discourse.mozilla.org/t/about-common-voice-readme-first/17218)
- [Common Voice on Discord](https://discord.gg/9QTj9zwn)
- [Common Voice on Telegram](https://t.me/mozilla_common_voice)

### Contribute

- [Speak](https://commonvoice.mozilla.org/hi/speak)
- [Write](https://commonvoice.mozilla.org/hi/write)
- [Listen](https://commonvoice.mozilla.org/hi/listen)
- [Review](https://commonvoice.mozilla.org/hi/review)

## Licence

This dataset is released under the [Creative Commons Zero (CC-0)](https://creativecommons.org/public-domain/cc0/) licence. By downloading this data you agree to not determine the identity of speakers in the dataset.
