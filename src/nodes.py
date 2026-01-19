from langchain_core.messages import SystemMessage, HumanMessage
from uuid import uuid4
from .prompts import *
from .models import *
from config.settings import *

def plan_outline(planner_llm):
    
    async def _node(state: SeminarState):
    
        """
        Step 1: Create SIMPLE 5-section outline
        Mimics: Human deciding report structure
        """
        response = await planner_llm.with_structured_output(Plan).ainvoke([
            SystemMessage(content=plan_outline_prompt), 
            HumanMessage(content=state['topic'])
        ])
        
        outline = response.Plan    
        return {
            "outline": outline,
            "current_section_index": 0,
            "final_report": []
        }
    return _node

def brainstorm_section(llm):

    async def _node(state: SeminarState):
        idx = state["current_section_index"]
        section = state["outline"][idx]
        state["current_section"] = section
        print(section)
        print("\n" + "="*60)
        print(f"💡 STEP 2: BRAINSTORMING ")
        print("="*60)
        key_points = await llm.with_structured_output(Keypoints).ainvoke([
            SystemMessage(content=research_paln_prompt.format(
            topic=state['topic'],
            section=section)),
            HumanMessage(content=state['topic'])
        ])
        
        key_points = key_points.Keypoints
        
        print(f"\n✓ Identified {len(key_points)} key points:")
        
        return {
            "key_points": key_points,
            "current_section": section
        }
    return _node

def should_continue(state: SeminarState) -> Literal["continue", "done"]:
    if state["current_section_index"] >= len(state["outline"]):
        return "done"
    return "continue"

def research_section(retriever, web_search):
    async def _node(state: SeminarState):
        print("\n" + "="*60)
        print(f"🔍 STEP 3: GATHERING INFORMATION")
        print("="*60)
        section = state["current_section"]
        points = state["key_points"]

        web_text = ""
        rag_text = ""
        
        for p in points:
            
            # Research query combines topic + section + key points
            query = f"For this topic: {state['topic']} find the information for{' '.join(p)}"
            
            print(f"\n→ Web search: {query[:80]}...")
            try:
                response = await web_search.ainvoke(query)
                
                web_text = web_text + response['content']
        
            except Exception as e:
                print(f"  ⚠️ Web search failed: {e}")
                web_text = "No web results available"
            
            print(f"\n→ RAG retrieval: {section}...")
            try:
                docs = await retriever.ainvoke(query)
                rag_text = rag_text + ("\n\n".join([
                    f"Document excerpt {i+1}:\n{d.page_content}"
                    for i, d in enumerate(docs[:3])
                ]))
            except Exception as e:
                print(f"  ⚠️ RAG retrieval failed: {e}")
                rag_text = "No local documents available"

        print(f"\n✓ Gathered {len(web_text)} chars from web, {len(rag_text)} chars from papers")

        return {
            "web_context": web_text,
            "rag_context": rag_text
        }
    return _node

def write_section(llm):

    async def _node(state: SeminarState):
        """
        Step 4: Write the actual content
        Mimics: Human writing with gathered information
        """
        print("\n" + "="*60)
        print(f"✍️  STEP 4: WRITING SECTION")
        print("="*60)
        
        user_message = HumanMessage(
            content=f"MAIN TOPIC: {state['topic']}\n\nHere is my plan:\n\n{state['outline']}")
        messages = [
            SystemMessage(
                content=writing_prompt.format(section=state['current_section'], key_points=state['key_points'], CONTEXT=state.get('web_context', '') + "\n" + state.get('rag_context', ''))
            ),
            user_message
            ]
        response = await llm.ainvoke(messages)
        print(f"the section {state['current_section_index']+1}. {state['current_section']}: is completed")
        draft = f"## Section {state['current_section_index']+1}. {state['current_section']}: \n\n{response.content.strip()}"
        
        word_count = len(draft.split())
        print(f"\n✓ Generated draft: {word_count} words")
        
        return {
            "draft": draft, 
            "revision_number": state.get("revision_number", 0) + 1
        }
    return _node

def route_after_validation(state: SeminarState):
    if state["is_valid"]:
        return "save"
    if state["revision_count"] >= 2:
        return "save"
    return "write"

def save_and_next(state: SeminarState):
    drafts = state.get("section_drafts", [])
    drafts.append(state["draft"])

    return {
        "section_drafts": drafts,
        "current_section_index": state["current_section_index"] + 1
    }


def validate_section(pcllm):
    async def _node(state: SeminarState):
        """
        Step 5: Check if section is good
        Mimics: Human self-editing
        """
        print("\n" + "="*60)
        print(f"🔍 STEP 5: VALIDATION")
        print("="*60)
        topic = state['topic']
        draft = state['draft']
        messages = [
            SystemMessage(content=research_critic_prompt.format(topic=topic,section=state['current_section'])), 
            HumanMessage(content=draft)
        ]
        
        response = await pcllm.ainvoke(messages)
        feedback = response.content.strip()
        
        is_valid = "approve" in feedback.lower()
        
        if is_valid:
            print(f"✓ Section APPROVED")
        else:
            print(f"✗ Needs revision: {feedback[:100]}")
        
        return {
            "is_valid": is_valid,
            "feedback": feedback,
            "revision_count": state["revision_count"] + 1
        }
    return _node


def synthesize_full_report(llm):
    async def _node(state: SeminarState):
        print("\n🧠 GLOBAL SYNTHESIS: CONNECTING ALL SECTIONS")

        combined_sections = "\n\n".join(state["section_drafts"])

        prompt = full_paper_prompt.format(
            topic=state['topic'],
            outline=", ".join(state['outline']),
            combined_sections=combined_sections
        )
        response = await llm.ainvoke(prompt)
        return {
            "final_paper": response.content
        }
    return _node
