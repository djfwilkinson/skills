import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "ledger.py"
SPEC = importlib.util.spec_from_file_location("orchestrated_run_ledger", SCRIPT)
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        ledger.HOME = self.root / "ledger"
        ledger.RUNS = ledger.HOME / "runs"
        ledger.PORT_FILE = ledger.HOME / "port"
        ledger.PID_FILE = ledger.HOME / "pid"
        ledger.INDEX = ledger.HOME / "index.html"
        ledger.ARCHIVE_CACHE.clear()
        ledger.RUNS.mkdir(parents=True)

        self.run = self.root / "project" / ".agent-runs" / "orchestrated-run" / "run-1"
        (self.run / "tickets").mkdir(parents=True)
        (self.run / "asks").mkdir()
        (self.run / "GOALS.md").write_text("## G-001\n\n### Status\nachieved\n", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def registration(self, **extra):
        path = ledger.run_file(self.run)[2]
        data = {"run": {"id": self.run.name, "name": self.run.name,
                        "project": "project", "dir": str(self.run), **extra}}
        ledger.write_json(path, data)
        return path

    def add_answered_ask(self, invalid_page=False):
        (self.run / "tickets" / "T-001-DIS.md").write_text(
            "---\nid: T-001-DIS\ntitle: Confirm wording\ntype: Discuss/Gather Inputs\n"
            "status: resolved\npresentation: answered\nmay_withdraw_on: []\n---\n",
            encoding="utf-8",
        )
        page = self.run / "asks" / "T-001-DIS.html"
        if invalid_page:
            page.write_bytes(b"\xff")
        else:
            page.write_text(
                'summary: "Confirm wording",\nwhy: "Judgement",\n'
                'presentedAt: "2026-10-22T08:00:00Z",',
                encoding="utf-8",
            )

    def test_complete_archives_existing_registration_and_preserves_history(self):
        self.add_answered_ask()
        path = self.registration()

        with mock.patch.object(ledger, "start") as start:
            ledger.complete(self.run)

        start.assert_called_once_with(show_url=False)
        data = ledger.read_json(path)
        self.assertEqual(data["run"]["dir"], str(self.run.resolve()))
        self.assertIn("archivedAt", data["run"])
        view = ledger.run_view(path.stem, data)
        self.assertEqual(view["history"][0]["action"], "Confirm wording")

    def test_complete_recreates_a_missing_registration_as_archived(self):
        path = ledger.run_file(self.run)[2]

        with mock.patch.object(ledger, "start"):
            ledger.complete(self.run)

        data = ledger.read_json(path)
        self.assertEqual(data["run"]["dir"], str(self.run.resolve()))
        self.assertIn("archivedAt", data["run"])

    def test_register_clears_archive_marker(self):
        path = self.registration(archivedAt="2026-10-22T08:00:00Z")

        with (
            mock.patch.object(ledger, "start") as start,
            mock.patch.object(ledger, "saved_port", return_value=47400),
            mock.patch("builtins.print"),
        ):
            ledger.register(self.run)

        start.assert_called_once_with(show_url=False)
        self.assertNotIn("archivedAt", ledger.read_json(path)["run"])

    def test_invalid_historical_page_does_not_break_archived_view(self):
        self.add_answered_ask(invalid_page=True)
        path = self.registration(archivedAt="2026-10-22T08:00:00Z")

        view = ledger.run_view(path.stem, ledger.read_json(path))

        self.assertEqual(view["history"][0]["id"], "T-001-DIS")
        self.assertFalse(view["history"][0]["hasPage"])

    def test_answered_ask_remains_in_active_history(self):
        self.add_answered_ask()
        path = self.registration()

        view = ledger.run_view(path.stem, ledger.read_json(path))

        self.assertEqual(view["history"][0]["id"], "T-001-DIS")

    def test_archived_cache_refreshes_when_an_ask_changes(self):
        self.add_answered_ask()
        path = self.registration(archivedAt="2026-10-22T08:00:00Z")
        data = ledger.read_json(path)
        first = ledger.run_view(path.stem, data)
        (self.run / "asks" / "T-001-DIS.html").write_text(
            'summary: "Revised wording",\nwhy: "Judgement",\n'
            'presentedAt: "2026-10-22T08:00:00Z",',
            encoding="utf-8",
        )

        second = ledger.run_view(path.stem, data)

        self.assertEqual(first["history"][0]["action"], "Confirm wording")
        self.assertEqual(second["history"][0]["action"], "Revised wording")

    def test_invalid_ticket_and_goals_do_not_break_run_view(self):
        (self.run / "tickets" / "T-001-DIS.md").write_bytes(b"\xff")
        (self.run / "GOALS.md").write_bytes(b"\xff")
        path = self.registration(archivedAt="2026-10-22T08:00:00Z")

        view = ledger.run_view(path.stem, ledger.read_json(path))

        self.assertEqual(view["asks"], [])
        self.assertFalse(view["run"]["looksComplete"])

    def test_missing_run_directory_keeps_registration_visible(self):
        missing = self.root / "moved-run"
        data = {"run": {"id": "moved-run", "dir": str(missing),
                        "archivedAt": "2026-10-22T08:00:00Z"}}

        view = ledger.run_view("project--moved-run", data)

        self.assertTrue(view["run"]["dirMissing"])
        self.assertEqual(view["history"], [])

    def test_start_stops_if_older_server_survives(self):
        ledger.PID_FILE.write_text("123", encoding="utf-8")
        ledger.INDEX.write_text(
            '<meta name="ledger-version" content="1">old index',
            encoding="utf-8",
        )
        with (
            mock.patch.object(ledger, "running_version", return_value=ledger.VERSION - 1),
            mock.patch.object(ledger, "wait_for", return_value=False),
            mock.patch.object(ledger.os, "kill"),
        ):
            with self.assertRaises(SystemExit):
                ledger.start(show_url=False)
        self.assertIn("old index", ledger.INDEX.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
