
from langchain.chains import ConstitutionalChain
from local_llm import FineTunedModel
import mcp_integration

class PersonalAI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.llm = FineTunedModel.load_for_user(user_id)
        self.knowledge_base = KnowledgeBase(user_id)
        self.constitution = [
            "Prioritize user privacy above all else",
            "Never store sensitive data without encryption",
            "Verify information from external sources"
        ]
   
    async def process_query(self, query: str) -> str:
        # Step 1: Context retrieval
        context = await self.knowledge_base.retrieve_relevant_context(query)
       
        # Step 2: Local processing
        local_result = self.llm.generate(
            prompt=query,
            context=context
        )
       
        # Step 3: MCP augmentation
        if self.requires_external_data(local_result):
            mcp_query = self.build_mcp_query(local_result)
            external_data = await mcp_integration.query(mcp_query)
            return self.llm.refine(local_result, external_data)
       
        # Step 4: Constitutional compliance
        chain = ConstitutionalChain(
            base_chain=self.llm.chain,
            constitutional_principles=self.constitution
        )
        return chain.run(input=local_result)
   
    def build_mcp_query(self, local_result):
        return {
            "user_id": self.user_id,
            "context": local_result.context_gap_analysis(),
            "capabilities": ["web_search", "cross_ai_verification"]
        } 
