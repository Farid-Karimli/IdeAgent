# Project Overview

Automate exploring research directions on a topic. The goal is to set up an agentic system to help explore and evaluate possible research directions for a user-provided research topic. Think of a few agents communicating with each other, and iteratively work towards a comprehensive roadmap of research ideas and what each one entails.

## Current design

### Agent 1: Idea Generator

- Uses generative models to brainstorm potential research directions based on the input topic (e.g., herbaria identification).
- Incorporates existing knowledge from databases, recent papers, and relevant research trends.
- Outputs a list of potential directions, each accompanied by a brief explanation or reasoning.

### Agent 2: Evaluator & Organizer

- Critiques and evaluates the ideas from Agent 1 based on predefined metrics (e.g., feasibility, novelty, impact, or required resources).
- Suggests refinements or merges related ideas into broader themes.
- Iteratively refines the roadmap until it reaches a comprehensive and structured output.

### Interaction

The agents communicate iteratively, refining ideas and creating a structured roadmap of research questions, potential methods, datasets required, and expected challenges.
