import typer

from backend.adapters.model_client import GeminiModelClient
from backend.core.runners.main import Runner
from backend.storage.main import StorageManager

app = typer.Typer()


@app.command()
def run_suite(suite_path: str):
    """
    Run a test suite against the model.
    """
    model_client = GeminiModelClient()
    runner = Runner(model_client=model_client)
    storage_manager = StorageManager()

    run_result = runner.run_suite(suite_path=suite_path)
    storage_manager.save_run(run_result=run_result)

    print(f"Run completed. Run ID: {run_result.id}")


if __name__ == "__main__":
    app()