import subprocess

def run_git(msg):
    subprocess.run(['git', 'commit', '-m', msg], check=True)

subprocess.run(['git', 'add', 'backend/requirements/base.txt'])
run_git('chore(backend): add langchain and langgraph dependencies')

subprocess.run(['git', 'add', 'backend/app/core/config.py'])
run_git('chore(backend): add OPENAI_API_KEY to config')

subprocess.run(['git', 'add', 'backend/app/agents/__init__.py'])
run_git('chore(backend): initialize agents package')

subprocess.run(['git', 'add', 'backend/app/agents/tools.py'])
run_git('feat(backend): implement agent database tools')

subprocess.run(['git', 'add', 'backend/app/agents/state.py'])
run_git('feat(backend): define langgraph state schema')

subprocess.run(['git', 'add', 'backend/app/agents/graph.py'])
run_git('feat(backend): implement langgraph agent workflow')

subprocess.run(['git', 'add', 'backend/app/agents/service.py'])
run_git('feat(backend): create agent service wrapper')

subprocess.run(['git', 'add', 'backend/app/schemas/chat.py'])
run_git('feat(backend): define chat request schemas')

subprocess.run(['git', 'add', 'backend/app/api/v1/endpoints/assistant.py'])
run_git('feat(backend): expose AI assistant REST endpoint')

subprocess.run(['git', 'add', 'backend/app/api/v1/router.py'])
run_git('chore(backend): register assistant router')

content = open('frontend/pages/5_AI_Assistant.py', encoding='utf-8').read()
layout = content.split('if "chat_history"')[0]
open('frontend/pages/5_AI_Assistant.py', 'w', encoding='utf-8').write(layout)
subprocess.run(['git', 'add', 'frontend/pages/5_AI_Assistant.py'])
run_git('feat(frontend): create AI Assistant Streamlit page layout')

layout2 = layout + 'if "chat_history"' + content.split('if "chat_history"')[1].split('if prompt :=')[0]
open('frontend/pages/5_AI_Assistant.py', 'w', encoding='utf-8').write(layout2)
subprocess.run(['git', 'add', 'frontend/pages/5_AI_Assistant.py'])
run_git('feat(frontend): implement chat history state')

open('frontend/pages/5_AI_Assistant.py', 'w', encoding='utf-8').write(content)
subprocess.run(['git', 'add', 'frontend/pages/5_AI_Assistant.py'])
run_git('feat(frontend): implement agent chat interaction logic')

readme = open('README.md', encoding='utf-8').read()
readme1 = readme.replace('- [ ] AI Agents', '- [x] AI Agents')
open('README.md', 'w', encoding='utf-8').write(readme1)
subprocess.run(['git', 'add', 'README.md'])
run_git('docs: check off AI Agents in roadmap')

readme2 = readme1.replace('- [ ] LangGraph Workflows', '- [x] LangGraph Workflows')
open('README.md', 'w', encoding='utf-8').write(readme2)
subprocess.run(['git', 'add', 'README.md'])
run_git('docs: check off LangGraph Workflows in roadmap')
