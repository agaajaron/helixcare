from llama_index.core.tools import FunctionTool

PROVIDERS = [
  {"name":"City Imaging Center","network":"PPO-Blue-2025","zip":"80301","modality":"MRI"},
  {"name":"FastScan Radiology","network":"PPO-Blue-2025","zip":"80202","modality":"MRI"},
]

def find_in_network(modality:str, network:str, near_zip:str):
    return [p for p in PROVIDERS if p["modality"]==modality and p["network"]==network]

PROVIDER_TOOL = FunctionTool.from_defaults(
    fn=find_in_network, name="find_in_network",
    description="Find in-network providers for a modality (synthetic)"
)
