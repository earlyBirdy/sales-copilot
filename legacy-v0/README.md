# Sales Copilot v0

Sales Copilot v0 is a human-in-the-loop assistant that converts incoming emails, articles, press releases, and product updates into reviewable sales communication drafts.

## Purpose

The goal is to save time for sales and business development work by turning one source into multiple editable outbound drafts while keeping the user in control before anything is sent.

Core workflow:

`source in -> structured extraction -> audience-specific drafts -> user review/edit -> export final copy`

## v0 principles

- Human-in-the-loop
- Source-grounded
- Multi-audience
- Editable-first
- No auto-send
- Commercially useful, not just summarization

## Supported input types

- pasted email text
- uploaded email text
- pasted article text
- pasted press release
- pasted announcement note

## Supported outputs

- internal team share
- existing customer message
- prospect outreach
- partner/distributor note
- LinkedIn DM
- LinkedIn post
- CRM-style summary note

## v0 non-goals

- auto-send
- CRM sync
- bulk campaign automation
- inbox monitoring
- autonomous agent behavior
- analytics dashboard

## Folder overview

- `schemas/` JSON schemas for inputs and outputs
- `prompts/` modular prompt files
- `app/` lightweight pipeline code
- `examples/` sample inputs and outputs

## Basic pipeline

1. Intake source
2. Summarize source
3. Extract sales signals
4. Reframe for selected audience
5. Generate draft variants
6. Revise with user edits
7. Export clean output

## Example usage

Input:
- source text
- audience = customer
- tone = technical_commercial
- lengths = short, medium

Output:
- 3-bullet summary
- extracted sales signals
- 2 customer drafts
- CTA options
- review notes

## Run

```bash
python -m app.pipeline
```

This starter pack is scaffold-first. It includes schemas, prompts, examples, and a simple local pipeline with placeholder logic that you can replace with model calls later.
