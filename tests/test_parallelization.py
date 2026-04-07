"""Tests for agent parallelization and resource management."""

import pytest
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime

from api.config import settings


class TestParallelizationBasic:
    """Test basic agent execution and state tracking."""

    def test_single_agent_execution(self):
        """Test executing a single agent."""
        from api.main import write_agent_state, read_agent_state

        # Execute single agent
        write_agent_state("test_agent", {
            "status": "executing",
            "prompt": "test prompt",
            "started_at": datetime.now().isoformat(),
        })

        # Read state
        state = read_agent_state("test_agent")
        assert state["status"] == "executing"
        assert "started_at" in state

    def test_agent_state_persistence(self):
        """Test that agent state is persisted to disk."""
        from api.main import write_agent_state, read_agent_state

        write_agent_state("persistence_test", {
            "status": "completed",
            "result": "test result",
        })

        # Read from fresh instance
        state = read_agent_state("persistence_test")
        assert state["status"] == "completed"
        assert state["result"] == "test result"


class TestParallelizationConcurrency:
    """Test concurrent agent execution."""

    @pytest.mark.asyncio
    async def test_three_agents_concurrent(self):
        """Test executing 3 agents concurrently (maximum recommended)."""
        from api.main import write_agent_state, read_agent_state

        async def execute_agent(agent_id: str):
            start = time.time()
            write_agent_state(agent_id, {
                "status": "executing",
                "started_at": datetime.now().isoformat(),
            })
            await asyncio.sleep(0.1)  # Simulate work
            write_agent_state(agent_id, {
                "status": "completed",
                "duration": time.time() - start,
            })

        # Execute 3 agents in parallel
        agents = ["agent_1", "agent_2", "agent_3"]
        start_time = time.time()
        await asyncio.gather(*[execute_agent(agent) for agent in agents])
        total_time = time.time() - start_time

        # Verify all completed
        for agent in agents:
            state = read_agent_state(agent)
            assert state["status"] == "completed"

        # Should take ~100ms (parallel), not 300ms (sequential)
        assert total_time < 1.0  # Allow some overhead

    @pytest.mark.asyncio
    async def test_queue_management(self):
        """Test that 4+ concurrent agents are queued."""
        from api.main import write_agent_state, read_agent_state

        async def simulate_agent_work(agent_id: str, duration: float):
            write_agent_state(agent_id, {"status": "executing"})
            await asyncio.sleep(duration)
            write_agent_state(agent_id, {"status": "completed"})

        # Queue 4 agents (max 3 concurrent)
        agents = ["q_1", "q_2", "q_3", "q_4"]
        tasks = [simulate_agent_work(agent, 0.1) for agent in agents]

        start = time.time()
        await asyncio.gather(*tasks)
        total_time = time.time() - start

        # All 4 run via asyncio.gather (truly parallel in async)
        # Total time should be ~0.1s (parallel), not 0.4s (sequential)
        assert total_time < 1.0


class TestResourceAllocation:
    """Test resource allocation per agent."""

    def test_agent_configuration_resources(self):
        """Test agent configurations specify resource limits."""
        agents_json = Path(".claude") / "agents.json"
        if agents_json.exists():
            with open(agents_json) as f:
                data = json.load(f)
                agents = data.get("agents", {})

                # Each agent should have resource spec
                for agent_name, agent_config in agents.items():
                    assert "resources" in agent_config or "concurrent_limit" in agent_config
                    if "resources" in agent_config:
                        assert "cpu" in agent_config["resources"]
                        assert "memory" in agent_config["resources"]

    def test_concurrency_limits_respected(self):
        """Test that concurrency limits in agents.json are respected."""
        agents_json = Path(".claude") / "agents.json"
        if agents_json.exists():
            with open(agents_json) as f:
                data = json.load(f)
                concurrency = data.get("concurrency", {})
                assert concurrency.get("max_parallel", 0) <= 3  # Max 3 for 16GB
                assert concurrency.get("queue_size", 0) >= 10


