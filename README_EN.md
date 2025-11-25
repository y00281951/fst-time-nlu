# FST Time NLU

## Time Expression Recognition and Parsing

[![CI](https://github.com/y00281951/fst-time-nlu/workflows/CI/badge.svg)](https://github.com/y00281951/fst-time-nlu/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🚀 Online Demo

**👉 [Try Live Demo Now](https://fst-time-nlu-t52oauj46kezvmgah25whe.streamlit.app/) 👈**

No installation required, experience time expression recognition directly in your browser!

---

### Introduction

FST Time NLU is a **production-grade** time expression recognition and parsing toolkit based on Finite-State Transducer (FST) technology.

**Core Features**:

- ⚡ **High Performance**: Average inference latency ~4ms, 10-100x faster than deep learning methods
- 🎯 **High Accuracy**: 95%+ accuracy, supports multiple complex time expressions
- 🌏 **Bilingual Support**: Chinese and English time expressions
- 🔧 **Easy to Customize**: Rule-based, quick to modify and extend
- 📦 **Ready to Use**: Provides Python API and command-line tools, can be used directly as a submodule

**Supported Time Expression Types**:

- Absolute time: `2025年1月21日上午9点`, `January 21, 2025 at 9 AM`
- Relative time: `明天上午9点`, `下周一`, `3天后`, `tomorrow at 9 AM`
- Time intervals: `从明天到后天`, `上午9点到下午5点`, `from 9 AM to 5 PM`
- Holidays: `春节`, `国庆节`, `Christmas`, `Thanksgiving`
- Lunar calendar: `正月初一`, `腊月二十三`
- Recurring time: `每天上午9点`, `每周一`, `every Monday`

## 💻 Run Locally

```bash
# Clone the repository
git clone https://github.com/y00281951/fst-time-nlu.git
cd fst-time-nlu

# Install dependencies
pip install -r requirements.txt

# Start web application
streamlit run app.py
```

Then open **http://localhost:8501** in your browser!

**Deployment Guide**: See [.streamlit/DEPLOYMENT_GUIDE.md](.streamlit/DEPLOYMENT_GUIDE.md) to learn how to deploy the app to Streamlit Cloud.

## How to Use

### 1. Quick Start

#### 1.1 Installation

```bash
# Install from source
git clone https://github.com/y00281951/fst-time-nlu.git
cd fst-time-nlu
pip install -r requirements.txt
```

#### 1.2 Command Line Usage

```bash
# Chinese time parsing
python main.py --text "明天上午9点" --language chinese

# English time parsing
python main.py --text "tomorrow at 9 AM" --language english

# Batch process files
python main.py --file src/english/test/groundtruth_utc_700english.jsonl --language chinese
```

#### 1.3 Python API Usage

```python
from src.chinese.fst_time_extractor import FstTimeExtractor

# Create extractor instance
extractor = FstTimeExtractor(overwrite_cache=False)

# Parse time text
datetime_results, query_tag = extractor.extract(
    "明天上午9点开会",  # "Meeting at 9 AM tomorrow"
    base_time="2025-01-21T08:00:00Z"
)
print(f"Recognition result: {datetime_results}")
# Output: Recognition result: ['2025-01-22T09:00:00Z']

# Process time intervals
datetime_results, query_tag = extractor.extract(
    "从明天上午9点到下午5点",  # "From 9 AM to 5 PM tomorrow"
    base_time="2025-01-21T08:00:00Z"
)
print(f"Recognition result: {datetime_results}")
# Output: Recognition result: ['2025-01-22T09:00:00Z', '2025-01-22T17:00:00Z']
```

### 2. Advanced Usage

#### 2.1 Custom Rules

If you need to modify or add rules to fix bad cases, try:

```bash
git clone https://github.com/y00281951/fst-time-nlu.git
cd fst-time-nlu
pip install -r requirements.txt

# `overwrite_cache` will rebuild all rules based on your modifications to src/chinese/rules/xx.py
# After rebuilding, you can find new .fst files in the current directory
python main.py --text "明天上午9点" --language chinese --overwrite_cache
```

#### 2.2 Using Custom Rules

After successfully rebuilding the rules, you can use them in the installed package:

```python
from src.chinese.fst_time_extractor import FstTimeExtractor

# Use custom cache directory
extractor = FstTimeExtractor(cache_dir="PATH_TO_YOUR_CUSTOM_CACHE")
datetime_results, query_tag = extractor.extract("明天上午9点")
print(datetime_results)
```

## Technical Architecture

### Overall Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface Layer                    │
│  ┌──────────────────────────┐  ┌──────────────────────┐    │
│  │      Python API          │  │   Command Line Tool  │    │
│  └──────────────────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Time Extractor Layer (FstTimeExtractor)         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Unified interface encapsulation                   │  │
│  │  • Cache management                                  │  │
│  │  • Performance statistics                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                Text Normalization Layer (Normalizer)         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • FST model loading and compilation                 │  │
│  │  │  Text preprocessing → FST recognition → Tag gen  │  │
│  │  • Traditional/Simplified conversion, number norm.   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Time Parser Layer (TimeParser)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Tag parsing and time calculation                  │  │
│  │  • Relative time to absolute time                    │  │
│  │  • Context merging and conflict resolution           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Parser Layer (Parsers)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Relative │ │ Between  │ │ Holiday  │ │  Lunar   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Delta   │ │  Period  │ │   Week   │ │ UTC Time │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Rules Layer (Rules)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • FST rule definition (based on pynini)             │  │
│  │  • Linguistic rule encoding                          │  │
│  │  • Pattern matching and transformation               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Resource Layer (Data)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │Dictionary│ │ Holidays │ │  Number  │ │  Config  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Core Module Description

#### 1. FstTimeExtractor (Time Extractor)

- **Responsibility**: Unified time extraction interface
- **Features**:
  - Integrate text normalization and time parsing
  - FST model cache management
  - Performance statistics and monitoring
- **Usage**: Main entry point for user calls

#### 2. Normalizer (Text Normalizer)

- **Responsibility**: Convert natural language text to structured tags
- **Features**:
  - FST model loading and compilation
  - Text preprocessing (Traditional/Simplified conversion, full/half-width conversion, etc.)
  - Pattern matching and tag generation
- **Input**: Raw text (e.g., "明天上午9点" / "tomorrow at 9 AM")
- **Output**: Structured tags (e.g., "TIME#2025-01-22T09:00:00Z")

#### 3. TimeParser (Time Parser)

- **Responsibility**: Convert tags to specific time values
- **Features**:
  - Tag parsing and validation
  - Relative time to absolute time
  - Context merging and conflict resolution
- **Input**: Tag sequence
- **Output**: ISO 8601 format time string

#### 4. Parsers (Specialized Parsers)

- **RelativeParser**: Handle relative time (tomorrow, next week, 3 days later)
- **BetweenParser**: Handle time intervals (from...to...)
- **HolidayParser**: Handle holidays (Spring Festival, Christmas)
- **LunarParser**: Handle lunar calendar (first day of lunar new year, etc.)
- **PeriodParser**: Handle time periods (morning, afternoon, evening)
- **WeekParser**: Handle weekdays (Monday, weekend)
- **DeltaParser**: Handle time deltas (3 hours later, 2 days ago)
- **RecurringParser**: Handle recurring time (every day, every Monday)

#### 5. Rules (FST Rules)

- **Responsibility**: Define time expression recognition rules
- **Technology**: Build FST based on pynini library
- **Features**:
  - Declarative rule definition
  - Composable and reusable
  - Support weights and priorities

#### 6. Data (Data Resources)

- **Dictionary data**: Time vocabulary, number mappings
- **Holiday data**: Chinese holidays, international holidays
- **Configuration files**: Parser configurations, rule parameters

## Main Features

### Core Features

- **FST Model**: Efficient time expression recognition based on finite-state transducers
- **Multi-format Support**: Support absolute time, relative time, time intervals, and various other expressions
- **Text Normalization**: Automatic handling of Traditional/Simplified conversion, full/half-width conversion, number normalization, etc.
- **Cache Mechanism**: FST model caching for improved reuse performance

### Parser Types

- **Base Parser** (`base_parser.py`): Provides basic parser functionality
- **Between Parser** (`between_parser.py`): Handles "from...to..." type time intervals
- **Delta Parser** (`delta_parser.py`): Handles relative time deltas, such as "3 hours later"
- **Holiday Parser** (`holiday_parser.py`): Recognizes Chinese traditional holidays
- **Lunar Parser** (`lunar_parser.py`): Supports lunar calendar time expressions
- **Period Parser** (`period_parser.py`): Handles time periods like "morning", "evening"
- **Relative Parser** (`relative_parser.py`): Handles relative expressions like "tomorrow", "next week"
- **UTC Time Parser** (`utctime_parser.py`): Handles UTC time format
- **Week Parser** (`week_parser.py`): Handles week-related expressions
- **Context Merger** (`context_merger.py`): Intelligently merges multiple time tokens, handles complex time expression combinations, such as "tomorrow morning at 9", "next Monday evening at 8"

## Chinese Time Expression Recognition Capabilities

Base time defaults to 2025-01-21T08:00:00

### Supported Time Expression Types

#### Absolute Time and Relative Time (UTCTimeRule / RelativeRule)

| Query                                          | Result                                             | Notes                     |
| ---------------------------------------------- | -------------------------------------------------- | ------------------------ |
| 查询20240307计划 (Check plan for 20240307)     | `["2024-03-07T00:00:00Z", "2024-03-07T23:59:59Z"]` | Recognize pure number date from sentence |
| 农历二〇二〇年十二月二十九日原告去被告家看嫁妆 (Lunar date in long sentence) | `["2021-02-10T00:00:00Z", "2021-02-10T23:59:59Z"]` | Recognize Chinese number date from long sentence |
| 住在南京网2021-09-21热度 578瞰地 (Living in Nanjing net 2021-09-21) | `["2021-09-21T00:00:00Z", "2021-09-21T23:59:59Z"]` | Recognize date from sentence |
| 下下下周一 (Three Mondays from now)            | `["2025-02-10T00:00:00Z", "2025-02-10T23:59:59Z"]` | Recognize multiple relative times |
| 上上个月五号 (5th of two months ago)           | `["2024-11-05T00:00:00Z", "2024-11-05T23:59:59Z"]` | Recognize multiple relative months plus date |
| 他在10月22出生 (He was born on Oct 22)         | `["2025-10-22T00:00:00Z", "2025-10-22T23:59:59Z"]` | Recognize relative month date from sentence |

#### Time Delta and Week (DeltaRule / WeekRule)

| Query                          | Result                                                       | Notes                   |
| ------------------------------ | ------------------------------------------------------------ | ---------------------- |
| 大概六天后的3时1刻需要处理东西 (About 6 days later at 3:15) | `["2025-01-27T03:15:00Z"]`                                   | Fuzzy time delta plus exact time |
| 在近一年的时间内保 (Within nearly a year) | `["2024-01-06T00:00:00Z", "2025-01-06T00:00:00Z"]`           | Recognize time range from sentence |
| 周一或周二都可以 (Monday or Tuesday both OK) | `[['2025-01-20T00:00:00Z', '2025-01-20T23:59:59Z'], ['2025-01-21T00:00:00Z', '2025-01-21T23:59:59Z']]` | Recognize multiple weekday options |
| 6月第3个星期日 (3rd Sunday of June) | `["2025-06-15T00:00:00Z", "2025-06-15T23:59:59Z"]`           | Recognize Nth weekday of month |

#### Period, Holiday and Lunar (Period Rule / HolidayRule / LunarRule)

| Query                                          | Result                                             | Notes                     |
| ---------------------------------------------- | -------------------------------------------------- | ------------------------ |
| 大前天晚上9~11点 (Night 9-11PM three days ago) | `["2025-01-03T21:00:00Z", "2025-01-03T23:00:00Z"]` | Multiple relative time plus period range |
| 今晚八点30到明天上午 (Tonight 8:30 to tomorrow morning) | `["2025-01-21T20:30:00Z", "2025-01-22T12:00:00Z"]` | Recognize cross-day time period |
| 3月11日下午15:30-17:00 (March 11 afternoon 15:30-17:00) | `["2025-03-11T15:30:00Z", "2025-03-11T17:00:00Z"]` | Date plus period range |
| 明年母亲节 (Next year Mother's Day)            | `["2026-05-10T00:00:00Z", "2026-05-10T23:59:59Z"]` | Recognize relative year plus holiday |
| 冬至那天 (Winter Solstice day)                 | `["2025-12-21T00:00:00Z", "2025-12-21T23:59:59Z"]` | Recognize solar term date |
| 农历二〇二〇年十二月二十九日原告去被告家看嫁妆 (Full lunar date in sentence) | `["2021-02-10T00:00:00Z", "2021-02-10T23:59:59Z"]` | Recognize complete lunar date from long sentence |
| 今年腊月18000吨物品被寄 (This year 12th lunar month) | `["2024-12-31T00:00:00Z", "2025-01-28T23:59:59Z"]` | Find lunar time from long sentence |
| 腊月18，已经过了好几天 (12th lunar month 18th) | `["2025-01-17T00:00:00Z", "2025-01-17T23:59:59Z"]` | Recognize lunar date from sentence |

#### Time Range, Period and Between (RangeRule / PeriodRule / BetweenRule)

| Query                                            | Result                                               | Notes                   |
| ------------------------------------------------ | ---------------------------------------------------- | ---------------------- |
| 帮我查下15点20分到16点30的会议室 (Check meeting room 15:20-16:30) | `["2025-01-21T15:20:00Z", "2025-01-21T16:30:00Z"]`   | Recognize time range from sentence |
| 1月3至2月10 (Jan 3 to Feb 10)                    | `["2025-01-03T00:00:00Z", "2025-02-10T23:59:59Z"]`   | Recognize month date range |
| 在2021年4月20日11:00至2021年4月25日17:00对对方为 (Long sentence with time range) | `[["2021-04-20T11:00:00Z", "2021-04-25T17:00:00Z"]]` | Find time range from long sentence |
| 2018年年底 (End of 2018)                         | `["2018-11-01T00:00:00Z", "2018-12-31T23:59:59Z"]`   | Recognize year-end of specified year |
| 过去一个月所有生产事故问题统计 (Past month's statistics) | `["2024-12-06T00:00:00Z", "2025-01-06T00:00:00Z"]`   | Recognize period range from sentence |
| 上个世纪 (Last century)                          | `["1900-01-01T00:00:00Z", "1999-12-31T23:59:59Z"]`   | Recognize century time range |
| 20世纪60年代前期 (Early 1960s)                   | `["1960-01-01T00:00:00Z", "1969-12-31T23:59:59Z"]`   | Recognize early decade time range |

#### Time Word Ambiguity Filtering

| Query            | Result                       | Notes                             |
| ---------------- | ---------------------------- | -------------------------------- |
| 再说两点 (Let's talk about two points) | `[]` | "两点" means enumeration points, not time |
| 简洁一点 (A bit more concise) | `[]` | "一点" means degree, not time |
| 是一个十一点的事 (It's an 11 o'clock matter) | `[["2025-07-25T11:00:00Z"]]` | "十一点" correctly recognized in time context |

#### Number and Text Filtering

| Query                      | Result | Notes                         |
| -------------------------- | ------ | ---------------------------- |
| 45901                      | `[]`   | Pure number is not a date |
| 身份证号140302197706220124 (ID number) | `[]` | Numbers in ID not recognized as date |
| 黎明主演的电影已上映 (Movie starring Li Ming) | `[]` | "黎明" is a person's name, not time |
| 一日之计在于晨 (Chinese idiom) | `[]` | Time words in idioms not recognized |

## English Time Expression Recognition Capabilities

Base time defaults to 2025-01-21T08:00:00Z

### Supported Time Expression Types

#### Absolute Time and Relative Time (UTCTimeRule / RelativeRule)

| Query                                          | Result                                             | Notes                   |
| ---------------------------------------------- | -------------------------------------------------- | ---------------------- |
| living in nanjing net 2021-09-21 popularity 578 view | `[["2021-09-21T00:00:00Z", "2021-09-21T23:59:59Z"]]` | Recognize date from long sentence |
| three Mondays from now                         | `[["2025-02-10T00:00:00Z", "2025-02-10T23:59:59Z"]]` | Recognize multiple week increments |
| the day after tomorrow                         | `[["2025-01-23T00:00:00Z", "2025-01-23T23:59:59Z"]]` | Recognize compound relative time |
| day after tomorrow 5pm                         | `[["2025-01-23T17:00:00Z"]]`                       | Relative date plus exact time |
| march 3 2015                                   | `[["2015-03-03T00:00:00Z", "2015-03-03T23:59:59Z"]]` | Recognize complete date format |
| the first of march                             | `[["2025-03-01T00:00:00Z", "2025-03-01T23:59:59Z"]]` | Recognize ordinal date format |

#### Time Delta and Week (TimeDeltaRule / WeekRule)

| Query                          | Result                                             | Notes                       |
| ------------------------------ | -------------------------------------------------- | -------------------------- |
| in a couple of minutes         | `[["2025-01-21T08:02:00Z"]]`                       | Recognize fuzzy time increment |
| in a few hours                 | `[["2025-01-21T11:00:00Z"]]`                       | Recognize fuzzy hour increment |
| first tuesday of october       | `[["2025-10-07T00:00:00Z", "2025-10-07T23:59:59Z"]]` | Recognize Nth weekday of month |
| last Monday of March           | `[["2025-03-31T00:00:00Z", "2025-03-31T23:59:59Z"]]` | Recognize last few weekdays of month |
| third tuesday of september 2014 | `[["2014-09-16T00:00:00Z", "2014-09-16T23:59:59Z"]]` | Recognize Nth weekday of month in specified year |
| wednesday after next           | `[["2025-01-29T00:00:00Z", "2025-01-29T23:59:59Z"]]` | Recognize compound week expression |

#### Period and Holiday (PeriodRule / HolidayRule)

| Query                                  | Result                                             | Notes                   |
| -------------------------------------- | -------------------------------------------------- | ---------------------- |
| late last night                        | `[["2025-01-20T18:00:00Z", "2025-01-20T23:59:59Z"]]` | Recognize multiple relative time plus period |
| tonight at 8 o'clock                   | `[["2025-01-21T20:00:00Z"]]`                       | Recognize relative period plus exact time |
| morning of christmas 2013              | `[["2025-12-25T06:00:00Z", "2025-12-25T12:00:00Z"]]` | Recognize holiday plus period |
| next thanksgiving day                  | `[["2026-11-26T00:00:00Z", "2026-11-26T23:59:59Z"]]` | Recognize relative year plus holiday |
| next Martin Luther King day            | `[["2026-01-19T00:00:00Z", "2026-01-19T23:59:59Z"]]` | Recognize complex holiday name |
| from tonight 8:30 to tomorrow morning  | `[["2025-01-21T20:30:00Z", "2025-01-22T12:00:00Z"]]` | Recognize cross-day time period |

#### Time Range, Period and Between (RangeRule / TimeRangeRule / CenturyRule)

| Query                                            | Result                                               | Notes                   |
| ------------------------------------------------ | ---------------------------------------------------- | ---------------------- |
| from 9:30 - 11:00 on Thursday                   | `[["2025-01-23T09:30:00Z", "2025-01-23T11:00:00Z"]]` | Recognize time range plus weekday from sentence |
| between 9:30 and 11:00 on thursday              | `[["2025-01-23T09:30:00Z", "2025-01-23T11:00:00Z"]]` | Recognize time range with "between" |
| scheduled from april 20 2021 11:00 to april 25 2021 17:00 | `[["2021-04-20T11:00:00Z", "2021-04-25T17:00:00Z"]]` | Find complete time range from long sentence |
| for 10 days from 18th Dec                       | `[["2025-12-18T00:00:00Z", "2025-12-28T23:59:59Z"]]` | Recognize duration range |
| last 2 years                                     | `[["2023-01-21T08:00:00Z", "2025-01-21T08:00:00Z"]]` | Recognize multi-year time range |
| last century                                     | `[["1900-01-01T00:00:00Z", "1999-12-31T23:59:59Z"]]` | Recognize century time range |
| the 80s                                          | `[["1980-01-01T00:00:00Z", "1989-12-31T23:59:59Z"]]` | Recognize decade time range |

#### Mixed Complex Expressions

| Query                                                                        | Result                                                       | Notes                 |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------- |
| 2015-03-28 17:00:00/2015-03-29 21:00:00                                     | `[["2015-03-28T17:00:00Z"], ["2015-03-29T21:00:00Z"]]`       | Recognize multiple time points |
| today that huizhou solar calendar march 8th                                 | `[["2025-01-21T00:00:00Z", "2025-01-21T23:59:59Z"], ["2025-03-08T00:00:00Z", "2025-03-08T23:59:59Z"]]` | Recognize multiple times from complex sentence |
| what do i need to prepare in advance if i want to go to chiang mai next new year's day | `[["2026-01-01T00:00:00Z", "2026-01-01T23:59:59Z"]]` | Recognize relative holiday from long sentence |

### Misrecognition Filtering Mechanism

#### Time Word Ambiguity Filtering

| Query            | Result | Notes                             |
| ---------------- | ------ | -------------------------------- |
| ten-thirty       | `[]`   | "ten-thirty" means quantity, not time |
| laughing out loud | `[]`   | "lol" abbreviation not recognized as time |
| this is the one  | `[]`   | "one" means reference, not time |

#### Number and Text Filtering

| Query    | Result | Notes                         |
| -------- | ------ | ---------------------------- |
| 1974     | `[]`   | Pure number is not a date |
| 1 adult  | `[]`   | "1 adult" means quantity, not time |
| 25       | `[]`   | Single number is not a date |

## Performance and Accuracy

### Performance Metrics

| Metric         | Value    |
| ------------ | ------- |
| Average inference latency | ~4ms    |
| CPU usage     | Low      |
| Memory usage     | < 100MB |
| Concurrency support     | Yes      |

### Accuracy

| Language | Test Set Size | Accuracy |
| ---- | ---------- | ------ |
| Chinese | 300+ samples | 95%+   |
| English | 700+ samples  | 95%+   |

### Benchmark Testing

```bash
# Chinese benchmark
python main.py --language chinese --file src/chinese/test/groundtruth_utc.jsonl

# English benchmark
python main.py --language english --file src/english/test/groundtruth_utc_700english.jsonl
```

## Core Module Description

### FstTimeExtractor (Main Entry)

- Provides unified time extraction interface
- Integrates text normalization and time parsing functions
- Supports FST model cache management

### Text Processing Workflow

1. **Preprocessing** (`preprocessor.py`): Text cleaning and normalization
2. **FST Recognition** (`test/fst/zh_tn_tagger.fst`): Use FST model to recognize time entities
3. **Rule Parsing** (`rules/`): Apply grammar rules for precise parsing
4. **Postprocessing** (`postprocessor.py`): Result normalization and validation

### Architecture Characteristics

1. **Modular Design**: Core processing logic separated from language-specific implementation
2. **Extensibility**: Supports adding new parsers and rules
3. **High Performance**: FST model provides efficient pattern matching
4. **Robustness**: Multi-level error handling and fault tolerance

## Dependencies

### Core Dependencies

- `pynini>=2.1.5` - FST construction and processing
- `python-dateutil>=2.8.0` - Date and time utilities
- `zhdate` - Chinese date processing
- `lunarcalendar` - Lunar calendar support
- `inflect>=5.0.0` - English number processing

### Development Dependencies

- `pytest>=6.0.0` - Testing framework
- `black>=21.0.0` - Code formatting
- `flake8>=3.8.0` - Code linting

## Discussion and Communication

Welcome to participate in discussions through the following ways:

- [GitHub Issues](https://github.com/y00281951/fst-time-nlu/issues) - Report issues, make suggestions
- [GitHub Discussions](https://github.com/y00281951/fst-time-nlu/discussions) - Technical discussions, usage communication

## Acknowledgments

1. Thanks to the authors of [OpenFst](https://www.openfst.org/twiki/bin/view/FST/WebHome) and [Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini) for their foundational libraries
2. Thanks to the [WeTextProcessing](https://github.com/wenet-e2e/WeTextProcessing) project for reference and inspiration
3. Thanks to all developers who have contributed to this project

## License

This project is licensed under the [Apache License 2.0](LICENSE).

Copyright (c) 2025 Ming Yu (yuming@oppo.com), Liangliang Han (hanliangliang@oppo.com)

## Citation

If this project helps your research or work, feel free to cite:

```bibtex
@misc{fst-time-nlu,
  title={FST Time NLU: Production First Time Expression Recognition},
  author={Ming Yu and Liangliang Han},
  year={2025},
  publisher={GitHub},
  howpublished={\url{https://github.com/y00281951/fst-time-nlu}}
}
```

