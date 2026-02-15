"""Tests for crew.py — verifies imports, agent config, and crew structure."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_crewai_imports():
    """CrewAI packages are installed and importable."""
    from crewai import Agent, Task, Crew
    from langchain_openai import ChatOpenAI


def test_crew_module_imports():
    """crew.py imports without errors."""
    import crew


def test_llm_configured_for_domekit():
    """LLM points at DomeKit's local endpoint."""
    import crew

    base = str(crew.llm.openai_api_base)
    assert "localhost:8080" in base


def test_two_agents_defined():
    """Crew should have a researcher and a writer."""
    import crew

    assert crew.researcher is not None
    assert crew.writer is not None
    assert crew.researcher.role is not None
    assert crew.writer.role is not None


def test_two_tasks_defined():
    """Crew should have a research task and a report task."""
    import crew

    assert crew.research_task is not None
    assert crew.report_task is not None


def test_crew_has_both_agents():
    """The Crew object should include both agents."""
    import crew

    agent_roles = [a.role for a in crew.crew.agents]
    assert len(agent_roles) == 2


def test_crew_has_both_tasks():
    """The Crew object should include both tasks."""
    import crew

    assert len(crew.crew.tasks) == 2


def test_research_task_mentions_database():
    """Research task should reference the products database."""
    import crew

    assert "products" in crew.research_task.description.lower()
