"""脚本的可观察不变量；不把检索成功当作前端设计质量证明。"""
import copy
import io
import json
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from profile_project import profile
from recommend import recommend, load_catalog
from fetch_reference import fetch, validate_payload, validate_url, OfficialRedirect
from check_delivery import check


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def test_detects_stack_without_exposing_commands_or_credentials(self):
        self.write("package.json", json.dumps({
            "dependencies": {"react": "^19.0.0", "motion": "^12.0.0",
                             "private": "https://user:SECRET_SENTINEL@example.org/pkg"},
            "scripts": {"build": "echo SECRET_SENTINEL"}, "packageManager": "bun@1.2.0"}))
        self.write("components.json", json.dumps({"style": "new-york", "registries": {
            "@private": "https://example.org/r?token=SECRET_SENTINEL"}}))
        self.write("src/index.css", ":root { --background: red; --radius: 8px; }")
        self.write("src/components/calendar.tsx", "export const Calendar = null")
        self.write(".env.local", "SECRET_SENTINEL")
        self.write("bun.lock", "SECRET_SENTINEL")
        result = profile(self.root)
        self.assertEqual(result["frameworks"], ["react"])
        self.assertEqual(result["packages"][0]["available_checks"], ["build"])
        self.assertEqual(result["motion_packages"], ["motion"])
        self.assertEqual(result["styles"][0]["token_names"], ["--background", "--radius"])
        self.assertEqual(result["components_configs"][0]["registry_names"], ["@private"])
        self.assertNotIn("SECRET_SENTINEL", json.dumps(result))

    def test_skip_generated_hidden_and_symlinked_paths(self):
        self.write("node_modules/dep/package.json", '{"dependencies":{"vue":"3"}}')
        self.write(".cache/pkg/package.json", '{"dependencies":{"svelte":"5"}}')
        self.write("src/main.templ", "package main")
        (self.root / "linked").symlink_to(self.root / "node_modules", target_is_directory=True)
        (self.root / "package.json").symlink_to(self.root / "node_modules/dep/package.json")
        result = profile(self.root)
        self.assertEqual(result["frameworks"], ["go-templ"])
        self.assertEqual(result["packages"], [])

    def test_budget_and_depth_are_bounded(self):
        for i in range(8):
            self.write(f"{i}.tsx", "export default null")
        self.write("deep/child/component.vue", "<template/>")
        result = profile(self.root, max_files=3)
        self.assertTrue(result["scan"]["truncated"])
        self.assertEqual(result["scan"]["files_seen"], 3)
        self.assertEqual(len(result["component_file_candidates"]), 3)
        self.assertNotIn("deep/child/component.vue", profile(self.root, max_depth=0)["component_file_candidates"])

    def test_malformed_optional_fields_do_not_abort_scan(self):
        self.write("package.json", '{"scripts":null,"dependencies":{"react":"19"}}')
        self.write("components.json", '{"registries":42}')
        self.write("broken/package.json", "{invalid")
        result = profile(self.root)
        self.assertEqual(result["frameworks"], ["react"])
        self.assertEqual(len(result["warnings"]), 3)

    def test_monorepo_does_not_hide_multiple_frameworks(self):
        self.write("apps/a/package.json", '{"dependencies":{"react":"19"}}')
        self.write("apps/b/package.json", '{"dependencies":{"vue":"3"}}')
        result = profile(self.root)
        self.assertEqual(result["frameworks"], ["react", "vue"])
        with self.assertRaises(ValueError):
            recommend("日期范围", "auto", profile_data=result)

    def test_frameworks_and_package_managers_are_not_fixed(self):
        cases = [("react", "react", "npm@10.0.0"), ("next", "react", "pnpm@9.0.0"),
                 ("vue", "vue", "yarn@4.0.0"), ("nuxt", "vue", "bun@1.2.0"),
                 ("svelte", "svelte", "npm@10.0.0"), ("@angular/core", "angular", "pnpm@9.0.0")]
        for index, (dependency, framework, manager) in enumerate(cases):
            with self.subTest(dependency=dependency):
                folder = f"arbitrary-layout-{index}"
                self.write(folder + "/package.json", json.dumps({
                    "dependencies": {dependency: "*"}, "packageManager": manager}))
                result = profile(self.root / folder)
                self.assertEqual(result["frameworks"], [framework])
                self.assertEqual(result["packages"][0]["package_manager"], manager)


