# Initialize monorepo
mkdir personal-ai-hub && cd personal-ai-hub
npx create-next-app@latest frontend --typescript --eslint
python -m venv backend && source backend/bin/activate
mkdir contracts && cd contracts && npm init -y && npm install @openzeppelin/contracts hardhat
