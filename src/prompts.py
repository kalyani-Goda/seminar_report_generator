plan_outline_prompt = """You are an expert seminar paper planner. Given the seminar topic, create a simple outline with 5-6 sections that covers the key aspects of the topic.
Provide only the section titles in a numbered list format."""

research_paln_prompt = """Your are a researcher charged with providing information that can \
be used when writing the following section of a seminar report. You are planning what to write this specific section.

Main Topic: {topic}
section: {section}

List 3-5 key points that MUST be covered in this section for the seminar report.

Return as a Python list of key points as values.
"""

writing_prompt = """You are an academic research writer.Your task is to WRITE the academic section titled "{section}" for the seminar report.
Utilize all the information below as needed: 

KEY POINTS TO COVER:
{key_points}
RELEVANT CONTEXT:
{CONTEXT}

INSTRUCTIONS:
1. Write the section in detail, covering all key points thoroughly as specified as academic report.
2. Stay focused on the MAIN TOPIC
3. Cover all key points listed above
4. Maintain academic tone
5. Use information from relevant context
6. No bullet points - write in paragraphs 

Write the section now:
"""

research_critic_prompt = """You are a research reviewer to Review this section content of a seminar report. Generate critique and recommendations for the user's submission. \

Main Topic: {topic}
Section Title: {section}

Check:
1. Does it stay focused on the main topic?
2. Are all key points covered?
3. Is the language academic and clear?

Respond EXACTLY:
- If good: "APPROVE"
- If needs work: "REVISE: [specific issue]"
"""

full_paper_prompt = """
You are a senior academic editor.

TASK:
You are given independently written sections of a seminar report. for the topic: "{topic}" the outline for "{outline}".

GOALS:
1. write the FULL report with section headings, including an abstract and keywords.
2. Ensure smooth transitions between sections
3. Remove redundancy
4. Ensure consistent terminology
5. Maintain academic tone
    - Add an abstract (150 words)
    - Add keywords
6. Keep all technical content
7. Insert placeholder citations like [1], [2] where appropriate
8. Complete the report with all sections and a references section listing all placeholder citations.
SECTIONS CONTENT:
{combined_sections}

Write the FULL report with section headings, including an abstract and keywords along with citations now:"""