class RecommendationTests(unittest.TestCase):
    def test_routing_scenarios(self):
        cases = json.loads((ROOT / "evals/routing-cases.json").read_text(encoding="utf-8"))["cases"]
        for case in cases:
            with self.subTest(case=case["id"]):
                result = recommend(case["query"], case["framework"],
                                   intents=case.get("explicit_intents"),
                                   profile_data=case.get("profile"),
                                   no_new_dependencies=case.get("no_new_dependencies", False),
                                   motion=case.get("motion", 1))
                candidates = result["candidates"]
                sources = {c["source"] for c in candidates}
                self.assertEqual(set(result["intents"]), set(case["intents"]))
                if case.get("empty"):
                    self.assertEqual(candidates, [])
                if "top_source" in case:
                    self.assertTrue(candidates)
                    self.assertEqual(candidates[0]["source"], case["top_source"])
                if "top_name" in case:
                    self.assertEqual(candidates[0]["name"], case["top_name"])
                self.assertTrue(set(case.get("include_sources", [])) <= sources)
                self.assertFalse(set(case.get("exclude_sources", [])) & sources)
                if "allowed_sources" in case:
                    self.assertTrue(sources <= set(case["allowed_sources"]))
                for candidate in candidates:
                    self.assertIsNone(candidate["install_command"])
                    self.assertFalse(candidate["api_verified"])
                    if "use" in case:
                        self.assertEqual(candidate["use"], case["use"])

    def test_auto_uses_only_unambiguous_framework(self):
        result = recommend("命令面板", "auto", profile_data={"frameworks": ["vue"]})
        self.assertEqual(result["candidates"][0]["source"], "nxui")
        for frameworks in ([], ["react", "vue"], "react", None, [[]]):
            with self.subTest(frameworks=frameworks), self.assertRaises(ValueError):
                recommend("命令面板", "auto", profile_data={"frameworks": frameworks})

    def test_bad_framework_intent_and_profile_report_errors(self):
        for kwargs in ({"framework": "invented"}, {"intents": ["invented"]},
                       {"profile_data": []}, {"profile_data": {"packages": [None]}}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                recommend("表单", **kwargs)

    def test_framework_filter_covers_all_returned_candidates(self):
        resources, _, intents = load_catalog()
        for framework in ("react", "vue", "svelte", "angular", "go-templ", "html"):
            result = recommend("", framework, intents=[i["id"] for i in intents], limit=100, motion=2)
            for candidate in result["candidates"]:
                frameworks = resources[candidate["source"]]["frameworks"]
                self.assertTrue(framework in frameworks or frameworks == ["inspiration"])

    def test_motion_budget_and_existing_runtime_affect_candidates(self):
        low = recommend("进度", "react", limit=25, motion=1)
        high = recommend("进度", "react", limit=25, motion=2)
        self.assertNotIn("beam", {c["source"] for c in low["candidates"]})
        self.assertIn("beam", {c["source"] for c in high["candidates"]})
        existing = recommend("AI 对话", "react", profile_data={"packages": [
            {"dependencies": {"@assistant-ui/react": "0.12"}}]})
        self.assertIn("@assistant-ui/react", " ".join(existing["candidates"][0]["reasons"]))

    def test_catalog_references_and_coverage(self):
        resources, components, intents = load_catalog()
        self.assertEqual(len(resources), 22)
        self.assertEqual({c["source"] for c in components}, set(resources))
        self.assertEqual(len({c["id"] for c in components}), len(components))
        known_intents = {i["id"] for i in intents}
        self.assertEqual({i for c in components for i in c["intents"]}, known_intents)
        for resource in resources.values():
            self.assertTrue((ROOT / resource["evidence"]).is_file())
            self.assertFalse(resource["connection_tested"])


class DownloadTests(unittest.TestCase):
    def test_rejects_html_fallback_for_text_or_json(self):
        for content, mime in ((b"<html>home</html>", "text/plain"),
                              (b"welcome", "text/html")):
            for kind in ("text", "json", "registry"):
                with self.subTest(kind=kind, mime=mime), self.assertRaises(ValueError):
                    validate_payload(content, mime, kind)

    def test_registry_accepts_inline_jsx_but_requires_source_content(self):
        body = json.dumps({"files": [{"content": "export default () => <html/>"}]}).encode()
        self.assertEqual(validate_payload(body, "application/json", "registry")["file_count"], 1)
        for value in ({"files": []}, {"files": [{"path": "remote.tsx"}]}, {"items": []}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_payload(json.dumps(value).encode(), "application/json", "registry")

    def test_empty_invalid_encoding_and_invalid_json_are_rejected(self):
        for body, kind in ((b" ", "text"), (b"\xff", "text"), (b"{broken", "json")):
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_payload(body, "text/plain", kind)

    def test_explicit_page_mode_accepts_html_as_unreviewed_material(self):
        self.assertEqual(validate_payload(b"<html>docs</html>", "text/html", "page"),
                         {"format": "html-page"})

    def test_untrusted_hosts_schemes_ports_and_credentials_rejected(self):
        hosts = {"lab.moumen.dev"}
        validate_url("https://lab.moumen.dev/llms.txt", hosts)
        for url in ("http://lab.moumen.dev/x", "https://evil.example/x",
                    "https://lab.moumen.dev:444/x", "https://user:pass@lab.moumen.dev/x"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url, hosts)

    def test_redirects_cannot_escape_host_or_lead_to_login(self):
        handler = OfficialRedirect({"lab.moumen.dev"})
        request = urllib.request.Request("https://lab.moumen.dev/llms.txt")
        for url in ("https://evil.example/x", "https://lab.moumen.dev/login?next=docs"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                handler.redirect_request(request, None, 302, "redirect", {}, url)

    def test_download_records_bytes_hash_and_does_not_execute(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "reference.md"
            response = io.BytesIO(b"# public docs\n")
            response.url = "https://lab.moumen.dev/llms.txt"
            response.headers = {"Content-Type": "text/plain"}
            with patch("fetch_reference.urllib.request.build_opener") as opener:
                opener.return_value.open.return_value = response
                result = fetch("moumen", None, "text", output)
            self.assertEqual(output.read_bytes(), b"# public docs\n")
            self.assertEqual(result["status"], "downloaded_unreviewed")
            self.assertFalse(result["executed"])
            self.assertEqual(len(result["sha256"]), 64)

    def test_existing_file_is_not_overwritten_or_requested(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "existing"
            output.write_text("preserve")
            with patch("fetch_reference.urllib.request.build_opener") as opener:
                with self.assertRaises(ValueError):
                    fetch("moumen", None, "text", output)
                opener.assert_not_called()
            self.assertEqual(output.read_text(), "preserve")

    def test_oversized_download_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "too-large"
            response = io.BytesIO(b"12345")
            response.url = "https://lab.moumen.dev/llms.txt"
            response.headers = {"Content-Type": "text/plain"}
            with patch("fetch_reference.urllib.request.build_opener") as opener:
                opener.return_value.open.return_value = response
                with self.assertRaises(ValueError):
                    fetch("moumen", None, "text", output, max_bytes=4)
            self.assertFalse(output.exists())


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "evidence"
        self.root.mkdir()
        (self.root / "check.log").write_text("Actual check result for fixture\n")
        self.report = {"schema_version": 1, "requirements": [{"id": "flow"}],
                       "checks": [{"id": "interaction", "requirements": ["flow"], "status": "pass",
                                   "observation": "Fixture observed.", "evidence": ["check.log"]}]}

    def test_complete_record_is_not_named_product_pass(self):
        result = check(self.report, self.root)
        self.assertEqual(result["status"], "evidence_record_complete")
        self.assertIn("不等于", result["limit"])

    def test_missing_empty_and_outside_evidence_are_invalid(self):
        (self.root / "empty.log").touch()
        outside = self.root.parent / "outside.log"
        outside.write_text("outside")
        (self.root / "linked.log").symlink_to(outside)
        for evidence in ([], ["missing.log"], ["empty.log"], ["../outside.log"],
                         [str(outside)], ["linked.log"]):
            with self.subTest(evidence=evidence):
                self.report["checks"][0]["evidence"] = evidence
                self.assertEqual(check(self.report, self.root)["status"], "invalid")

    def test_failed_and_unverified_results_cannot_be_complete(self):
        for state, expected in (("fail", "has_failures"), ("unverified", "incomplete")):
            self.report["checks"][0]["status"] = state
            self.report["checks"][0]["evidence"] = []
            self.assertEqual(check(self.report, self.root)["status"], expected)

    def test_required_checks_cannot_all_be_not_applicable(self):
        self.report["checks"][0]["status"] = "not-applicable"
        self.assertEqual(check(self.report, self.root)["status"], "invalid")
        self.report["requirements"][0]["required"] = False
        self.assertEqual(check(self.report, self.root)["status"], "evidence_record_complete")

    def test_uncovered_and_unknown_requirement_are_invalid(self):
        self.report["requirements"].append({"id": "mobile"})
        self.assertEqual(check(self.report, self.root)["status"], "invalid")
        self.report["checks"][0]["requirements"] = ["invented"]
        self.assertEqual(check(self.report, self.root)["status"], "invalid")

    def test_malformed_fields_and_duplicate_ids_are_invalid(self):
        variants = [[], {}, {"schema_version": 1, "requirements": [None], "checks": [None]}]
        for field, value in (("status", []), ("requirements", [{}]), ("evidence", [None]),
                             ("id", {}), ("observation", None)):
            report = copy.deepcopy(self.report)
            report["checks"][0][field] = value
            variants.append(report)
        duplicate = copy.deepcopy(self.report)
        duplicate["checks"].append(copy.deepcopy(duplicate["checks"][0]))
        variants.append(duplicate)
        for report in variants:
            with self.subTest(report=report):
                self.assertEqual(check(report, self.root)["status"], "invalid")

    def test_template_honestly_starts_incomplete(self):
        template = json.loads((ROOT / "templates/delivery-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(check(template, self.root)["status"], "incomplete")


if __name__ == "__main__":
    unittest.main()
