import pytest

from datetime import datetime, timedelta

from mail.dbapi import RuleQuery


@pytest.fixture
def rule_query():
    rule = {
        "description": "Rule_1",
        "conditions": [
            {
                "field": "sender",
                "predicate": "contains",
                "value": "neupass.com"
            },
            {
                "field": "subject",
                "predicate": "not equals",
                "value": "better"
            },
            {
                "field": "date",
                "predicate": "less than",
                "value": "2"
            }
        ],
        "predicate": "All"
    }
    return RuleQuery(rule)


def test_get_query_for_condition_contains(rule_query):
    query = "SELECT * FROM email WHERE "
    condition = {
        "field": "sender",
        "predicate": "contains",
        "value": "neupass.com"
    }
    expected_query = "SELECT * FROM email WHERE sender LIKE '%neupass.com%' AND "
    assert rule_query.get_query_for_condition(query, condition) == expected_query


def test_get_query_for_condition_not_equals(rule_query):
    query = "SELECT * FROM email WHERE "
    condition = {
        "field": "subject",
        "predicate": "not equals",
        "value": "better"
    }
    expected_query = "SELECT * FROM email WHERE subject <> 'better' AND "
    assert rule_query.get_query_for_condition(query, condition) == expected_query


def test_get_query_for_condition_less_than(rule_query):
    query = "SELECT * FROM email WHERE "
    condition = {
        "field": "date",
        "predicate": "less than",
        "value": "2"
    }
    n_days_ago = datetime.now() - timedelta(days=2)
    n_days_ago_str = n_days_ago.strftime('%Y-%m-%d')
    expected_query = "SELECT * FROM email WHERE date < '2023-06-08' AND "
    assert rule_query.get_query_for_condition(query, condition) == expected_query


def test_remove_trailing_predicate_and(rule_query):
    query = "SELECT * FROM email WHERE sender LIKE '%neupass.com%' AND "
    expected_query = "SELECT * FROM email WHERE sender LIKE '%neupass.com%'"
    assert rule_query.remove_trailing_predicate(query) == expected_query


def test_build_query(rule_query):
    expected_query = "SELECT * FROM email WHERE sender LIKE '%neupass.com%' AND subject <> 'better' AND date < '2023-06-08'"
    assert rule_query.build_query() == expected_query
