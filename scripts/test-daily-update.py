#!/usr/bin/env python3
"""Exercise validation with real Jujutsu repositories and actual publication files."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('daily_update', Path(__file__).with_name('daily-update.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


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

    def test_accepts_real_valid_edit(self):
        with (self.site / 'index.html').open('a') as f:
            f.write('<p>OMP is primary.</p>')
        self.assertEqual(sync.validate(self.site, self.base, ['omp'], self.report), ['index.html'])

    def test_rejects_unplanned_script_change(self):
        (self.site / 'unexpected.py').write_text('print(1)')
        with self.assertRaisesRegex(RuntimeError, 'allowlist'):
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

    def test_sandbox_sources_readonly_and_home_hidden(self):
        source = self.root / 'source'
        output = self.root / 'output'
        runtime = self.root / 'runtime'
        for path in (source, output, runtime):
            path.mkdir()
        (source / 'evidence').write_text('immutable')
        script = """from pathlib import Path
source, output, site, hidden = map(Path, __import__('sys').argv[1:])
try:
    (source / 'evidence').write_text('tampered')
    raise AssertionError('source writable')
except OSError:
    pass
assert not hidden.exists(), 'operator home visible'
(output / 'report').write_text('ok')
(site / 'editable').write_text('ok')
"""
        with tempfile.TemporaryDirectory(dir=Path.home(), prefix='.ai-sync-test-') as hidden_dir:
            hidden = Path(hidden_dir) / 'sentinel'
            hidden.write_text('must not be visible')
            sync.command(sync.sandbox(self.site, source, output, runtime) +
                         ['/usr/bin/python3', '-c', script, str(source), str(output), str(self.site), str(hidden)])
        self.assertEqual((source / 'evidence').read_text(), 'immutable')
        self.assertEqual((output / 'report').read_text(), 'ok')

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


if __name__ == '__main__':
    unittest.main()
