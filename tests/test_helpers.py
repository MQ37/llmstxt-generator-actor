from typing import TYPE_CHECKING

from src.helpers import clean_llms_data, get_hostname_path_string_from_url, get_url_path_dir, normalize_url

if TYPE_CHECKING:
    from src.mytypes import LLMSData


def test_clean_llms_data() -> None:
    # Test case 1: Normal case where sections with fewer links are moved to index
    data: LLMSData = {
        'title': 'Test LLMS',
        'description': None,
        'details': None,
        'sections': {
            'section_1': {
                'title': 'Section 1',
                'links': [{'url': 'http://example.com', 'title': 'Example', 'description': None}],
            },
            'section_2': {
                'title': 'Section 2',
                'links': [
                    {'url': 'http://example2.com', 'title': 'Example 2', 'description': None},
                    {'url': 'http://example3.com', 'title': 'Example 3', 'description': None},
                ],
            },
        },
    }

    clean_llms_data(data, section_min_links=2)

    assert 'section_1' not in data['sections']  # Section 1 should be removed
    assert 'section_2' in data['sections']  # Section 2 should remain
    assert '/' in data['sections']  # Index section should be created
    assert len(data['sections']['/']['links']) == 1  # The link from section_1 should be moved to index

    # Test case 2: If all sections meet the minimum link count, nothing changes
    data2: LLMSData = {
        'title': 'Test LLMS',
        'description': None,
        'details': None,
        'sections': {
            'section_1': {
                'title': 'Section 1',
                'links': [
                    {'url': 'http://example.com', 'title': 'Example', 'description': None},
                    {'url': 'http://example2.com', 'title': 'Example 2', 'description': None},
                ],
            }
        },
    }

    clean_llms_data(data2, section_min_links=2)

    assert 'section_1' in data2['sections']  # Section 1 should remain
    assert '/' not in data2['sections']  # Index section should not be created

    # Test case 4: Empty sections dictionary
    data4: LLMSData = {'title': 'Empty LLMS', 'description': None, 'details': None, 'sections': {}}

    clean_llms_data(data4, section_min_links=2)

    assert data4['sections'] == {}  # Sections should remain empty

    # Test case 5: Sections already have an index section
    data5: LLMSData = {
        'title': 'LLMS with Index',
        'description': None,
        'details': None,
        'sections': {
            '/': {'title': 'Index', 'links': [{'url': 'http://index.com', 'title': 'Index Link', 'description': None}]},
            'section_1': {
                'title': 'Section 1',
                'links': [{'url': 'http://example.com', 'title': 'Example', 'description': None}],
            },
        },
    }

    clean_llms_data(data5, section_min_links=2)

    assert 'section_1' not in data5['sections']  # Section 1 should be removed
    assert '/' in data5['sections']  # Index should remain
    assert len(data5['sections']['/']['links']) == 2  # Index should now contain both the old and new links


def test_get_url_path_dir() -> None:
    url = 'https://example.com/dir/subdir/page'
    _dir = '/dir/subdir'
    assert get_url_path_dir(url) == _dir

    url2 = 'https://example.com/page'
    _dir2 = '/'
    assert get_url_path_dir(url2) == _dir2

    url3 = 'https://example.com/dir/page/'
    _dir3 = '/dir'
    assert get_url_path_dir(url3) == _dir3


def test_normalize_url() -> None:
    url = 'https://example.com/'
    url_normalized = 'https://example.com'
    assert normalize_url(url) == url_normalized

    url2 = 'https://example.com/dir/page'
    url2_normalized = 'https://example.com/dir/page'
    assert normalize_url(url2) == url2_normalized

    url3 = 'https://example.com/dir/page/'
    url3_normalized = 'https://example.com/dir/page'
    assert normalize_url(url3) == url3_normalized


def test_get_hostname_path_string_from_url() -> None:
    url = 'https://example.com/path'
    assert get_hostname_path_string_from_url(url) == 'example.com/path'

    url2 = 'https://example.com/path/'
    assert get_hostname_path_string_from_url(url2) == 'example.com/path/'
