import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from task_manager import add_task, delete_task, mark_done, filter_tasks, load_tasks, save_tasks

# Helper: vrati novu listu zadataka za test
@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "description": "Zadatak 1", "status": "todo"},
        {"id": 2, "description": "Zadatak 2", "status": "todo"},
    ]

def test_add_task(sample_tasks):
    add_task(sample_tasks, "Novi zadatak")
    assert len(sample_tasks) == 3
    assert sample_tasks[-1]["description"] == "Novi zadatak"
    assert sample_tasks[-1]["status"] == "todo"

def test_mark_done(sample_tasks):
    mark_done(sample_tasks, 1)
    assert sample_tasks[0]["status"] == "done"

def test_mark_done_invalid_id(sample_tasks, capsys):
    mark_done(sample_tasks, 99)  # nepostojeći ID
    captured = capsys.readouterr()
    assert "Nije pronađen zadatak" in captured.out

def test_delete_task(sample_tasks):
    delete_task(sample_tasks, 0)  # obrisati prvi zadatak
    assert len(sample_tasks) == 1
    assert sample_tasks[0]["id"] == 1  # ID-jevi se resetuju

def test_delete_task_invalid_index(sample_tasks, capsys):
    delete_task(sample_tasks, 99)  # nepostojeći index
    captured = capsys.readouterr()
    assert "Nevažeći broj zadatka" in captured.out

def test_filter_tasks(sample_tasks, capsys):
    # testirati da li filter prikazuje samo todo zadatke
    filter_tasks(sample_tasks, "todo")
    captured = capsys.readouterr()
    assert "Zadatak 1" in captured.out
    assert "Zadatak 2" in captured.out

def test_filter_tasks_empty(capsys):
    empty_list = []
    filter_tasks(empty_list, "todo")
    captured = capsys.readouterr()
    assert "Nema zadataka" in captured.out

def test_filter_tasks_done(sample_tasks, capsys):
    mark_done(sample_tasks, 1)
    filter_tasks(sample_tasks, "done")
    captured = capsys.readouterr()
    assert "Zadatak 1" in captured.out
    assert "Zadatak 2" not in captured.out
