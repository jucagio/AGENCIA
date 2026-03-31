from src.agents.registry import get_agent, AGENT_REGISTRY


def test_all_agents_registered():
    expected = {"jarvis", "jade", "sasha", "brook", "erik", "cinthya", "ego"}
    assert set(AGENT_REGISTRY.keys()) == expected


def test_get_agent_by_mention():
    agent = get_agent("@jarvis")
    assert agent is not None
    assert agent.name == "jarvis"
    assert agent.model == "claude-opus-4-5"


def test_get_agent_without_at():
    agent = get_agent("jade")
    assert agent is not None
    assert agent.name == "jade"


def test_unknown_agent_returns_none():
    assert get_agent("desconocido") is None


def test_opus_agents():
    for name in ["jarvis", "sasha", "ego"]:
        assert "opus" in get_agent(name).model


def test_sonnet_agents():
    for name in ["jade", "brook", "erik", "cinthya"]:
        assert "sonnet" in get_agent(name).model
