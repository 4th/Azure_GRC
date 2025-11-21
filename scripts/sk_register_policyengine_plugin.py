#!/usr/bin/env python
"""
Example: Register PolicyEngine as a Semantic Kernel plugin and run a simple call.
This assumes you have sk_policyengine_plugin.py and SK installed.
"""

import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


from agents.tools.sk_policyengine_plugin import PolicyEnginePlugin  # adjust import


async def main() -> None:
    kernel = Kernel()

    # Example Azure OpenAI config – replace with your own env vars
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        )
    )

    plugin = PolicyEnginePlugin(
        base_url=os.environ.get("POLICYENGINE_URL", "http://127.0.0.1:8080")
    )
    kernel.add_plugin(plugin, plugin_name="policyengine")

    func = kernel.get_function("policyengine", "evaluate_profile")  # depends on your plugin
    result = await func.invoke_async(
        profile_ref="iso_42001-global@1.2.0",
        context={"system_name": "Demo System"},
    )

    print("[sk-demo] Result from PolicyEngine via SK:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
