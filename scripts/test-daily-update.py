#!/usr/bin/env python3
"""Exercise validation with real Jujutsu repositories and actual publication files."""
import importlib.util
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import tempfile
import sqlite3
import subprocess
import threading
import unittest

os.environ.setdefault('AI_SITE_USER_AGENT', 'site-update-test-agent')

spec = importlib.util.spec_from_file_location('daily_update', Path(__file__).with_name('daily-update.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class CheckpointInventoryTests(unittest.TestCase):
    def test_existing_checkpoint_discovers_new_inventory_sources(self):
        previous = {'omp': 'same', 'agents': 'same'}
        current = {**previous, 'cli': '1', 'mcps': '2', 'hooks': '3'}
        self.assertEqual(sync.changed_sources(previous, current), ['cli', 'hooks', 'mcps'])

    def test_bootstrap_does_not_republish_archived_skills(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'
            site = root / 'site'
            site.mkdir()
            (site / 'main.js').write_text("const paths = {'active': 'skills/active/SKILL.md'};")
            for name in ('active', 'archived'):
                (source / 'skills' / name).mkdir(parents=True)
                (source / 'skills' / name / 'SKILL.md').write_text('current')
                (site / 'skills' / name).mkdir(parents=True)
                (site / 'skills' / name / 'SKILL.md').write_text('old')
            changed = sync.bootstrap_sources({'skills/active': '1', 'skills/archived': '2'}, source, site)
            self.assertIn('skills/active', changed)
            self.assertNotIn('skills/archived', changed)

    def test_source_tree_detects_changes_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'snapshot'
            source.mkdir()
            file = source / 'source.json'
            file.write_text('first')
            before = sync.source_tree(source)
            file.write_text('second')
            self.assertNotEqual(before, sync.source_tree(source))
            (source / 'link').symlink_to(file)
            with self.assertRaisesRegex(RuntimeError, 'Symlink'):
                sync.source_tree(source)

    def test_jj_http_uses_private_user_agent(self):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                received.append(self.headers.get('User-Agent'))
                self.send_response(404)
                self.end_headers()

            def log_message(self, *args):
                pass

        with tempfile.TemporaryDirectory() as temporary, HTTPServer(('127.0.0.1', 0), Handler) as server:
            subprocess.run(['jj', 'git', 'init', '--colocate', temporary], check=True, capture_output=True)
            subprocess.run(['git', 'remote', 'add', 'probe',
                            f'http://127.0.0.1:{server.server_port}/test'],
                           cwd=temporary, check=True, capture_output=True)
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            try:
                with self.assertRaises(RuntimeError):
                    sync.jj(Path(temporary), 'git', 'fetch', '--remote', 'probe')
            finally:
                server.shutdown()
                thread.join()
            self.assertEqual(received, [sync.UA])


class ModelRankingTests(unittest.TestCase):
    def test_usage_aggregates_seven_days_and_aliases(self):
        current = sync.dt.datetime(2026, 10, 27, 16, tzinfo=sync.dt.timezone.utc)
        def day(date, rows):
            return {'date': date, 'total': sum(value for _, value in rows),
                    'breakdown': [{'name': name, 'tokens': {'total': value}} for name, value in rows]}
        payload = {'schemaVersion': 1, 'start': '2026-10-20', 'end': '2026-10-27',
                   'updatedAt': '2026-10-27T15:00:00Z',
                   'providers': [
                       {'daily': [day('2026-10-20', [('gpt-old', 999)]),
                                  day('2026-10-21', [('anthropic/claude-opus-5-5', 10),
                                                     ('gpt-6.1-sol', 20)])]},
                       {'daily': [day('2026-10-27', [('claude-5.5-opus', 5), ('gpt-6-astra', 7),
                                                     ('gpt-6-luna', 4)])]},
                   ]}
        snapshot = sync.usage_snapshot(payload, current)
        self.assertEqual(snapshot['totals'], {'claude-5.5-opus': 15, 'gpt-6.1-sol': 20,
                                              'gpt-6-astra': 7, 'gpt-6-luna': 4})
        payload['providers'][1]['daily'][0]['total'] += 1
        with self.assertRaisesRegex(ValueError, 'incomplete model attribution'):
            sync.usage_snapshot(payload, current)
        payload['providers'][1]['daily'][0]['total'] -= 1
        with self.assertRaisesRegex(ValueError, 'stale'):
            sync.usage_snapshot(payload, current + sync.dt.timedelta(days=3))

    def test_malformed_api_shapes_are_rejected(self):
        current = sync.dt.datetime(2026, 10, 27, 16, tzinfo=sync.dt.timezone.utc)
        valid = {'schemaVersion': 1, 'start': '2026-10-20', 'end': '2026-10-27',
                 'updatedAt': '2026-10-27T15:00:00Z', 'providers': []}
        for payload in (None, [], {**valid, 'updatedAt': None}, {**valid, 'providers': [None]}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                sync.usage_snapshot(payload, current)

    def test_consecutive_snapshots_and_same_day_reruns(self):
        order = ['alpha', 'beta', 'gamma', 'delta']
        first = {'date': '2026-10-26', 'totals': {'alpha': 100, 'beta': 120, 'gamma': 80,
                                                   'delta': 10, 'epsilon': 20}}
        second = {'date': '2026-10-27', 'totals': {'alpha': 100, 'beta': 120, 'gamma': 80,
                                                    'delta': 10, 'epsilon': 20}}
        state = sync.advance_model_state(first, None)
        self.assertEqual(sync.ranked_models(first, state['previous'], order), order)
        state = sync.advance_model_state(first, state)
        self.assertIsNone(state['previous'])
        state = sync.advance_model_state(second, state)
        self.assertEqual(sync.ranked_models(second, state['previous'], order),
                         ['beta', 'alpha', 'gamma', 'epsilon'])
        second['totals']['beta'] = 110
        self.assertEqual(sync.ranked_models(second, state['previous'], order),
                         ['alpha', 'beta', 'gamma', 'epsilon'])
        gap = {'date': '2026-10-29', 'totals': second['totals']}
        self.assertIsNone(sync.advance_model_state(gap, state)['previous'])
        with self.assertRaisesRegex(ValueError, 'predates'):
            sync.advance_model_state(first, state)

    def test_displayed_columns_enforce_rank_and_membership(self):
        html = ('<section id="models"><span class="role-label font-karla">Primary</span>'
                '<span class="entry-name">Alpha</span><span class="entry-name">Beta</span>'
                '<span class="role-label font-karla">Secondary</span>'
                '<span class="entry-name">Gamma</span><span class="entry-name">Delta</span></section>')
        self.assertEqual(sync.displayed_models(html), ['alpha', 'beta', 'gamma', 'delta'])
        with self.assertRaisesRegex(RuntimeError, 'four distinct'):
            sync.displayed_models(html.replace('Delta</span>', 'Gamma</span>'))


class VercelAuthTests(unittest.TestCase):
    def test_unexpired_login_does_not_change_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'auth.json'
            original = json.dumps({'token': 'current', 'expiresAt': 4102444800})
            path.write_text(original)
            self.assertEqual(sync.vercel_access_token(path), 'current')
            self.assertEqual(path.read_text(), original)

    def test_expired_login_without_refresh_preserves_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'auth.json'
            original = json.dumps({'token': 'expired', 'expiresAt': 1})
            path.write_text(original)
            with self.assertRaisesRegex(RuntimeError, 'without a refresh token'):
                sync.vercel_access_token(path)
            self.assertEqual(path.read_text(), original)

    def test_refresh_replaces_credentials_and_preserves_other_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'auth.json'
            original = json.dumps({'token': 'old', 'refreshToken': 'old-refresh', 'userId': 'account'}).encode()
            path.write_bytes(original)
            sync.save_refreshed_vercel_auth(path, original,
                {'access_token': 'new', 'refresh_token': 'new-refresh', 'expires_in': 3600})
            auth = json.loads(path.read_text())
            self.assertEqual((auth['token'], auth['refreshToken'], auth['userId']),
                             ('new', 'new-refresh', 'account'))
            self.assertGreater(auth['expiresAt'], sync.time.time())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_refresh_does_not_overwrite_concurrent_login(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / 'auth.json'
            original = json.dumps({'token': 'old', 'refreshToken': 'old-refresh'}).encode()
            path.write_text('{"token":"concurrent"}')
            with self.assertRaisesRegex(RuntimeError, 'changed during refresh'):
                sync.save_refreshed_vercel_auth(path, original,
                    {'access_token': 'new', 'refresh_token': 'new-refresh', 'expires_in': 3600})
            self.assertEqual(json.loads(path.read_text())['token'], 'concurrent')
            recovery, = root.glob('.vercel-auth-recovery-*')
            self.assertEqual(json.loads(recovery.read_text())['refreshToken'], 'new-refresh')
            self.assertEqual(recovery.stat().st_mode & 0o777, 0o600)


class InventoryTests(unittest.TestCase):
    def test_cli_keeps_only_curated_descriptions(self):
        catalogue = {'schema_version': 2, 'mode': 'curated', 'tools': [
            {'name': 'example', 'description': 'Search documents', 'why': 'Find answers',
             'when': 'Research', 'path': '/home/private/tool', 'help_hint': 'secret'},
        ]}
        self.assertEqual(sync.cli_inventory(catalogue), [
            {'name': 'example', 'description': 'Search documents', 'why': 'Find answers', 'when': 'Research'}])
        catalogue['tools'].append(dict(catalogue['tools'][0]))
        with self.assertRaisesRegex(RuntimeError, 'unique'):
            sync.cli_inventory(catalogue)
        catalogue['tools'].pop()
        catalogue['schema_version'] = 3
        with self.assertRaisesRegex(RuntimeError, 'Unsupported'):
            sync.cli_inventory(catalogue)

    def test_selected_skill_scripts_are_snapshotted_and_hashed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills = root / 'installed'
            site = root / 'site'
            site.mkdir()
            (site / 'main.js').write_text("const paths = {'public': 'skills/public/SKILL.md'};")
            for name in ('public', 'private'):
                (skills / name / 'scripts').mkdir(parents=True)
                (skills / name / 'SKILL.md').write_text('Skill instructions')
                (skills / name / 'scripts/run.py').write_text('print(1)')
            first = sync.capture_skills(skills, root / 'first', site)
            self.assertEqual((root / 'first/skills/public/scripts/run.py').read_text(), 'print(1)')
            self.assertFalse((root / 'first/skills/private/scripts/run.py').exists())
            (skills / 'public/scripts/run.py').write_text('print(2)')
            second = sync.capture_skills(skills, root / 'second', site)
            self.assertNotEqual(first['skills/public'], second['skills/public'])
            self.assertEqual(first['skills/private'], second['skills/private'])


    def test_hook_excerpts_exclude_strings_and_private_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            root = home / 'hooks/post'
            root.mkdir(parents=True)
            hook = root / 'gate.ts'
            hook.write_text('// Checks whether a task is complete.\n// Install at /home/private/gate\n'
                            'pi.on("session_stop", () => "private implementation");\n'
                            'if (decision.continue) return;\n')
            first = sync.hook_inventory(home)
            self.assertEqual(first[0]['events'], ['session_stop'])
            self.assertIn('Checks whether a task is complete.', first[0]['evidence'])
            self.assertIn('if (decision.continue) return;', first[0]['evidence'])
            self.assertNotIn('private', str(first))
            hook.write_text(hook.read_text().replace('implementation', 'change'))
            self.assertNotEqual(first[0]['digest'], sync.hook_inventory(home)[0]['digest'])
            hook.write_text('')
            with self.assertRaisesRegex(RuntimeError, 'Empty hook'):
                sync.hook_inventory(home)

    def test_codex_untrusted_and_disabled_hooks_are_not_active(self):
        with tempfile.TemporaryDirectory(dir=Path.home(), prefix='.ai-sync-hook-test-') as temporary:
            home = Path(temporary)
            key = str(home / 'hooks.json') + ':pre_tool_use:0:0'
            (home / 'config.toml').write_text(
                '[features]\nhooks = true\n[hooks.state.' + json.dumps(key) + ']\nenabled = false\n')
            (home / 'hooks.json').write_text(json.dumps({'hooks': {'PreToolUse': [{
                'matcher': 'Bash', 'hooks': [
                    {'type': 'command', 'command': 'true', 'statusMessage': 'Disabled hook'},
                    {'type': 'command', 'command': 'true', 'statusMessage': 'Untrusted hook'},
                ]}]}}))
            self.assertEqual(sync.codex_hook_inventory(home), [])

    def test_mcp_research_requires_evidence_for_every_requested_server(self):
        item = {'source_kind': 'mcp_tools', 'source': 'configured MCP',
                'description': 'Search indexed documents',
                'evidence': ['search: Find documents', 'secret token must not appear']}
        report = {'status': 'complete', 'servers': {'example': item}}
        inventory = [{'name': 'example', 'evidence': []}]
        self.assertEqual(sync.normalize_mcp_research(report, inventory), [
            {'name': 'example', 'source': 'mcp_tools',
             'text': 'Search indexed documents\nsearch: Find documents'}])
        with self.assertRaisesRegex(RuntimeError, 'incomplete'):
            sync.normalize_mcp_research(report, inventory + [{'name': 'missing', 'evidence': []}])
        item['evidence'] = ['secret token must not appear']
        with self.assertRaisesRegex(RuntimeError, 'public-safe evidence'):
            sync.normalize_mcp_research(report, inventory)
        item['evidence'] = ['search: Find documents']
        item['source_kind'] = 'guess'
        with self.assertRaisesRegex(RuntimeError, 'supported source'):
            sync.normalize_mcp_research(report, inventory)
        item['source_kind'] = 'offline_tools'
        with self.assertRaisesRegex(RuntimeError, 'unavailable captured metadata'):
            sync.normalize_mcp_research(report, inventory)
        inventory[0]['evidence'] = [{'source': 'offline MCP tools/list', 'text': 'search: Find documents'}]
        self.assertEqual(sync.normalize_mcp_research(report, inventory)[0]['source'], 'offline_tools')
        item['source_kind'] = 'official_doc'
        with self.assertRaisesRegex(RuntimeError, 'HTTPS documentation'):
            sync.normalize_mcp_research(report, inventory)

    def test_mcp_cache_requires_matching_config_and_unexpired_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = {'command': 'server', 'args': ['--stdio']}
            config_hash = sync.digest(b'{"args":["--stdio"],"command":"server","type":"stdio"}')
            payload = json.dumps({'version': 1, 'configHash': config_hash, 'tools': [
                {'name': 'search', 'description': 'Search a code graph'},
                {'name': 'auth', 'description': 'token secret should not be published'},
            ]})
            with sqlite3.connect(root / 'agent.db') as connection:
                connection.execute('CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT, expires_at INTEGER)')
                connection.executemany('INSERT INTO cache VALUES (?, ?, ?)', [
                    ('mcp_tools:current', payload, 4102444800),
                    ('mcp_tools:expired', payload, 1),
                    ('mcp_tools:changed', payload, 4102444800),
                ])
            servers = {'current': config, 'expired': config,
                       'changed': {'command': 'other', 'args': ['--stdio']}}
            evidence = sync.mcp_cache_evidence(root, {}, servers, list(servers), 'omp/18.12.0')
            self.assertEqual(evidence, {'current': [
                {'source': 'cached MCP tools/list', 'text': 'search: Search a code graph'}]})
            self.assertEqual(sync.mcp_cache_evidence(root, {}, servers, list(servers), 'omp/19.0.0'), {})

    def test_mcp_evidence_reads_local_package_without_config_secrets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'package'
            (root / 'dist').mkdir(parents=True)
            script = root / 'dist/server.js'
            script.write_text('server')
            script.chmod(0o755)
            (root / 'package.json').write_text('{"description": "Search a local code graph"}')
            (root / 'README.md').write_text(
                '# Graph server\nIndexes code and finds references.\n'
                'Connect to https://example.test/private\n'
                '```sh\nexport TOKEN=secret\n```\n')
            evidence = sync.mcp_evidence({'command': 'node', 'args': [str(script)],
                                          'env': {'TOKEN': 'never copy'}})
            self.assertIn('Search a local code graph', str(evidence))
            self.assertIn('Indexes code and finds references', str(evidence))
            self.assertNotIn('never copy', str(evidence))
            self.assertNotIn('example.test', str(evidence))
            self.assertNotIn('secret', str(evidence))
            self.assertEqual(sync.mcp_evidence({'command': str(script)}), evidence)

    def test_mcp_evidence_does_not_describe_the_launcher(self):
        self.assertEqual(sync.mcp_evidence({'command': 'node', 'args': ['some-package']}), [])

    def test_stdio_tool_discovery_is_offline_and_credential_free(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            private = root / 'private.txt'
            private.write_text('private')
            server = root / 'server.py'
            server.write_text(
                'import json, os, pathlib, sys\n'
                f'private = pathlib.Path({str(private)!r})\n'
                f'host_net = {os.readlink("/proc/self/ns/net")!r}\n'
                'isolated = not private.exists() and "SENSITIVE" not in os.environ '
                'and os.readlink("/proc/self/ns/net") != host_net\n'
                'for line in sys.stdin:\n'
                '    message = json.loads(line)\n'
                '    if message.get("method") == "initialize":\n'
                '        print(json.dumps({"jsonrpc": "2.0", "id": 1, "result": {}}), flush=True)\n'
                '    if message.get("method") == "tools/list":\n'
                '        page = message.get("params", {}).get("cursor")\n'
                '        description = "Isolation verified" if isolated else "Isolation failed"\n'
                '        result = {"tools": [{"name": "capture" if not page else "inspect", '
                '"description": description}]}\n'
                '        if not page: result["nextCursor"] = "next"\n'
                '        print(json.dumps({"jsonrpc": "2.0", "id": message["id"], "result": result}), flush=True)\n'
            )
            evidence = sync.mcp_tool_evidence({
                'command': '/usr/bin/python3', 'args': [str(server)], 'env': {'SENSITIVE': 'private'}})
            self.assertEqual(evidence, [{'source': 'offline MCP tools/list',
                                         'text': 'capture: Isolation verified\ninspect: Isolation verified'}])
            self.assertEqual(sync.mcp_tool_evidence({'command': '/usr/bin/python3',
                                                     'args': ['--token', 'private']}), [])

    def test_stdio_node_server_can_load_its_installed_package_offline(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'package'
            (root / 'dist').mkdir(parents=True)
            dependency = root / 'node_modules' / 'fixture'
            dependency.mkdir(parents=True)
            (root / 'package.json').write_text('{}')
            (dependency / 'index.js').write_text(
                "module.exports = { name: 'inspect', description: 'Inspect indexed documents' };")
            server = root / 'dist' / 'server.js'
            server.write_text(
                '#!/usr/bin/env node\n'
                "const readline = require('readline'); const tool = require('fixture');\n"
                "readline.createInterface({input: process.stdin}).on('line', line => {\n"
                '  const message = JSON.parse(line);\n'
                "  if (message.method === 'initialize' || message.method === 'tools/list')\n"
                "    console.log(JSON.stringify({jsonrpc: '2.0', id: message.id, "
                "result: message.method === 'initialize' ? {} : {tools: [tool]}}));\n"
                '});\n')
            server.chmod(0o755)
            self.assertEqual(sync.mcp_tool_evidence({'command': str(server)}), [
                {'source': 'offline MCP tools/list', 'text': 'inspect: Inspect indexed documents'}])

    def test_cli_reconciliation_checks_names_descriptions_and_duplicates(self):
        catalogue = [{'name': 'alpha', 'description': 'Search & find'},
                     {'name': 'beta', 'description': 'Inspect files'}]
        alpha = ('<div class="stack-entry"><div><a><span class="entry-name">alpha</span>'
                 '</a></div><p class="entry-description">Search &amp; find</p></div>')
        beta = ('<div class="stack-entry"><span class="entry-name">beta</span>'
                '<p class="entry-description">Inspect files</p></div>')
        def wrap(entries):
            return '<section class="stack-section" id="cli-tools">' + entries + '</section>'
        sync.validate_cli(wrap(alpha + beta), catalogue)
        for entries in (alpha, alpha + beta + beta, alpha + beta.replace('Inspect files', 'Old description'),
                        alpha + beta.replace('beta', 'obsolete')):
            with self.subTest(entries=entries), self.assertRaisesRegex(RuntimeError, 'lsops catalogue'):
                sync.validate_cli(wrap(entries), catalogue)

    def test_extensions_are_separate_and_backup_files_excluded(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            root = home / 'extensions'
            root.mkdir()
            (root / 'catalogue.js').write_text('pi.on("session_start", handler);')
            (root / 'catalogue.js.backup').write_text('old')
            entries = sync.extension_inventory(home)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]['events'], ['session_start'])


class DailyUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.site = self.root / 'site'
        sync.command(['jj', 'git', 'init', str(self.site)])
        (self.site / 'agents').mkdir()
        (self.site / 'skills/example').mkdir(parents=True)
        (self.site / 'index.html').write_text('<div class="change-group" data-group="22/10/2026"><div class="change-entry"><h3 class="change-title">Existing history</h3><p>Original detail</p></div></div><div id="example"></div>')
        (self.site / 'main.js').write_text("const skillContentPaths = {'example': 'skills/example/SKILL.md'};\n")
        (self.site / 'skills/example/SKILL.md').write_text('Public skill\n')
        (self.site / 'agents/AGENTS.md').write_text('Public instructions\n')
        sync.jj(self.site, 'describe', '-m', 'fixture')
        self.base = sync.jj(self.site, 'log', '--no-graph', '-r', '@', '-T', 'commit_id')
        sync.jj(self.site, 'new')
        self.report = {'status': 'complete', 'sources': {'omp': {'action': 'applied', 'reason': 'Changed primary harness'}}}

    def tearDown(self):
        self.temp.cleanup()

    def test_source_hashes_detect_add_modify_remove(self):
        self.assertEqual(sync.changed_sources({'a': '1', 'b': '2'}, {'b': '3', 'c': '4'}), ['a', 'b', 'c'])
        with self.assertRaisesRegex(RuntimeError, 'catalog lost'):
            sync.changed_sources({str(i): 'x' for i in range(21)}, {})

    def test_rejects_incomplete_report(self):
        with self.assertRaisesRegex(RuntimeError, 'every changed source'):
            sync.validate(self.site, self.base, ['omp', 'agents'], self.report)

    def test_ignored_cli_change_cannot_bypass_catalogue_validation(self):
        (self.root / 'source').mkdir()
        (self.root / 'editorial').mkdir()
        (self.root / 'source/cli.json').write_text(json.dumps([
            {'name': 'new-tool', 'description': 'Search documents'}]))
        (self.root / 'input.json').write_text(json.dumps({
            'base': self.base, 'changed': ['cli'], 'sources': {}}))
        (self.root / 'editorial/report.json').write_text(json.dumps({
            'status': 'complete', 'sources': {'cli': {'action': 'ignored', 'reason': 'No change'}}}))
        with (self.site / 'index.html').open('a') as file:
            file.write('<section id="cli-tools"><div class="stack-entry">'
                       '<span class="entry-name">new-tool</span>'
                       '<p class="entry-description">Old description</p></div></section>')
        with self.assertRaisesRegex(RuntimeError, 'lsops catalogue'):
            sync.finish_prepare(self.root)

    def test_accepts_real_valid_edit(self):
        with (self.site / 'index.html').open('a') as f:
            f.write('<p>OMP is primary.</p>')
        self.assertEqual(sync.validate(self.site, self.base, ['omp'], self.report), ['index.html'])

    def test_rejects_unplanned_script_change(self):
        (self.site / 'unexpected.py').write_text('print(1)')
        with self.assertRaisesRegex(RuntimeError, 'allowlist'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_selected_skill_script_is_allowed_but_private_skill_is_rejected(self):
        script = self.site / 'skills/example/scripts/run.py'
        script.parent.mkdir()
        script.write_text('print("hello")\n')
        self.assertEqual(sync.validate(self.site, self.base, ['omp'], self.report),
                         ['skills/example/scripts/run.py'])
        script.unlink()
        private = self.site / 'skills/private/scripts/run.py'
        private.parent.mkdir(parents=True)
        private.write_text('print("private")\n')
        with self.assertRaisesRegex(RuntimeError, 'unselected skill'):
            sync.validate(self.site, self.base, ['omp'], self.report)


    def test_rejects_symlink_and_deletion(self):
        (self.site / 'skills/example/SKILL.md').unlink()
        with self.assertRaisesRegex(RuntimeError, 'deletions or symlinks'):
            sync.validate(self.site, self.base, ['omp'], self.report)
        (self.site / 'skills/example/SKILL.md').symlink_to('/etc/hostname')
        with self.assertRaisesRegex(RuntimeError, 'deletions or symlinks'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_rejects_history_loss(self):
        (self.site / 'index.html').write_text('<div id="example"></div>')
        with self.assertRaisesRegex(RuntimeError, 'Historical'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_rejects_broken_skill_link(self):
        (self.site / 'main.js').write_text("const paths = {'example': 'skills/missing/SKILL.md'};")
        with self.assertRaisesRegex(RuntimeError, 'Broken local skill'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_rejects_private_paths(self):
        (self.site / 'agents/AGENTS.md').write_text('Use /home/operator/private-key')
        with self.assertRaisesRegex(RuntimeError, 'Private machine'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_rejects_private_request_metadata(self):
        (self.site / 'agents/AGENTS.md').write_text(sync.UA)
        with self.assertRaisesRegex(RuntimeError, 'Private request metadata'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_changed_candidate_rejected_before_remote_access(self):
        candidate = {'workspace': str(self.site), 'base': self.base, 'tree': {}}
        (self.site / 'index.html').write_text('tampered')
        with self.assertRaisesRegex(RuntimeError, 'changed after validation'):
            sync.publish({'state': str(self.root)}, candidate)

    def test_rejects_history_detail_loss(self):
        path = self.site / 'index.html'
        path.write_text(path.read_text().replace('<p>Original detail</p>', ''))
        with self.assertRaisesRegex(RuntimeError, 'Historical'):
            sync.validate(self.site, self.base, ['omp'], self.report)


    def test_resume_after_push_does_not_create_another_commit(self):
        remote = self.root / 'remote.git'
        sync.command(['git', 'init', '--bare', str(remote)])
        sync.jj(self.site, 'git', 'remote', 'add', 'origin', str(remote))
        sync.jj(self.site, 'bookmark', 'set', 'main', '-r', self.base)
        sync.jj(self.site, 'git', 'push', '--remote', 'origin', '--bookmark', 'main', '--allow-new')
        (self.site / 'index.html').write_text((self.site / 'index.html').read_text() + '<p>OMP</p>')
        tree = {'index.html': sync.digest((self.site / 'index.html').read_bytes())}
        candidate = {'workspace': str(self.site), 'directory': str(self.root), 'base': self.base,
                     'tree': tree, 'expected': tree, 'sources': {'omp': 'snapshot'}}
        config = {'state': str(self.root), 'repo': str(self.site),
                  'vercel_auth': str(self.root / 'unavailable-credential.json')}
        # A real missing credential fails verification after a real local-remote push.
        with self.assertRaises(FileNotFoundError):
            sync.publish(config, candidate)
        pending = sync.read_json(self.root / 'pending.json')
        head = sync.remote_head(self.site)
        self.assertEqual(head, pending['commit'])
        self.assertNotEqual(head, self.base)
        self.assertFalse((self.root / 'checkpoint.json').exists())
        with self.assertRaises(FileNotFoundError):
            sync.publish(config, pending)
        self.assertEqual(sync.remote_head(self.site), head)
        self.assertEqual(sync.read_json(self.root / 'pending.json'), pending)

    def test_rejects_entry_moved_outside_date_group(self):
        path = self.site / 'index.html'
        path.write_text(path.read_text().replace('data-group="22/10/2026">', 'data-group="22/10/2026"></div>'))
        with self.assertRaisesRegex(RuntimeError, 'Historical'):
            sync.validate(self.site, self.base, ['omp'], self.report)

    def test_path_allowlist(self):
        for path in ('../index.html', '/index.html', 'skills/../private.md', 'skills/a/script.py', 'vercel.json'):
            self.assertFalse(sync.allowed(path), path)
        self.assertTrue(sync.allowed('skills/example/references/guide.md'))
        self.assertTrue(sync.allowed('skills/example/scripts/run.py'))


if __name__ == '__main__':
    unittest.main()
