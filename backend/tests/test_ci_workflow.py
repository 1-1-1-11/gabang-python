from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUALITY_WORKFLOW = ROOT / ".github" / "workflows" / "quality.yml"


def test_quality_workflow_runs_project_gates():
    workflow = QUALITY_WORKFLOW.read_text(encoding="utf-8")

    assert "runs-on: windows-latest" in workflow
    assert 'python-version: "3.12"' in workflow
    assert 'node-version: "22"' in workflow
    assert "python -m pip install -r backend\\requirements.lock.txt" in workflow
    assert "npm ci" in workflow
    assert "npx playwright install chromium" in workflow
    assert "python -m pytest backend\\tests -q" in workflow
    assert "npm run build" in workflow
    assert "npm run test:e2e" in workflow
    assert "git diff-tree --check --no-commit-id --root -r HEAD" in workflow
    assert "4173" not in workflow