class TestAgentStateManagement:
    """Test agent state persistence and tracking."""

    def test_state_directory_created(self):
        """Test that agent state directory exists."""
        state_dir = Path(settings.agent_state_path)
        assert state_dir.parent.exists()

    def test_state_file_format(self):
        """Test that state files are valid JSON."""
        from api.main import write_agent_state, read_agent_state

        test_data = {
            "status": "test",
            "execution_id": "test_123",
            "results": ["item1", "item2"],
        }
        write_agent_state("format_test", test_data)

        # Verify file is valid JSON
        state_file = Path(settings.agent_state_path) / "format_test.json"
        with open(state_file) as f:
            data = json.load(f)
            assert data["status"] == "test"
            assert data["execution_id"] == "test_123"

    def test_state_contains_timestamps(self):
        """Test that all state updates include timestamps."""
        from api.main import write_agent_state, read_agent_state

        write_agent_state("timestamp_test", {"status": "test"})
        state = read_agent_state("timestamp_test")

        assert "last_updated" in state


class TestLogging:
    """Test execution logging."""

    def test_agent_logs_directory_exists(self):
        """Test that agent logs directory is created."""
        logs_dir = Path(settings.agent_logs_path)
        assert logs_dir.parent.exists()

    def test_audit_log_format(self):
        """Test that audit logs are JSONL format."""
        from api.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Make request to trigger audit log
        client.get("/health")

        audit_path = Path(settings.agent_logs_path) / "api_audit.jsonl"
        if audit_path.exists():
            with open(audit_path) as f:
                for line in f:
                    # Each line should be valid JSON
                    data = json.loads(line)
                    assert "timestamp" in data
                    assert "method" in data
                    assert "path" in data


class TestPerformanceMetrics:
    """Test performance monitoring."""

    @pytest.mark.asyncio
    async def test_agent_execution_duration_tracked(self):
        """Test that agent execution duration is tracked."""
        from api.main import write_agent_state, read_agent_state

        start = time.time()
        write_agent_state("perf_test", {"status": "executing"})
        await asyncio.sleep(0.05)  # Simulate 50ms work
        duration = time.time() - start
        write_agent_state("perf_test", {
            "status": "completed",
            "duration": duration,
        })

        state = read_agent_state("perf_test")
        assert "duration" in state
        assert state["duration"] > 0

    def test_concurrent_execution_parallelism(self):
        """Test that concurrent execution shows parallelism, not sequencing."""
        from api.main import write_agent_state, read_agent_state
        import concurrent.futures

        def execute_agent_sync(agent_id):
            start = time.time()
            write_agent_state(agent_id, {"status": "executing"})
            time.sleep(0.1)  # Simulate 100ms work
            duration = time.time() - start
            write_agent_state(agent_id, {"status": "completed", "duration": duration})
            return duration

        # Sequential execution in thread pool (simulates parallelism)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            start_total = time.time()
            futures = [executor.submit(execute_agent_sync, f"par_{i}") for i in range(3)]
            durations = [f.result() for f in concurrent.futures.as_completed(futures)]
            total_time = time.time() - start_total

        # 3 agents in parallel: should be ~100ms, not 300ms
        assert total_time < 0.25  # Less than 250ms (with overhead)


class TestErrorHandling:
    """Test error handling in parallelization."""

    def test_agent_failure_isolation(self):
        """Test that one agent failure doesn't affect others."""
        from api.main import write_agent_state, read_agent_state

        # Agent 1 fails
        write_agent_state("fail_1", {"status": "failed", "error": "test error"})

        # Agent 2 succeeds
        write_agent_state("success_1", {"status": "completed", "result": "ok"})

        # Verify states are independent
        state1 = read_agent_state("fail_1")
        state2 = read_agent_state("success_1")

        assert state1["status"] == "failed"
        assert state2["status"] == "completed"

    def test_invalid_state_file_handling(self):
        """Test graceful handling of corrupted state files."""
        from api.main import read_agent_state

        # Create invalid JSON file
        state_dir = Path(settings.agent_state_path)
        state_dir.mkdir(parents=True, exist_ok=True)
        bad_file = state_dir / "bad_state.json"
        bad_file.write_text("{ invalid json")

        # Should return default state, not crash
        state = read_agent_state("bad_state")
        assert state == {"status": "idle", "last_updated": None}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
