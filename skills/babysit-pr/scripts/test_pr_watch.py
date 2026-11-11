import unittest
from datetime import datetime, timezone

import pr_watch

HEAD = 'a' * 40
NOW = datetime(2026, 1, 1, 1, tzinfo=timezone.utc)
PUSHED = '2026-01-01T00:00:00Z'


def comment(author, body):
    return {'id': author, 'author': {'login': author, '__typename': 'Bot'}, 'body': body,
            'createdAt': '2026-01-01T00:10:00Z', 'updatedAt': '2026-01-01T00:10:00Z',
            'url': 'https://example.com/comment', 'reactions': {'nodes': []}}


def review(author, state, head=HEAD, body=''):
    return {'author': {'login': author, '__typename': 'Bot'}, 'state': state, 'body': body,
            'commit': {'oid': head}, 'url': 'https://example.com/review', 'submittedAt': '2026-01-01T00:10:00Z'}


def pr(comments=(), reviews=(), checks=(), threads=()):
    return {'url': 'https://github.com/owner/repo/pull/1', 'state': 'OPEN', 'headRefOid': HEAD,
            'commits': {'nodes': [{'commit': {'committedDate': PUSHED, 'statusCheckRollup': {'contexts': {'nodes': list(checks)}}}}]},
            'timelineItems': {'nodes': []}, 'headComments': {'nodes': list(comments)}, 'tailComments': {'nodes': []},
            'reviews': {'nodes': list(reviews)}, 'reviewThreads': {'nodes': list(threads)},
            'mergeable': 'MERGEABLE', 'mergeStateStatus': 'CLEAN', 'baseRefName': 'main', 'isDraft': False}


def evaluate(value, ignore=()):
    return pr_watch.evaluate(value, 'owner', NOW, ['coderabbit', 'codex'], list(ignore))


class ReviewGateTests(unittest.TestCase):
    def test_either_clean_review_satisfies_gate_and_suppresses_triggers(self):
        codex = comment('chatgpt-codex-connector', f"Didn't find any major issues. Reviewed commit: `{HEAD}`")
        rabbit = review('coderabbitai', 'APPROVED')
        codex_approval = review('chatgpt-codex-connector', 'APPROVED')
        rabbit_clean_comment = review('coderabbitai', 'COMMENTED', body='**Actionable comments posted: 0**')
        for value in (pr(comments=[codex]), pr(reviews=[rabbit]), pr(reviews=[codex_approval]), pr(reviews=[rabbit_clean_comment])):
            with self.subTest(value=value):
                result = evaluate(value)
                self.assertEqual(result['verdict'], 'ready')
                self.assertFalse(any(s.get('trigger') for s in result['bots'].values()))

    def test_findings_or_stale_review_does_not_satisfy_gate(self):
        for item in (review('chatgpt-codex-connector', 'COMMENTED'),
                     review('coderabbitai', 'COMMENTED'), review('coderabbitai', 'APPROVED', 'b' * 40)):
            with self.subTest(item=item):
                self.assertEqual(evaluate(pr(reviews=[item]))['verdict'], 'waiting')

    def test_approval_with_outside_findings_does_not_clear_other_bot(self):
        rabbit = review('coderabbitai', 'APPROVED', body='Outside diff range comments (1)')
        result = evaluate(pr(reviews=[rabbit]))
        self.assertEqual(result['verdict'], 'action_needed')
        self.assertTrue(any(item['kind'] == 'bot_review' for item in result['waiting']))
        self.assertTrue(result['bots']['codex'].get('trigger'))

    def test_existing_findings_remain_actionable(self):
        codex = comment('chatgpt-codex-connector', f"Didn't find any major issues. Reviewed commit: `{HEAD}`")
        rabbit = review('coderabbitai', 'APPROVED', body='Outside diff range comments (1)')
        result = evaluate(pr(comments=[codex], reviews=[rabbit]))
        self.assertEqual(result['verdict'], 'action_needed')
        self.assertEqual(result['actions'][0]['kind'], 'body_findings')

    def test_required_coderabbit_check_is_not_ignored(self):
        codex = comment('chatgpt-codex-connector', f"Didn't find any major issues. Reviewed commit: `{HEAD}`")
        check = {'__typename': 'CheckRun', 'name': 'CodeRabbit', 'status': 'IN_PROGRESS',
                 'conclusion': None, 'isRequired': True, 'detailsUrl': None}
        result = evaluate(pr(comments=[codex], checks=[check]), ['*'])
        self.assertEqual(result['verdict'], 'waiting')
        self.assertEqual(result['waiting'][0]['kind'], 'check_pending')
        check.update(status='COMPLETED', conclusion='FAILURE')
        result = evaluate(pr(comments=[codex], checks=[check]), ['*'])
        self.assertEqual(result['actions'][0]['kind'], 'check_failed')


if __name__ == '__main__':
    unittest.main()
