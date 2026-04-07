#!/usr/bin/env python3
"""
Agent Runner — Orquestador de agentes IA locales.

Ejecuta 2-3 agentes en paralelo, persiste estado en Obsidian vault.
Integración con Claude SDK (CLAUDE_API_KEY en .env).
"""

import json
import os
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.config import settings

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"{settings.agent_logs_path}/agent-runner.log")
    ]
)
logger = logging.getLogger("AgentRunner")


@dataclass
class ExecutionResult:
    """Result of an agent execution."""
    agent_name: str
    status: str  # "success", "error", "queued"
    output: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class AgentRunner:
    """Orchestrates parallel execution of agents with Obsidian vault persistence."""

    def __init__(self, agents_config_path: str = "agents.json"):
        """Initialize agent runner."""
        self.agents_config_path = agents_config_path
        self.agents_config: Dict[str, Any] = self._load_agents_config()
        self.max_parallel = self.agents_config.get("concurrency", {}).get("max_parallel", 3)
        self.vault_path = Path(settings.vault_path)
        self.agent_state_path = Path(settings.agent_state_path)
        self.agent_logs_path = Path(settings.agent_logs_path)

        # Create directories
        self.agent_state_path.mkdir(parents=True, exist_ok=True)
        self.agent_logs_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"[OK] AgentRunner initialized (max_parallel: {self.max_parallel})")

    def _load_agents_config(self) -> Dict[str, Any]:
        """Load agents configuration from JSON."""
        try:
            with open(self.agents_config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"[ERROR] agents.json not found at {self.agents_config_path}")
            return {"agents": {}, "concurrency": {"max_parallel": 3}}

    def get_agent_config(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific agent."""
        return self.agents_config.get("agents", {}).get(agent_name)

    def read_agent_state(self, agent_name: str) -> Dict[str, Any]:
        """Read agent state from Obsidian vault."""
        state_file = self.agent_state_path / f"{agent_name}.json"
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading state for {agent_name}: {e}")

        return {
            "agent_name": agent_name,
            "status": "idle",
            "last_execution": None,
            "last_output": None,
        }

    def write_agent_state(self, agent_name: str, state: Dict[str, Any]) -> None:
        """Write agent state to Obsidian vault."""
        state_file = self.agent_state_path / f"{agent_name}.json"
        state["timestamp"] = datetime.now().isoformat()

        try:
            with open(state_file, "w") as f:
                json.dump(state, f, indent=2)
            logger.debug(f"💾 State saved for {agent_name}")
        except Exception as e:
            logger.error(f"Error writing state for {agent_name}: {e}")

    def log_execution(self, result: ExecutionResult) -> None:
        """Log execution to agent logs."""
        log_file = self.agent_logs_path / f"{result.agent_name}_executions.log"

        try:
            with open(log_file, "a") as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"Timestamp: {result.timestamp}\n")
                f.write(f"Status: {result.status}\n")
                f.write(f"Duration: {result.duration_seconds:.2f}s\n")
                if result.output:
                    f.write(f"\nOutput:\n{result.output}\n")
                if result.error:
                    f.write(f"\nError:\n{result.error}\n")
        except Exception as e:
            logger.error(f"Error logging execution for {result.agent_name}: {e}")

    async def execute_agent(self, agent_name: str, prompt: str) -> ExecutionResult:
        """
        Execute a single agent with a prompt.

        Integration point: Replace with Claude API call when CLAUDE_API_KEY available.
        """
        start_time = datetime.now()
        result = ExecutionResult(
            agent_name=agent_name,
            status="pending",
            timestamp=start_time.isoformat(),
        )

        try:
            # Update state: executing
            self.write_agent_state(agent_name, {
                "status": "executing",
                "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
                "started_at": start_time.isoformat(),
            })

            logger.info(f"[RUN]  Executing {agent_name}...")

            # === INTEGRATION POINT: Claude API ===
            # When CLAUDE_API_KEY is available in .env:
            # from anthropic import Anthropic
            # client = Anthropic(api_key=settings.claude_api_key)
            # agent_config = self.get_agent_config(agent_name)
            # response = client.messages.create(
            #     model=agent_config["model"],  # "opus" or "sonnet"
            #     max_tokens=agent_config.get("max_tokens", 4096),
            #     system=f"You are {agent_config['role']}. {system_prompt}",
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # result.output = response.content[0].text

            # PLACEHOLDER: Simulated response
            result.status = "success"
            result.output = f"[PLACEHOLDER] {agent_name} would execute with: {prompt[:100]}...\n\nNote: Connect CLAUDE_API_KEY in .env to enable real execution."
            logger.info(f"[OK] {agent_name} completed (placeholder mode)")

        except Exception as e:
            result.status = "error"
            result.error = str(e)
            logger.error(f"[ERROR] {agent_name} failed: {e}")

        finally:
            # Calculate duration
            end_time = datetime.now()
            result.duration_seconds = (end_time - start_time).total_seconds()

            # Update state: completed
            self.write_agent_state(agent_name, {
                "status": result.status,
                "last_execution": end_time.isoformat(),
                "last_output": result.output[:200] if result.output else None,
                "duration_seconds": result.duration_seconds,
            })

            # Log execution
            self.log_execution(result)

        return result

    async def execute_parallel(
        self,
        agent_names: List[str],
        prompts: Dict[str, str],
        max_parallel: Optional[int] = None,
    ) -> Dict[str, ExecutionResult]:
        """
        Execute multiple agents in parallel.

        Args:
            agent_names: List of agent names to execute
            prompts: Dict mapping agent_name -> prompt
            max_parallel: Override max parallel agents (default from config)

        Returns:
            Dict mapping agent_name -> ExecutionResult
        """
        max_parallel = max_parallel or self.max_parallel

        # Validate inputs
        if len(agent_names) > max_parallel:
            logger.warning(
                f"[WARN] Requested {len(agent_names)} agents, but max_parallel is {max_parallel}. "
                f"Executing {max_parallel} first."
            )
            agent_names = agent_names[:max_parallel]

        logger.info(f"[START] Starting {len(agent_names)} agents in parallel (max_parallel: {max_parallel})")

        tasks = [
            self.execute_agent(agent_name, prompts.get(agent_name, ""))
            for agent_name in agent_names
        ]

        results = await asyncio.gather(*tasks, return_exceptions=False)

        return {result.agent_name: result for result in results}

    def list_agents(self) -> List[str]:
        """List all configured agents."""
        return list(self.agents_config.get("agents", {}).keys())

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Get current state of all agents."""
        states = {}
        for agent_name in self.list_agents():
            states[agent_name] = self.read_agent_state(agent_name)
        return states


async def main():
    """CLI entry point for agent runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Runner — Orquestador de agentes IA")
    parser.add_argument("--list", action="store_true", help="List all agents")
    parser.add_argument("--state", type=str, help="Get state of a specific agent")
    parser.add_argument("--execute", type=str, help="Execute a specific agent (comma-separated names)")
    parser.add_argument("--prompt", type=str, default="Hola, resume tu rol", help="Prompt for execution")
    parser.add_argument("--parallel", type=int, help="Override max parallel agents")

    args = parser.parse_args()

    runner = AgentRunner()

    if args.list:
        agents = runner.list_agents()
        logger.info(f"[LIST] Configured agents ({len(agents)}):")
        for agent in agents:
            config = runner.get_agent_config(agent)
            logger.info(f"   - {agent}: {config['role']} ({config['model']})")

    elif args.state:
        state = runner.read_agent_state(args.state)
        logger.info(f"[STATUS] State for {args.state}:\n{json.dumps(state, indent=2)}")

    elif args.execute:
        agent_names = [a.strip() for a in args.execute.split(",")]
        prompts = {agent: args.prompt for agent in agent_names}

        logger.info(f"Executing {len(agent_names)} agent(s)...")
        results = await runner.execute_parallel(
            agent_names,
            prompts,
            max_parallel=args.parallel,
        )

        logger.info("\n[STATUS] Execution Results:")
        for agent_name, result in results.items():
            logger.info(f"\n{agent_name}:")
            logger.info(f"  Status: {result.status}")
            logger.info(f"  Duration: {result.duration_seconds:.2f}s")
            if result.output:
                logger.info(f"  Output: {result.output[:100]}...")

    else:
        logger.info("Use --help for usage information")
        runner_instance = AgentRunner()
        states = runner_instance.get_all_states()
        logger.info(f"[OK] Agent Runner ready. {len(states)} agents available.")


if __name__ == "__main__":
    asyncio.run(main())
